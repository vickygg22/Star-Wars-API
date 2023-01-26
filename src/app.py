"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
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

# @app.route('/user', methods=['GET'])
# def handle_hello():

#     response_body = {
#         "msg": "Hello, this is your GET /user response "
#     }

#     return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    print(planets)
    planets_list = list(map(lambda object : object.serialize_all(), planets))
    response_body = {
        "msg": "Hey there, this is your GET /planets response :)",
        "planets": planets_list
    }

    return jsonify(response_body), 200

@app.route("/planets/<int:id_planet>", methods=["GET"])
def get_single_planet(id_planet):
    planet = Planet.query.get(id_planet)
    return jsonify(planet.serialize()), 200

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    print(characters)
    characters_list = list(map(lambda object : object.serialize_all(), characters))
    response_body = {
        "msg": "Hey there, this is your GET /characters response :)",
        "planets": characters_list
    }

    return jsonify(response_body), 200

@app.route("/characters/<int:id_character>", methods=["GET"])
def get_single_character(id_character):
    character = Character.query.get(id_character)
    return jsonify(character.serialize()), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    print(users)
    users_list = list(map(lambda object : object.serialize(), users))
    response_body = {
        "msg": "Hey there, this is your GET /users response :)",
        "users": users_list
    }

    return jsonify(response_body), 200

@app.route("/users/<int:id_user>", methods=["GET"])
def get_single_user(id_user):
    user = User.query.get(id_user)
    return jsonify(user.serialize()), 200

@app.route("/users/<int:id_user>/favorites", methods=["GET"])
def get_user_favorites(id_user):
    user = Favorite.query.filter_by(user_id = id_user).all()
    user_favs_list = list(map(lambda object : object.serialize(), user))
    response = {
        "status": "ok",
        "favorites": user_favs_list
    }
    return jsonify(response), 200

@app.route('/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.all()
    print(favorites)
    favorites_list = list(map(lambda object : object.serialize(), favorites))
    response_body = {
        "msg": "Hey there, this is your GET /favorites response :)",
        "favorites": favorites_list
    }

    return jsonify(response_body), 200

@app.route("/users/<int:id_user>/favorites/planets/<int:id_planet>", methods=["POST"])
def get_planet_favorite(id_user, id_planet):
    user = User.query.get(id_user)
    planet = Planet.query.get(id_planet)
    body = json.loads(request.data)
    print(body)
    new_fav = Favorite(user_id = body["id_user"], planet_id = body["id_planet"])
    db.session.add(new_fav)
    db.session.commit()
    return jsonify("POST planet favorite method OK"), 200

@app.route("/users/<int:id_user>/favorites/characters/<int:id_character>", methods=["POST"])
def get_character_favorite(id_user, id_character):
    user = User.query.get(id_user)
    character = Character.query.get(id_character)
    body = json.loads(request.data)
    print(body)
    new_fav = Favorite(user_id = body["id_user"], character_id = body["id_character"])
    db.session.add(new_fav)
    db.session.commit()
    return jsonify("POST character favorite method OK"), 200

@app.route("/users/<int:id_user>/favorites/characters/<int:id>", methods=["DELETE"])
def delete_character_favorite(id_user, id):
    user = User.query.get(id_user)
    deleted_fav = Favorite.query.filter_by(character_id = id, user_id = id_user).delete()
    # deleted_list = list(map(lambda obj : obj.serialize(), deleted_fav))
    # print(deleted_fav, deleted_list)
    # db.session.delete(deleted_fav)
    db.session.commit()
    return jsonify("DELETE character favorite method OK"), 200

@app.route("/users/<int:id_user>/favorites/planets/<int:id>", methods=["DELETE"])
def delete_planet_favorite(id_user, id):
    user = User.query.get(id_user)
    deleted_planet_fav = Favorite.query.filter_by(planet_id = id, user_id = id_user).delete()
    # deleted_list = list(map(lambda obj : obj.serialize(), deleted_fav))
    # print(deleted_fav, deleted_list)
    # db.session.delete(deleted_fav)
    db.session.commit()
    return jsonify("DELETE planet favorite method OK"), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
