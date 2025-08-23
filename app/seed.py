from . import db
from .models import Property  # Assurez-vous que ce modèle existe dans models.py

def seed_database():
    # Vérifier si la base de données est vide
    if not Property.query.first():
        # Ajouter des propriétés d'exemple si nécessaire
        pass
    db.session.commit()
