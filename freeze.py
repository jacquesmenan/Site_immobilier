from app import create_app
from flask_frozen import Freezer
import os

app = create_app()
app.config['FREEZER_DESTINATION'] = 'build'
app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_DESTINATION_IGNORE'] = ['.git*', 'CNAME', '.gitignore']

freezer = Freezer(app)

# URLs à geler
urls = ['/', '/about/', '/contact/', '/properties/']

@freezer.register_generator
def url_generator():
    for url in urls:
        yield url

if __name__ == '__main__':
    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs('build', exist_ok=True)
    
    # Copier manuellement les fichiers statiques
    if os.path.exists('app/static'):
        import shutil
        if os.path.exists('build/static'):
            shutil.rmtree('build/static')
        shutil.copytree('app/static', 'build/static')
    
    # Geler le site
    freezer.freeze()