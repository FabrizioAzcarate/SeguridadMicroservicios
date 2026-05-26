from flask import Flask, request
from flask_restx import Api, Resource, fields
from auth_middleware import token_required
import requests

app = Flask(__name__)

api = Api(
    app,
    title="Pedido Service",
    version="1.0",
    description="Microservicio de pedidos protegido con JWT"
)

ns = api.namespace("orders", description="Operaciones de pedidos")

orders = [
    {"id": 1, "user_id": 1, "product": "Notebook"},
    {"id": 2, "user_id": 2, "product": "Mouse"}
]

order_model = api.model(
    "Order",
    {
        "id": fields.Integer(required=True),
        "user_id": fields.Integer(required=True),
        "product": fields.String(required=True)
    }
)

USER_SERVICE_URL = "http://usuario_service:5000/users"


@ns.route("/")
class OrderList(Resource):

    @token_required
    def get(self):
        return orders, 200

    @token_required
    @ns.expect(order_model)
    def post(self):
        data = request.get_json()

        user_id = data["user_id"]

        auth_header = request.headers.get("Authorization")

        response = requests.get(
            f"{USER_SERVICE_URL}/{user_id}",
            headers={
                "Authorization": auth_header
            }
        )

        if response.status_code != 200:
            return {
                "message": "Usuario no existe"
            }, 404

        new_order = {
            "id": data["id"],
            "user_id": user_id,
            "product": data["product"]
        }

        orders.append(new_order)

        return {
            "message": "Pedido creado",
            "order": new_order
        }, 201


@ns.route("/<int:order_id>")
class OrderById(Resource):

    @token_required
    def get(self, order_id):
        for order in orders:
            if order["id"] == order_id:
                return order, 200

        return {
            "message": "Pedido no encontrado"
        }, 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)