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
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

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

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret esto lo debo actualizar"  # Change this!
jwt = JWTManager(app)
# perro ===== perroa. , montaña === montañaa
# perro ===== peperropo. , montaña === monpotapañapa
# perro ===== asdfasfasdfasdfasdfasdf. , montaña === 12kj3412j3h4kj12h3k4j2hk

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
@jwt_required()
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

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"msg": "No se encontro ese usuario"}), 401
    print(user)
    print(user.email)
    if password != user.password:
        return jsonify({"msg": "La clave es incorrecta"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
