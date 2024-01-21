from sqlalchemy.orm import session
from schema.user_schema import User, Userschemanoid
from passlib.context import CryptContext


SECRET_KEY ="a2e2da9015817e03d78da769dca6b13bad1196ca632f2584a9fb13473ac0d35a"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



# person =User(1,"andresito","andres","almanza",3143513617,31,1024,"M","andy@ffg",123)

# def get_users(db:session):
#     return db.query(User).all()

def get_user(db:session):
    return db.query(User).filter(User.id==id).first()

def get_user_by_name(db:session,name:str):
    return db.query(User).filter(User.name==name).first()

def create_user(db:session,user:User):
    #aqui va la contraseña
    passwordhash =  pwd_context.hash(user.passwd)
    new_user=User(name=user.name,password=passwordhash)
    db.add(new_user)
    db.commit()
    db.flush(new_user)
    return new_user
    
   
    print( person.create_user())