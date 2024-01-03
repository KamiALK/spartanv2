from fastapi import APIRouter
from config.db.conection import conn, engine,Meta_Data
from model.users import users
from schema.user_schema import UserSchema,User


userprueba = APIRouter()



@userprueba.get("/")
async def root():
    return {"messaje":"soy router y estoy siendo importado al main"}









@userprueba.post("/usuarios/")
async def create_user(user: User):
    

    userdict = user.dict()
    userdict.pop("id", None)  # Remove id as it's auto-generated
    conn.execute(users.insert().values(**userdict))
    conn.commit()
   
    
    print(user)
    print(userdict)

    return {"message": "User created successfully."}


    