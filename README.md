# Proyecto Microservicios con Autenticación JWT

Aplicación desarrollada en Python usando Flask y Docker, basada en arquitectura de microservicios.

El sistema implementa autenticación con JWT para proteger endpoints y comunicación entre servicios.

---

# Tecnologías utilizadas

- Python
- Flask
- Flask-RESTX
- JWT (PyJWT)
- Requests
- Docker
- Docker Compose
- Swagger/OpenAPI
- APIs REST

---

# Microservicios

## Auth Service

Puerto: 5002

Gestiona:
- Crear usuario
- Login
- Generar token JWT

Endpoints:
- POST /auth/create-user
- POST /auth/login

Swagger:
http://localhost:5002/

---

## Usuario Service

Puerto: 5000

Protegido por JWT.

Gestiona:
- Obtener usuarios
- Buscar usuario por ID
- Crear usuario

Endpoints:
- GET /users/
- GET /users/<id>
- POST /users/

Swagger:
http://localhost:5000/

---

## Pedido Service

Puerto: 5001

Protegido por JWT.

Gestiona:
- Obtener pedidos
- Buscar pedido por ID
- Crear pedido

Valida existencia del usuario consultando `usuario_service`.

Endpoints:
- GET /orders/
- GET /orders/<id>
- POST /orders/

Swagger:
http://localhost:5001/

---

# Ejecución con Docker

Ubicarse en la carpeta raíz:

```bash
cd microservicios
