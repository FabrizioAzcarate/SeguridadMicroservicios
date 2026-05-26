from flask import Flask, request
from flask_restx import Api, Resource, fields
from auth_middleware import token_required

app = Flask(__name__)

api = Api(
    app,
    title="Usuario Service",
    version="1.0",
    description="Microservicio de usuarios protegido con JWT"
)

ns = api.namespace("users", description="Operaciones de usuarios")

users = [
    {"id": 1, "name": "Juan"},
    {"id": 2, "name": "Ana"}
]

user_model = api.model(
    "User",
    {
        "id": fields.Integer(required=True),
        "name": fields.String(required=True)
    }
)


@ns.route("/")
class UserList(Resource):

    @token_required
    def get(self):
        return users, 200

    @token_required
    @ns.expect(user_model)
    def post(self):
        data = request.get_json()

        new_user = {
            "id": data["id"],
            "name": data["name"]
        }

        users.append(new_user)

        return {
            "message": "Usuario creado",
            "user": new_user
        }, 201


@ns.route("/<int:user_id>")
class UserById(Resource):

    @token_required
    def get(self, user_id):
        for user in users:
            if user["id"] == user_id:
                return user, 200

        return {"message": "Usuario no encontrado"}, 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)