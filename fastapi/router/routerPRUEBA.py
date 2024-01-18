from fastapi import APIRouter,HTTPException,status,Response, Depends
from sqlalchemy import RowMapping,Row
from db.conection import engine
from model.users import users
from schema.user_schema import User,Userschemanoid,Usernopass,Token,TokenData

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
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},)
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
        if  userdb["passwd"]== password:
            print(userdb["passwd"])
            return userdb
        else: {"messaje":"password incorrect"}
    else:{"mesaje":"login o password incorrect"}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt





@userprueba.post("/login")
async def login(form:OAuth2PasswordRequestForm= Depends()) -> Token:
    #getuser lo obtengo de la funcion para traer mi funcion de base de datos 
    with engine.connect() as conn:
        userdb=get_individual_user(form.username)
        sin_hash =verify_password(form.password, userdb["passwd"])
        if  not sin_hash :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="contraseña incorrecta")
        # if userdb["username"] == form.username:#no hace nada
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
        data={"sub": userdb["username"]}, expires_delta=access_token_expires)

        return Token(access_token=access_token, token_type="bearer")    
    
async def get_current_user(token: Annotated[str, Depends(oauth2)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_individual_user(token_data.username)
    if user is None:
        raise credentials_exception
   
    return user



async def get_current_active_user(current_user: Annotated[Usernopass, Depends(get_current_user)]):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@userprueba.get("/me", response_model=Usernopass)
async def read_users_me(current_user: Annotated[Usernopass, Depends(get_current_active_user)]
):
    return current_user
