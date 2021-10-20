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
users = [
    
        {
            "id": 1,
            "first_name": "Bob",
            "last_name": "Dylan",
            "email": "bob@dylan.com",
            "password": "asdasdasd"
        }
    
]

# planets = [

#     {
#         "id": 1,
#         "name": "Earth",
#         "picture_url": None
#     }
# ]

people = [
    {
        "id": 1,
        "name" : "Yoda",
        "picture_url" : None
    }
]

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

@app.route('/user', methods=['POST'])
def create_user():
    request_body = request.json # decoded_request = json.loads(request_body)
    new_user = User.registrar(request_body['email'], request_body['password'])
    db.session.add(new_user)
    db.session.commit()
    # users.append(decoded_request)
    # response_body = {
    #     "msg": "User added successfully"
    # }
    return jsonify(request_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planet = Planets.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planet))
    return jsonify(all_planets), 200

@app.route('/planets', methods=['POST'])
def post_planets():
    request_body = request.data
    decoded_request = json.loads(request_body)
    planets.append(decoded_request)
    request_body = {
        "msg": "Planet added successfully"
    }
    return  jsonify(request_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    all_peoples = list(map(lambda x: x.serialize(), all_people))
    return jsonify(all_peoples), 200

@app.route('/people', methods=['POST'])
def post_people():
    request_body = request.data
    decoded_request = json.loads(request_body)
    people.append(decoded_request)
    response_body = {
        "msg": "People added successfully"
    }
    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
