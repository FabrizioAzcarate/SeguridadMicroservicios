import jwt
import datetime

SECRET_KEY = "microservice_secret_key"


def create_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    return token


def verify_token(token):
    try:
        decoded = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        return decoded

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None