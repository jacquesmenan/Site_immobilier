from flask import Blueprint, render_template, request
from .models import Property
from sqlalchemy import or_

# Création d'un Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def index():
    # Afficher les 6 dernières propriétés sur la page d'accueil
    latest_properties = Property.query.order_by(Property.created_at.desc()).limit(6).all()
    return render_template('index.html', properties=latest_properties)

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/properties')
def properties():
    # Récupérer les paramètres de recherche
    search = request.args.get('search', '')
    property_type = request.args.get('type', '')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    
    # Construire la requête de base
    query = Property.query
    
    # Appliquer les filtres
    if search:
        search = f"%{search}%"
        query = query.filter(
            or_(
                Property.title.ilike(search),
                Property.description.ilike(search),
                Property.location.ilike(search),
                Property.city.ilike(search)
            )
        )
    
    if property_type:
        query = query.filter(Property.property_type == property_type)
    
    if min_price:
        query = query.filter(Property.price >= float(min_price))
    
    if max_price:
        query = query.filter(Property.price <= float(max_price))
    
    # Trier par date de création décroissante
    properties = query.order_by(Property.created_at.desc()).all()
    
    # Récupérer les types de propriétés uniques pour le filtre
    property_types = [p[0] for p in Property.query.with_entities(Property.property_type).distinct().all() if p[0]]
    
    return render_template('properties.html',
                         properties=properties,
                         property_types=property_types,
                         search=request.args.get('search', ''),
                         selected_type=property_type,
                         min_price=min_price,
                         max_price=max_price)

@main.route('/search')
def search():
    # Récupérer les paramètres de recherche
    search_term = request.args.get('search', '')
    property_type = request.args.get('type', '')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    
    # Construire la requête de base
    query = Property.query
    
    # Appliquer les filtres
    if search_term:
        search_filter = f"%{search_term}%"
        query = query.filter(
            or_(
                Property.title.ilike(search_filter),
                Property.description.ilike(search_filter),
                Property.location.ilike(search_filter),
                Property.city.ilike(search_filter)
            )
        )
    
    if property_type:
        query = query.filter(Property.property_type == property_type)
    
    if min_price:
        query = query.filter(Property.price >= float(min_price))
    
    if max_price:
        query = query.filter(Property.price <= float(max_price))
    
    # Trier par date de création décroissante
    properties_result = query.order_by(Property.created_at.desc()).all()
    
    # Récupérer les types de propriétés uniques pour le filtre
    property_types = [p[0] for p in Property.query.with_entities(Property.property_type).distinct().all() if p[0]]
    
    return render_template('properties.html',
                         properties=properties_result,
                         property_types=property_types,
                         search=search_term,
                         selected_type=property_type,
                         min_price=min_price,
                         max_price=max_price)
