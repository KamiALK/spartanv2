from fastapi import APIRouter
from db.conection import conn
from model.users import users 
from schema.user_schema import User,Usernoid
from werkzeug.security import generate_password_hash, check_password_hash

userprueba = APIRouter()



@userprueba.get("/")
async def root():
    return {"messaje":"soy router y estoy siendo importado al main"}



#esta es fake
@userprueba.post("/usuariosfake/")
async def create_user(user: Usernoid):
    

    userdict = user.model_dump()#dict() funciona igual
    # userdict.pop("id", None)  # Remove id as it's auto-generated
    conn.execute(users.insert().values(**userdict))
    conn.commit()
   
    
    print(user)
    print(userdict)

    return {"message": "User created successfully."}












@userprueba.post("/usuarios/")
async def create_user(user: User):
    

    userdict = user.model_dump()#dict() funciona igual
    userdict.pop("id", None)  # Remove id as it's auto-generated
    conn.execute(users.insert().values(**userdict))
    conn.commit()
   
    
    print(user)
    print(userdict)

    return {"message": "User created successfully."}




    