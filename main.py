from fastapi import FastAPI
from routers import users, products, jwt_auth_users, basic_auth_users, users_db
from fastapi.staticfiles import StaticFiles
from typing import Union

app = FastAPI()

#Rutas
app.include_router(users.router)
app.include_router(products.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"Hello": "World"}

#Crear el entorno de desarrollo si no existe python -m venv venv
#Activar el entorno de desarrollo en window .\venv\Scripts\activate
#Activar el entorno de desarrollo en linux source venv/bin/activate

#Iniciar el server: uvicorn main:app --reload
#Detener el server: Ctrl + C

#Documentación con Swagger http://127.0.0.1:8000/docs
#Documentación con Redocly http://127.0.0.1:8000/redoc