from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)  # Permitir valores nulos temporalmente
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorites = db.relationship('Favorites', backref='user', lazy=True)
    
    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username":self.username,
            "email": self.email
        }
    def serializeFavorite(self):
        return{
            "favorites": [favorite.serialize() for favorite in self.favorites]
        }



class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    starship_id = db.Column(db.Integer, db.ForeignKey('starships.id'))
    
    
    def __repr__(self):
        return f'<Favorites {self.id}>'

    def serialize(self): 
        if self.planet_id is not None:
            planet = Planets.query.filter_by(id = self.planet_id).first().serialize()
            return {'planet': planet}
        if self.people_id is not None:
            people = People.query.filter_by(id = self.people_id).first().serialize()
            return {'people': people}
        if self.starship_id is not None:
            starships = Starships.query.filter_by(id = self.starship_id).first().serialize()
            return {"starship": starships}
        
        
class People (db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    height = db.Column(db.Integer(), nullable=False)
    hair_color = db.Column(db.String(255), nullable=False)
    skin_color = db.Column(db.String(255), nullable=False)
    eye_color = db.Column(db.String(255), nullable=False)
    birth_year = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(255), nullable=False)
    homeworld = db.Column(db.Integer(), db.ForeignKey('planets.id'), nullable=True)
    favorites = db.relationship('Favorites', backref='people', lazy=True)
    
    def __repr__(self):
        return '<People %r>' % self.name
    
    def serialize(self):
        homeworld = Planets.query.filter_by(id = self.homeworld).first().serialize()
        return {
        "id" : self.id,
        "name" : self.name,
        "height" : self.height,
        "hair_color": self.hair_color,
        "skin_color": self.skin_color,
        "eye_color": self.eye_color,
        "birth_year": self.birth_year,
        "gender": self.gender,
        "homeworld": homeworld,
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    diameter = db.Column(db.Integer(), nullable=False)
    rotation_period = db.Column(db.Integer(), nullable=False)
    orbital_period = db.Column(db.Integer(), nullable=False)
    gravity = db.Column(db.Integer(), nullable=False)
    population = db.Column(db.Integer(), nullable=False)
    climate = db.Column(db.String(255), nullable=False)
    terrain = db.Column(db.String(255), nullable=False)
    surface_water = db.Column(db.Integer(), nullable=False)
    favorites = db.relationship('Favorites', backref='planets', lazy=True)
    
    def __repr__(self):
        return '<Planets %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
        }
        
class Starships(db.Model):
    __tablename__ = "starships"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    starship_class = db.Column(db.String(255), nullable=False)
    manufacter = db.Column(db.String(255), nullable=False)
    cost_in_credits = db.Column(db.Integer(), nullable=False)
    length = db.Column(db.Integer(), nullable=False)
    consumables = db.Column(db.String(255), nullable=False)
    passengers = db.Column(db.Integer(), nullable=False)
    favorites = db.relationship('Favorites', backref='starships', lazy=True)
    
    def __repr__(self):
        return '<Starships %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "starship_class": self.starship_class,
            "manufacter": self.manufacter,
            "cost_in_credits": self.cost_in_credits,
            "length" : self.length,
            "consumables": self.consumables,
            "passengers": self.passengers,
        }