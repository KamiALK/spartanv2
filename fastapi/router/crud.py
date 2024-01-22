from sqlalchemy.orm import session
from schema.user_schema import UserData
from passlib.context import CryptContext
from db.conection import Userdb


SECRET_KEY = "a2e2da9015817e03d78da769dca6b13bad1196ca632f2584a9fb13473ac0d35a"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# person =User(1,"andresito","andres","almanza",3143513617,31,1024,"M","andy@ffg",123)

def get_users(db:session):
    return db.query(Userdb).all()


def get_user_by_cedula(db: session, cedula: int):
    user = db.query(Userdb).filter(Userdb.cedula == cedula).first()
    
      
    return user
    

def get_user_by_id(db: session, id: int):
    user = db.query(Userdb).filter(Userdb.ID == id).first()
    return user

def create_user(db: session, user: UserData):
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