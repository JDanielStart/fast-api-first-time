from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
        prefix="/users",
        tags=["users"],
        responses={404: {"message": "No encontrado"}},
    )

#Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

#Lista de usuarios
user_list = [
            User(id= 1, name="Tete", surname="Garcia", url="http://probando.com", age=25),
            User(id=2, name="Pepe", surname="Garcia", url="http://probando.com", age=25),
            User(id=3, name="Juan", surname="Garcia", url="http://probando.com", age=25),
        ] 

@router.get("/usersjson")
async def read_usersjson():
    return [
                {"id": "0", "name": "Tete", "surname": "Garcia", "url": "http://probando.com", "age": 25},
                {"id": "1", "name": "Pepe", "surname": "Garcia", "url": "http://probando.com", "age": 25},
                {"id": "2", "name": "Juan", "surname": "Garcia", "url": "http://probando.com", "age": 25}
            ]

#path
@router.get("/users")
async def read_users():
    return user_list

#path
@router.get("/user/{id}")
async def read_user(id: int):
    users = filter(lambda user: user.id == id, user_list)
    try: 
        return search_user(id)
    except:
        return {"error": "No se ha encontrado el usuario"}

#Query
@router.get("/userquery")
async def read_user(id: int):
    users = filter(lambda user: user.id == id, user_list)
    try: 
        return search_user(id)
    except:
        return {"error": "No se ha encontrado el usuario"}

@router.post("/user/", status_code=201)
async def create_user(user: User):
    existing_user = await search_user(user.id)
    if existing_user:
        raise HTTPException(status_code=409, detail="El usuario ya existe")

    user_list.routerend(user)
    return user

@router.put("/user/")
async def update_user(user: User, status_code=200):

    for index, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[index] = user
            return user

    raise HTTPException(status_code=404, detail="El usuario no existe")

@router.delete("/user/{id}", status_code=200)
async def delete_user(id: int):
    for index, user in enumerate(user_list):
        if user.id == id:
            return user_list.pop(index)

    raise HTTPException(status_code=404, detail="El usuario no existe")

async def search_user(id: int):
    global user_list
    users = filter(lambda user: user.id == id, user_list)
    user_list_filtered = list(users)
    return user_list_filtered[0] if user_list_filtered else None

#Crear el entorno de desarrollo si no existe python -m venv venv
#Activar el entorno de desarrollo en window .\venv\Scripts\activate
#Activar el entorno de desarrollo en linux source venv/bin/activate

#Iniciar el server: uvicorn users:router --reload
#Detener el server: Ctrl + C

#Documentación con Swagger http://127.0.0.1:8000/docs
#Documentación con Redocly http://127.0.0.1:8000/redoc