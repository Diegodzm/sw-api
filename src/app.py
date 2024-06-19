"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Favorites,Person,Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=['GET'])
def getPeople():
    people= Person.query.all()
    people= list(map(lambda person:person.serialize(),people))
    return jsonify(people), 200.


@app.route('/people/<int:people_id>', methods=['GET'])
def getonePeople(people_id):
    people= Person.filter_by(id=people_id)
    return jsonify(people.serialize()), 200.

@app.route('/planet/<int:planet_id>', methods=['GET'])
def getonePlanet(planet_id):
    planet= Planet.filter_by(id=planet_id)
    return jsonify(planet.serialize()), 200.

@app.route('/planets', methods=['GET'])
def getPlanets():
    planets= Planet.query.all()
    planets=   list(map(lambda planet:planet.serialize(),planets))
    return jsonify(planets), 200

@app.route('/users', methods=['GET'])
def getUsers():
    users= User.query.all()
    users= list(map(lambda user:user.serialize(),users))
    return jsonify(users), 200.

@app.route('/users/favorites', methods=['GET'])
def getFavorites(id):
    favorites= Favorites.query.all()
    favorites= list(map(lambda favorite:favorite.serialize(),favorites))
    return jsonify(favorites), 200.

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def postFavplanet(planet_id):
    favorite=Favorites()
    favorite.planet_id=planet_id
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg":"planeta favorito agregado"}), 200.

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def postFavpeople(people_id):
    favorite=Favorites()
    favorite.people_id=people_id
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg":"personaje favorito agregado"}), 200.

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delFavpeople(people_id):
    person = Favorites.filter_by(person_id=people_id).first()
    db.session.delete(person)
    db.session.commit()
    return jsonify({"msg": "personaje eliminado correctamente"}), 200
    
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delFavplanet(planet_id):
    planet = Favorites.filter_by(planet_id=planet_id).first()
    db.session.delete(planet)
    db.session.commit()
    return jsonify({"msg": "planeta eliminado correctamente"}), 200
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
