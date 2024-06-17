from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    user= db.relationship('Favorites', backref='user')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
class Planet(db.Model):
    __tablename__= 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    rotation_period   = db.Column(db.String(80), unique=False, nullable=False)
    orbital_period    = db.Column(db.String(80), unique=False, nullable=False)
    gravity = db.Column(db.String(80), unique=False, nullable=False)
    population   = db.Column(db.String(80), unique=False, nullable=False)
    terrain = db.Column(db.String(80), unique=False, nullable=False)
    planet=db.relationship('Favorites', backref='planet')
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            # do not serialize the password, its a security breach
        }
    
class Person(db.Model):
    __tablename__= 'person'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    birth_year = db.Column(db.String(80), unique=False, nullable=False)
    eye_color= db.Column(db.String(80), unique=False, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    hair_color = db.Column(db.String(80), unique=False, nullable=False)
    height = db.Column(db.String(80), unique=False, nullable=False)
    mass = db.Column(db.String(80), unique=False, nullable=False)
    homeworld  = db.Column(db.String(80), unique=False, nullable=False)
    person= db.relationship('Favorites', backref='person')
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth year": self.birth_year,
            "homeworld": self.homeworld,
            # do not serialize the password, its a security breach
        }
    
class Favorites(db.Model):
    __tablename__= 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'))
    planet_id=db.Column(db.Integer, db.ForeignKey('planet.id'))
    person_id=db.Column(db.Integer, db.ForeignKey('person.id'))

    def serialize(self):
        return {
            "id": self.id,
            "user id": self.user_id,
            # do not serialize the password, its a security breach
        }
    
    
    