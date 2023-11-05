"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, People, Starships, Favorites
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.url_map.strict_slashes = False
bcrypt = Bcrypt(app)

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

@app.route('/users', methods=['GET'])
def obtener_usuarios():
    usuarios = User.query.all()
    usuarios_serializados = list(map(lambda item: item.serialize(), usuarios))
    if len(usuarios) < 1:
        raise APIException("No existen usuarios en la BBDD", status_code=404)
    return jsonify(usuarios_serializados), 200

@app.route('/users', methods=['POST'])
def agregar_usuario():
    nuevo_usuario = request.json
    username = nuevo_usuario.get('username')
    email = nuevo_usuario.get('email')
    password = nuevo_usuario.get('password')
    secure_password = bcrypt.generate_password_hash(
            password, 10).decode("utf-8")
    if not username or not email or not password:
        raise APIException("Faltan campos obligatorios en la solicitud", status_code=400)
    usuario = User(username=username, email=email, password=secure_password)
    db.session.add(usuario)
    db.session.commit()

    return jsonify({"message":f"Se añadió correctamente el usuario: {username} en la BBDD"}), 201


@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()
        return jsonify(users=[users.serialize() for users in users])
    except Exception as e:
        return jsonify({"Error al traer todos los usuarios " + str(e)}), 500


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if user is not None:
            return jsonify(user.serialize()), 200
        else:
            return jsonify({"mensaje": "El usuario no existe"}), 404 
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    try:
        user = User.query.get(user_id)
        if user is not None:
            return User.serializeFavorite(user)
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/planets', methods=['POST'])
def create_planet():
    nuevo_planeta = request.json
    name = nuevo_planeta.get('name')
    diameter = nuevo_planeta.get('diameter')
    rotation_period = nuevo_planeta.get('rotation_period')
    orbital_period = nuevo_planeta.get('orbital_period')
    gravity = nuevo_planeta.get('gravity')
    population = nuevo_planeta.get('population')
    climate = nuevo_planeta.get('climate')
    terrain = nuevo_planeta.get('terrain')
    surface_water = nuevo_planeta.get('surface_water')
    
    planeta = Planets(name=name, diameter=diameter, rotation_period=rotation_period, orbital_period=orbital_period, gravity=gravity, population=population, climate=climate, surface_water=surface_water, terrain=terrain)
    db.session.add(planeta)
    db.session.commit()

    return jsonify({"message":f"Se añadió correctamente el planeta: {name} en la BBDD"}), 201   
    
    
@app.route('/planets', methods=['GET'])
def get_all_planets():
    try:
        planets = Planets.query.all()
        if planets is not None:
            return jsonify(planets=[planets.serialize() for planets in planets])
        else:
            return jsonify({"No existen planetas"})
    except Exception as e: 
        return jsonify({"error": str(e)})
    
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    try:
        planet=Planets.query.get(planet_id)
        if planet is not None:
            return jsonify(planet.serialize()),200
        else:
            return jsonify({"msg":"el Planeta no existe"})
        
    except Exception as e:
        return jsonify({"error": str(e)})
    
        
@app.route('/people', methods=['POST'])
def create_people():
    new_people = request.json
    name = new_people.get('name')
    height = new_people.get('height')
    hair_color = new_people.get('hair_color')
    skin_color = new_people.get('skin_color')
    eye_color = new_people.get('eye_color')
    birth_year = new_people.get('birth_year')
    gender = new_people.get('gender')
    homeworld = new_people.get('homeworld')
    people = People(name=name, height=height, hair_color=hair_color, skin_color=skin_color, eye_color=eye_color, birth_year=birth_year, gender=gender, homeworld=homeworld)
    db.session.add(people)
    db.session.commit()

    return jsonify({"message":f"Se añadió correctamente people: {name} en la BBDD"}), 201   
    
@app.route('/people', methods=['GET'])
def get_all_peoples():
    try:
        peoples = People.query.all()
        return jsonify(peoples=[peoples.serialize() for peoples in peoples])
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    try:
        people = People.query.get(people_id)
        if people is not None:
            return jsonify(people.serialize()), 200
        else:
            return jsonify({"msg": "people_id not found"})
        
    except Exception as e:
        return jsonify({"error": str(e)})
    

@app.route('/starship', methods=['POST'])
def create_starship():
    new_starship = request.json
    name = new_starship.get('name')
    model = new_starship.get('model')
    starship_class = new_starship.get('starship_class')
    manufacter = new_starship.get('manufacter')
    cost_in_credits = new_starship.get('cost_in_credits')
    length = new_starship.get('length')
    consumables = new_starship.get('consumables')
    passengers = new_starship.get('passengers')
    
    starship = Starships(name=name, model=model, starship_class=starship_class, manufacter=manufacter, cost_in_credits=cost_in_credits, length=length, passengers=passengers, consumables=consumables)
    db.session.add(starship)
    db.session.commit()
    
    return jsonify({"msg": f"se añadió correctamente la nave: {name} en la BBDD"}), 201

@app.route('/starships', methods=['GET'])
def get_all_starships():
    try:
        starships = Starships.query.all()
        if starships is not None:
            return jsonify(starships=[starships.serialize() for starships in starships])
        else:
            return jsonify({"msg": "No starships were found"}), 404
    except Exception as e:
        return jsonify({"msg": str(e)})
        

@app.route('/starship/<int:starship_id>', methods=['GET'])
def get_starship_id(starship_id):
    try:
        starship = Starships.query.get(starship_id)
        if starship is not None:
            return jsonify(starship.serialize()), 200
        else:
            return jsonify({"msg": "starship not found"})
    except Exception as e:
        return jsonify({"err": str(e)})


@app.route("/favorite/planet/<int:user_id>/<int:planet_id>", methods=["POST"])
def add_favorite_planet(user_id, planet_id):
    try:
        user = User.query.get(user_id)
        planet = Planets.query.get(planet_id)
        
        if user is None:
            return jsonify({"mensaje": "El usuario no existe"}), 404

        if planet is None:
            return jsonify({"mensaje": "El planeta no existe"}), 404

        # Comprueba si el planeta ya está en la lista de favoritos del usuario
        existing_favorite = Favorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        
        if existing_favorite:
            return jsonify({"mensaje": "El planeta ya está en la lista de favoritos del usuario"}), 200

        # Crea una nueva relación de favoritos entre el usuario y el planeta
        new_favorite = Favorites(user_id=user_id, planet_id=planet_id)
        db.session.add(new_favorite)
        db.session.commit()
        
        return jsonify({"mensaje": f"El planeta {planet.name} se ha añadido a la lista de favoritos del usuario"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/favorite/people/<int:user_id>/<int:people_id>", methods=["POST"])
def add_favorite_people(user_id, people_id):
    try:
        user = User.query.get(user_id)
        people = People.query.get(people_id)
        
        if user is None:
            return jsonify({"mensaje": "El usuario no existe"}), 404

        if people is None:
            return jsonify({"mensaje": "El people no existe"}), 404

        # Comprueba si el planeta ya está en la lista de favoritos del usuario
        existing_favorite = Favorites.query.filter_by(user_id=user_id, people_id=people_id).first()
        
        if existing_favorite:
            return jsonify({"mensaje": "El People ya está en la lista de favoritos del usuario"}), 200

        # Crea una nueva relación de favoritos entre el usuario y el planeta
        new_favorite = Favorites(user_id=user_id, people_id=people_id)
        db.session.add(new_favorite)
        db.session.commit()
        
        return jsonify({"mensaje": f"El People {people.name} se ha añadido a la lista de favoritos del usuario"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/favorite/starship/<int:user_id>/<int:starship_id>", methods=["POST"])
def add_favorite_starship(user_id, starship_id):
    try:
        user = User.query.get(user_id)
        starship = Starships.query.get(starship_id)
        
        if user is None:
            return jsonify({"mensaje": "El usuario no existe"}), 404

        if starship is None:
            return jsonify({"mensaje": "El starship no existe"}), 404

        # Comprueba si el planeta ya está en la lista de favoritos del usuario
        existing_favorite = Favorites.query.filter_by(user_id=user_id, starship_id=starship_id).first()
        
        if existing_favorite:
            return jsonify({"mensaje": "El starship ya está en la lista de favoritos del usuario"}), 200

        # Crea una nueva relación de favoritos entre el usuario y el planeta
        new_favorite = Favorites(user_id=user_id, starship_id=starship_id)
        db.session.add(new_favorite)
        db.session.commit()
        
        return jsonify({"mensaje": f"El starship {starship.name} se ha añadido a la lista de favoritos del usuario"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
