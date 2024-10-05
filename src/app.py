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
from models import db, User, Equipo
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

@app.route('/user', methods=['GET'])
def handle_hello():
    print('debugueando')
    all_users = User.query.all()
    print(all_users)
    results = list(map(lambda usuario: usuario.serialize(),all_users)) 
    print(results)
    

    response_body = {
        "msg": "Hello, this is your GET /user response 123 "
    }

    return jsonify(results), 200


@app.route('/equipo', methods=['GET'])
def get_teams():
    all_teams = Equipo.query.all()    
    results = list(map(lambda team: team.serialize(),all_teams)) 

    return jsonify(results), 200

@app.route('/equipo/<int:team_id>', methods=['GET'])
def get_team(team_id):
    print(team_id)
    team = Equipo.query.filter_by(id=team_id).first()
    print(team)   
    db.session.delete(team)
    db.session.commit()

    return jsonify(team.serialize()), 200

@app.route('/equipo', methods=['POST'])
def add_team():
    print('POST equipo')
    # leer datos del body del request
    print(request)
    print(request.get_json())
    print(request.get_json()['nombre'])
    body = request.get_json()
    # guardar un equipo en la BD
    team = Equipo(nombre = body['nombre'],color = body['color'],estadios = body['estadios'])
    # team = Equipo(**body)
    db.session.add(team)
    db.session.commit()

    response_body = {
        "msg": "Se creo el equipo",
        
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
