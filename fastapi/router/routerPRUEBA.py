from fastapi import APIRouter,HTTPException,status,Response, Depends
from sqlalchemy import RowMapping,Row
from db.conection import engine
from model.users import users
from schema.user_schema import User,Userschemanoid,Usernopass
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone







userprueba = APIRouter()



#? /////////////////////////////             GET            /////////////////////////////#






@userprueba.get("/usuarios")
#lista de todos los usuarios
async def get_users_lista():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()
        # Obtener los nombres de las columnas
        columns = users.columns.keys()
        # Convertir el resultado a una lista de diccionarios
        user_list = [dict(zip(columns, row)) for row in result]

        return user_list



@userprueba.get("/user/{user_id}",)#modelo sin contraseña    
#ficha de user
async def get_individual_user(user_id =int):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id==user_id)).first()
        if result is None:
            return {"error": "User not found"}
        
        columns = users.columns.keys()
        # Convertir el resultado de un elemento de una lista a diccionario
        user_list = dict(zip(columns, result))
        return user_list


    



#! /////////////////////////////////      POST       ///////////////////////////////    


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@userprueba.post("/usuarios/jwt/",status_code= status.HTTP_201_CREATED)
async def create_user_uno(user: Userschemanoid):
    with engine.connect() as conn:
        userdict = user.model_dump()#dict()  tomo el usuario y lo convierto en diccionario
        userdict["passwd"] = pwd_context.hash(user.passwd)
        print(userdict)
        conn.execute(users.insert().values(**userdict))
        conn.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED,
                         detail="usuario creado exitosamente")





#esta creacion de usuario con has "pbkdf2:sha256:30"
@userprueba.post("/usuarios/pass/",status_code= status.HTTP_201_CREATED)
async def create_user_dos(user: Userschemanoid):
    with engine.connect() as conn:
        userdict = user.model_dump()#dict()  tomo el usuario y lo convierto en diccionario
        userdict["passwd"] = generate_password_hash(user.passwd, "pbkdf2:sha256:30", 30)
        print(userdict)
        conn.execute(users.insert().values(**userdict))
        conn.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED,
                         detail="usuario creado exitosamente")






#! ///////////////////////////////////////         PUT         //////////////////////////////////////////
# version nueva con jwt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
@userprueba.put("/usuarios/{id}",)
async def update_user_uno( user_update: Userschemanoid, id=int):
    with engine.connect() as conn:
        #encripto la pass
        passwd_encrip =pwd_context.hash(user_update.passwd)
        #traigo el registro que quiero modificar 
        conn.execute(users.select().where(users.c.id==id)).first()
        #en el campo de comtraseña coloco el valor encriptado
        user_update.passwd =passwd_encrip
        #convierto todo en diccionario
        values = user_update.model_dump()
        #mando los datos a la base de datos 
        conn.execute(users.update().values(**values).where((users.c.id==id)))
        conn.commit()
    return values




#version antigua
@userprueba.put("/user/{id}",)
async def update_user_dos( user_update: Userschemanoid, id=int):
    with engine.connect() as conn:
        #encripto la pass
        passwd_encrip =generate_password_hash(user_update.passwd,"pbkdf2:sha256:30",30)
        #traigo el registro que quiero modificar 
        conn.execute(users.select().where(users.c.id==id)).first()
        #en el campo de comtraseña coloco el valor encriptado
        user_update.passwd =passwd_encrip
        #convierto todo en diccionario
        values = user_update.model_dump()
        #mando los datos a la base de datos 
        conn.execute(users.update().values(**values).where((users.c.id==id)))
        conn.commit()
    return values # me muestra los datos 
#! ///////////////////////////////////////        DELETE         //////////////////////////////////////////
@userprueba.delete("/user/{id}",)
async def delete_user(id=int):
    with engine.connect() as conn:
        # conn.execute(f"DELETE FROM users WHERE id = {id}")
        conn.execute(users.delete().where((users.c.id==id)))
        conn.commit()
    return {"mensaje":"usuario borrado"}

#! //////////////////////////////////////////// login  ////////////////////////////////////////////////////////

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_individual_user(usernameBACK: str):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id==usernameBACK)).first()
        if result is None:
            busqueda = "no esta"
            return busqueda
        
        columns = users.columns.keys()
        # Convertir el resultado de un elemento de una lista a diccionario
        user_list = dict(zip(columns, result))
        return user_list

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validar_usuario(user: Userschemanoid):
    with engine.connect() as conn:
        
        
        
        userdict = user.model_dump()#dict()  tomo el usuario y lo convierto en diccionario
        userdict["passwd"] = pwd_context.hash(user.passwd)
        print(userdict)
        conn.execute(users.insert().values(**userdict))
        conn.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED,
                         detail="usuario creado exitosamente")
    
    
@userprueba.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )


