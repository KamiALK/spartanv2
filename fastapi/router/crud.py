from sqlalchemy.orm import session
from schema.user_schema import UserID, TokenData,Token,Usernopass,UserData
from passlib.context import CryptContext
# from db.conection import Userdb
from model.Userdb import Userdb
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends,  HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError 
import jwt
from passlib.context import CryptContext
from typing import Optional
from fastapi import Cookie




SECRET_KEY = "a2e2da9015817e03d78da769dca6b13bad1196ca632f2584a9fb13473ac0d35a"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_users(db):
    
    return db.query(Userdb).all()


def get_user_by_username(db, username: str)->UserID:
    user:UserID = db.query(Userdb).filter(Userdb.email == username).first()
    return user
    

def get_user_by_id(db, id: int):
    user = db.query(Userdb).filter(Userdb.ID == id).first()
    return user
def get_user_by_cedula(db, cedula: int):
    user = db.query(Userdb).filter(Userdb.cedula == cedula).first()

def create_user(db, user: UserID):
    # Hash the password before storing it in the database
    user.passwd = pwd_context.hash(user.passwd)

    # Check if a user with the same cedula already exists
    existing_user = get_user_by_cedula(db=db, cedula=user.cedula)
    if existing_user:
        return None  # User already exists
    id=None
    new_user =Userdb(ID=id,username=user.username, nombre=user.nombre, apellido=user.apellido, celular=user.celular,
                      edad=user.edad, cedula=user.cedula, genero=user.genero, email=user.email, passwd=user.passwd)
    
    db.add(new_user)
    db.commit()
    db.flush(new_user)
    
    return new_user

#!? ///////////////////////////////// PRUEBA DE MODIFICACIONES //////////////////////////////////////////
def get_user_by_cedula(db, cedula: int, user_type: str):
    # Construye dinámicamente el nombre de la clase según el tipo de usuario seleccionado
    user_class = globals()[f"{user_type.capitalize()}db"]
    user = db.query(user_class).filter(user_class.cedula == cedula).first()
    return user
# Modifica la función create_user para recibir el tipo de usuario como parámetro
def create_user(db, user: UserID, user_type: str):
    # Hash the password before storing it in the database
    user.passwd = pwd_context.hash(user.passwd)

    # Check if a user with the same cedula already exists
    existing_user = get_user_by_cedula(db=db, cedula=user.cedula, user_type=user_type)
    if existing_user:
        return None  # User already exists
    id=None
    # Construye dinámicamente el nombre de la clase según el tipo de usuario seleccionado
    user_class = globals()[f"{user_type.capitalize()}db"]
    new_user = user_class(ID=id, username=user.username, nombre=user.nombre, apellido=user.apellido, celular=user.celular,
                          edad=user.edad, cedula=user.cedula, genero=user.genero, email=user.email, passwd=user.passwd)
    
    db.add(new_user)
    db.commit()
    db.flush(new_user)
    
    return new_user

# Modifica la función get_user_by_cedula para recibir el tipo de usuario como parámetro



#!   /////////////////////////////////////////////////////////////

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user1(db, username: str):
    if username in db:
        user_dict = db[username]
        return Usernopass(**user_dict)


def authenticate_user( db,username: str, password: str,)->UserID:
    # user = get_user(fake_db, username)
    user:UserID = get_user_by_username(db=db,username=username)
    if not user:
        return False
    if not verify_password(password, user.passwd):
        return False
    return user


def create_access_token(db,data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def login_for_access_token(db, form_data: Annotated[OAuth2PasswordRequestForm, Depends()])->UserData:
    user:UserData = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        db, data={
            "sub": user.username,
            "nombre": user.nombre,
            "apellido": user.apellido,
            "email":user.email,
            "username":user.username,
                  
                  }, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




def get_current_user(token: Optional[str] = Cookie(None)):
    credentials_exception = HTTPException(
        
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        if token is None:
            raise credentials_exception
        
        # Aquí decodificas el token de la cookie y obtienes la información del usuario
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        user_info = {
            "username": username,
            "nombre": payload.get("nombre"),
            "apellido": payload.get("apellido"),
            "email": payload.get("email"),
            "username": payload.get("username"),
            
        }
        return user_info
    
    except JWTError:
        raise credentials_exception


def read_users_me(db: session,
    current_user: Annotated[Userdb, Depends(get_current_user)]
):
    return current_user



def read_own_items(db: session,
    current_user: Annotated[Userdb, Depends(get_current_user)]
):
    return [{"item_id": "Foo", "owner": current_user.username}]

from typing import Dict

def get_current_active_user(db: session,
    current_user: Annotated[Usernopass, Depends(get_current_user)]
):

    return current_user