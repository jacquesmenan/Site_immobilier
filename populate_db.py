from app import create_app, db
from app.models import Property
from datetime import datetime, timedelta
import random

app = create_app()

# Données de test
property_types = ['Appartement', 'Maison', 'Villa', 'Loft', 'Château']
cities = ['Paris', 'Lyon', 'Marseille', 'Bordeaux', 'Toulouse', 'Nantes', 'Lille', 'Strasbourg']
descriptions = [
    "Magnifique bien lumineux avec vue imprenable",
    "Propriété spacieuse et moderne",
    "Cadre exceptionnel avec jardin arboré",
    "Appartement rénové avec goût",
    "Propriété de caractère avec beaucoup de cachet"
]

def create_sample_properties():
    with app.app_context():
        # Vérifier si la table des propriétés existe
        if not db.engine.dialect.has_table(db.engine, 'property'):
            db.create_all()
        
        # Vérifier s'il y a déjà des propriétés dans la base
        if Property.query.first() is not None:
            print("La base de données contient déjà des propriétés.")
            return
        
        # Créer 20 propriétés de test
        for i in range(1, 21):
            property_type = random.choice(property_types)
            city = random.choice(cities)
            price = random.randint(150000, 1200000)
            size = random.randint(30, 300)
            rooms = random.randint(1, 8)
            bedrooms = max(1, rooms - random.randint(0, 2))
            
            property = Property(
                title=f"{property_type} {i} pièces à {city}",
                description=random.choice(descriptions),
                price=price,
                size=size,
                rooms=rooms,
                bedrooms=bedrooms,
                location=f"Quartier {random.randint(1, 20)}",
                city=city,
                postal_code=f"{random.randint(1, 95):02d}000",
                property_type=property_type,
                status=random.choice(['À vendre', 'En cours de négociation', 'Disponible']),
                image_url=f"https://picsum.photos/800/600?random={i}",
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 365))
            )
            
            db.session.add(property)
        
        try:
            db.session.commit()
            print("20 propriétés de test ont été ajoutées à la base de données.")
        except Exception as e:
            db.session.rollback()
            print(f"Une erreur s'est produite : {e}")

if __name__ == '__main__':
    create_sample_properties()
