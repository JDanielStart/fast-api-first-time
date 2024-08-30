from fastapi import APIRouter, HTTPException, status
from db.models.users import User
from db.schemas.users import user_schema, users_schema
from db.client import db_client
from bson import ObjectId

router = APIRouter(
    prefix="/usersdb",
    tags=["usersdb"],
    responses={status.HTTP_404_NOT_FOUND: {"message": "No encontrado"}},
)

# Ruta para obtener todos los usuarios
@router.get("/", response_model=list[User])
async def read_users():
    users = db_client.users.find()
    return users_schema(users)

# Ruta para obtener un usuario por ID
@router.get("/{id}", response_model=User)
async def read_user(id: str):
    user = await search_user("_id", ObjectId(id))
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha encontrado el usuario")

# Ruta para crear un nuevo usuario
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    existing_user = await search_user("email", user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está en uso")

    user_dict = user.dict()
    del user_dict["id"]
    
    id = db_client.users.insert_one(user_dict).inserted_id

    new_user = db_client.users.find_one({"_id": id})
    new_user = user_schema(new_user)

    return User(**new_user)

# Ruta para actualizar un usuario
@router.put("/", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(user: User):
    user_dict = user.dict()
    del user_dict["id"]

    result = db_client.users.update_one(
        {"_id": ObjectId(user.id)}, {"$set": user_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe")

    return await search_user("_id", ObjectId(user.id))

# Ruta para eliminar un usuario
@router.delete("/{id}", response_model=User, status_code=status.HTTP_200_OK)
async def delete_user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})

    if found:
        return User(**user_schema(found))

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="El usuario no existe")

# Función para buscar un usuario por un campo específico
async def search_user(field: str, key):
    user = db_client.users.find_one({field: key})
    if user:
        return User(**user_schema(user))
    return None

# Crear el entorno de desarrollo si no existe python -m venv venv
# Activar el entorno de desarrollo en window .\venv\Scripts\activate
# Activar el entorno de desarrollo en linux source venv/bin/activate

# Iniciar el server: uvicorn users:router --reload
# Detener el server: Ctrl + C

# Documentación con Swagger http://127.0.0.1:8000/docs
# Documentación con Redocly http://127.0.0.1:8000/redoc