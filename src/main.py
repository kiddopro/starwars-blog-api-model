"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import json
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, People, FavoritesPeople
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

#variables


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# mis endpoints
@app.route('/user', methods=['GET'])
def get_users():
    all_user = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_user))
    return jsonify(all_users), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    # agarramos la respuesta del json y se la asignamos a body
    body = request.json
    # hacemos una busqueda a User por la id que se le pasa por parametro
    user = User.query.get(user_id)

    # corroboramos que se obtuvo respuesta, de lo contrario no existe un usuario con esa id
    if user is None:
        raise APIException('People not found', status_code=404)
    else:
        return jsonify(user.serialize()), 200



@app.route('/user', methods=['POST'])
def create_user():
    # request_body = request.json # decoded_request = json.loads(request_body)
    # new_user = User.registrar(request_body['email'], request_body['password'])
    # db.session.add(new_user)
    # db.session.commit()

    # obtengo lo que me mandan por json y lo agrego a la base de datos
    request_body = request.json
    is_active = request.json.get('is_active', False)
    user = User(email=request_body['email'], password=request_body['password'], is_active=is_active)
    db.session.add(user)   
    db.session.commit()

    # devuelvo la lista actualizada de usuarios

    all_user = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_user))

    return jsonify(all_users), 200

@app.route('/user/<int:id_user>', methods=['DELETE'])
def delete_user(id_user):

    # obtenemos el usuario
    user = User.query.get(id_user)

    # verificamos si se encontró un usuario con la id que viene por parametro
    if user is None:
        raise APIException('User not found', status_code=404)
    else:
        db.session.delete(user)
        db.session.commit()

    # retornamos todos los usuarios nuevamente para actualizar la lista
    all_user = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_user))

    return jsonify(all_users), 200



@app.route('/planets', methods=['GET'])
def get_planets():
    all_planet = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planet))
    return jsonify(all_planets), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    # agarramos la respuesta del json y se la asignamos a body
    body = request.json
    # hacemos una busqueda a Planets por la id que se le pasa por parametro
    planet = Planets.query.get(planet_id)

    # corroboramos que se obtuvo respuesta, de lo contrario no existe un planeta con esa id
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    else:
        return jsonify(planet.serialize()), 200

@app.route('/planets', methods=['POST'])
def post_planets():
    # obtengo lo que me mandan por json y lo agrego a la base de datos
    request_body = request.json
    planet = Planets(name=request_body['name'], picture_url=request_body['picture_url'])
    db.session.add(planet)   
    db.session.commit()

    # retorno una lista en json con los datos actualizados

    all_planet = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planet))
    return  jsonify(all_planets), 200


@app.route('/planets/<int:id_planet', methods=['DELETE'])
def delete_planet(id_planet):
    planet = Planets.query.get(id_planet)

    if planet is None:
        raise APIException('Planet not found', status_code=404)
    else:
        db.session.delete(planet)
        db.session.commit()


    all_planet = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planet))

    return jsonify(all_planets), 200


@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    all_peoples = list(map(lambda x: x.serialize(), all_people))
    return jsonify(all_peoples), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    # agarramos la respuesta del json y se la asignamos a body
    body = request.json
    # hacemos una busqueda a People por la id que se le pasa por parametro
    people = People.query.get(people_id)

    # corroboramos que se obtuvo respuesta, de lo contrario no existe un personaje con esa id
    if people is None:
        raise APIException('People not found', status_code=404)
    else:
        return jsonify(people.serialize()), 200

@app.route('/people', methods=['POST'])
def post_people():
    # obtengo lo que me mandan por json y lo agrego a la base de datos
    request_body = request.json
    people = People(name=request_body['name'], picture_url=request_body['picture_url'])
    db.session.add(people)   
    db.session.commit()

    # retorno una lista en json con los datos actualizados

    all_people = People.query.all()
    all_peoples = list(map(lambda x: x.serialize(), all_people))

    return jsonify(all_peoples), 200

@app.route('/people/<int:id_people>', methods=['DELETE'])
def delete_people(id_people):

    people = People.query.get(id_people)

    if people is None:
        raise APIException('People not found', status_code=404)
    else:
        db.session.delete(people)
        db.session.commit()


    all_people = People.query.all()
    all_peoples = list(map(lambda x: x.serialize(), all_people))

    return jsonify(all_peoples), 200

# favorites people/personajes
@app.route('/user/people', methods=['GET'])
def get_favorites_user_people():
    all_favorite = FavoritesPeople.query.all()
    all_favorites = list(map(lambda x: x.serialize(), all_favorite))
    
    return jsonify((all_favorites)), 200

@app.route('/user/people', methods=['POST'])
def post_favorites_user_people():
    # obtengo lo que me mandan por json y lo agrego a la base de datos
    request_body = request.json
    user = User.query.get(request_body['user_id'])
    people = People.query.get(request_body['people_id'])
    if user is None:
        raise APIException('User not found', status_code=404)
    elif people is None:
        raise APIException('People not found', status_code=404)
    else:
        favoritesPeople = FavoritesPeople(user_id=request_body['user_id'], people_id=request_body['people_id'])
        db.session.add(favoritesPeople)   
        db.session.commit()
        
    # retorno una lista en json con los datos actualizados

    all_fav_people = FavoritesPeople.query.all()
    all_fav_peoples = list(map(lambda x: x.serialize(), all_fav_people))

    return jsonify(all_fav_peoples), 200

@app.route('/user/people/<int:id>', methods=['DELETE'])
def del_fav_people(id):
    request_body = request.json # innecesario
    fav = FavoritesPeople.query.get(id)
    if fav is None:
        raise APIException('Identifier for FavoritesPeople is not found', status_code=404)
    else:
        db.session.delete(fav)
        db.session.commit()

    # retornamos nuevamente la lista de favoritos actualizada
    all_fav_people = FavoritesPeople.query.all()
    all_fav_peoples = list(map(lambda x: x.serialize(), all_fav_people))

    return jsonify(all_fav_peoples), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
