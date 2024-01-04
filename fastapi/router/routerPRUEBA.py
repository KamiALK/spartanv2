from fastapi import APIRouter,HTTPException,status
from db.conection import engine
from model.users import users 
from schema.user_schema import User,Userschemanoid
from werkzeug.security import generate_password_hash, check_password_hash

userprueba = APIRouter()



#? /////////////////////////////             GET            /////////////////////////////#

@userprueba.get("/")
async def root():
    return {"messaje":"soy router y estoy siendo importado al main"}



#esta creacion de usuario con has "pbkdf2:sha256:30"
@userprueba.post("/usuarios/pass/",status_code= status.HTTP_201_CREATED)
async def create_user(user: Userschemanoid):
    with engine.connect() as conn:
        userdict = user.model_dump()#dict()  tomo el usuario y lo convierto en diccionario
        print(userdict)
        userdict["passwd"] = generate_password_hash(user.passwd, "pbkdf2:sha256:30", 30)
        print(userdict)
        conn.execute(users.insert().values(**userdict))
        conn.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED,
                         detail="usuario creado exitosamente")


#esta es fake CREACION SIN ID EL JSON
@userprueba.post("/usuariosfake/")
async def create_user(user: Userschemanoid):
    userdict = user.model_dump()#dict()  tomo el usuario y lo convierto en diccionario
    # userdict.pop("id", None)  # Remove id as it's auto-generated    
    conn.execute(users.insert().values(**userdict))
    conn.commit()
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




    