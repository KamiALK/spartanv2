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
SECRET_KEY ="a2e2da9015817e03d78da769dca6b13bad1196ca632f2584a9fb13473ac0d35a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


userprueba = APIRouter()



#? /////////////////////////////             GET            /////////////////////////////
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
#! /////////////////////////////////         POST           ///////////////////////////////    
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
#? /////////////////////////////             PUT             ///////////////////////////////
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
#! ////////////////////////////              DELETE           ////////////////////////////////
@userprueba.delete("/user/{id}",)
async def delete_user(id=int):
    with engine.connect() as conn:
        # conn.execute(f"DELETE FROM users WHERE id = {id}")
        conn.execute(users.delete().where((users.c.id==id)))
        conn.commit()
    return {"mensaje":"usuario borrado"}
#* ////////////////////////////              LOGIN          /////////////////////////////////
def get_individual_user(usernameBACK: str ):
    #funcion 1
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.username==usernameBACK)).first()
        if result is None:
            busqueda = "no esta"
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="usuario no encontrado")
        else: result
        
        columns = users.columns.keys()
        # Convertir el resultado de un elemento de una lista a diccionario
        user_db = dict(zip(columns, result))
        return user_db
def validar_usuario(username:str, password:str):
    #getuser lo obtengo de la funcion para traer mi funcion de base de datos 
    with engine.connect() as conn:
        userdb=get_individual_user(username)
        
        hash_pass= userdb["passwd"]
    if userdb["username"]==username:
        print(userdb["username"])
        if  userdb["passwd"]== hash_pass:
            print(userdb["passwd"])
            return userdb
        else: {"messaje":"password incorrect"}
    else:{"mesaje":"login o password incorrect"}



@userprueba.post("/login")
async def login(form:OAuth2PasswordRequestForm= Depends()):
    #getuser lo obtengo de la funcion para traer mi funcion de base de datos 
    with engine.connect() as conn:
        userdb=get_individual_user(form.username)
        
        hash_pass= pwd_context.hash(form.password)
    if userdb["username"]==form.username:
        print(userdb["username"])
        print(hash_pass)
        if  userdb["passwd"]== hash_pass:
            print(userdb["passwd"])
            return userdb
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="contraseña incorrecta")
  
    else: HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="usuario incorrecto ")








        
   # @userprueba.post("/login")
# async def login(form:OAuth2PasswordRequestForm= Depends()):
#     userdb= validar_usuario(form.username,form.password)
#     print(userdb)
#     if not userdb:    
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="credenciales incorrectas")
#     user =get_individual_user(form.username)
#     return{"access_token":user.username,"token_type":"bearer"} 

# async def current_user(token: str=Depends(oauth2)):
#     user = get_individual_user(token)
#     if not user:
        # return user

# @userprueba.get("/user/me")
# async def me(user:User=Depends(current_user)):
#     return user 
        


