from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    population = db.Column(db.Integer)
    climate = db.Column(db.String(50))
    terrain = db.Column(db.String(50))
    diameter = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    rotation_period = db.Column(db.Integer)
    url = db.Column(db.String(100), unique=True)

    def serialize_all(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url
        }
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "diameter": self.diameter,
            "orbital_period": self.orbital_period,
            "rotation_period": self.rotation_period,
            "url": self.url
        }
    

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    gender = db.Column(db.String(15))
    height_cm = db.Column(db.Integer)
    mass_kg = db.Column(db.Integer)
    eye_color = db.Column(db.String(20))
    hair_color = db.Column(db.String(20))
    skin_color = db.Column(db.String(20))
    url = db.Column(db.String(100), unique=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    # planet = relationship(db.Planet)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "height_cm": self.height_cm,
            "mass_kg": self.mass_kg,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "planet_id": self.planet_id,
            "url": self.url
        }
    
    def serialize_all(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40))
    username = db.Column(db.String(40))
    password = db.Column(db.String(30))

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = relationship(User)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    # character = relationship(Character)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    # planet = relationship(Planet)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id
        }