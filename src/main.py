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
from models import db, User, Planets, People
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

@app.route('/user/<int:user_id>')
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

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planet = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planet))
    return jsonify(all_planets), 200

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

@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    all_peoples = list(map(lambda x: x.serialize(), all_people))
    return jsonify(all_peoples), 200

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

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
