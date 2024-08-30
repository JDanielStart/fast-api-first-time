from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str
    
users_db = {
    "daniel": {
        "username": "Daniel",
        "full_name": "González Alemán",
        "email": "daniel@prueba.com",
        "disabled": False,
        "password": "1234"
    },
    "daniel2": {
        "username": "Daniel2",
        "full_name": "González Alemán2",
        "email": "daniel2@prueba.com",
        "disabled": True,
        "password": "1234"
    },
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def get_current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credeciales inválidas",
                headers={"WWW-Authenticate": "Bearer"})

    if user.disabled:
        raise HTTPException(
            status_code=400,
            detail="Usuario deshabilitado")


    return user

@router.post("/loginbasic")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    
    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    return {"access_token": user.username, "token_type": "bearer"}

@router.get("/usersbasic/me")
async def read_users_me(user: User = Depends(get_current_user)):
    return user
