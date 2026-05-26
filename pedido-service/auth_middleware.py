from functools import wraps
from flask import request
import jwt

SECRET_KEY = "microservice_secret_key"


def token_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return {
                "message": "Token faltante"
            }, 401

        try:
            token = auth_header.split(" ")[1]

        except IndexError:
            return {
                "message": "Formato inválido"
            }, 401

        try:
            decoded = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

            request.user = decoded

        except jwt.ExpiredSignatureError:
            return {
                "message": "Token expirado"
            }, 401

        except jwt.InvalidTokenError:
            return {
                "message": "Token inválido"
            }, 401

        return function(*args, **kwargs)

    return decorated