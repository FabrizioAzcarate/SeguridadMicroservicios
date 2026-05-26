from flask import Flask, request
from flask_restx import Api, Resource, fields
from auth import create_token

app = Flask(__name__)

api = Api(
    app,
    title="Auth Service",
    version="1.0",
    description="Microservicio de autenticación JWT"
)

ns = api.namespace("auth", description="Operaciones de autenticación")

users = {}

# Modelo para Swagger
user_model = api.model(
    "User",
    {
        "username": fields.String(required=True, description="Nombre de usuario"),
        "password": fields.String(required=True, description="Contraseña")
    }
)


@ns.route("/create-user")
class CreateUser(Resource):

    @ns.expect(user_model)
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"message": "Faltan datos"}, 400

        if username in users:
            return {"message": "Usuario ya existe"}, 400

        users[username] = password

        return {"message": "Usuario creado correctamente"}, 201


@ns.route("/login")
class Login(Resource):

    @ns.expect(user_model)
    def post(self):
        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if username not in users:
            return {"message": "Usuario no encontrado"}, 404

        if users[username] != password:
            return {"message": "Contraseña incorrecta"}, 401

        token = create_token(username)

        return {"token": token}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)