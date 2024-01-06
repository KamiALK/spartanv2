from fastapi import APIRouter,HTTPException,status,Response
from sqlalchemy import RowMapping,Row
from db.conection import engine
from model.users import users, query
from schema.user_schema import User,Userschemanoid,Usernopass
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List


userprueba = APIRouter()



#? /////////////////////////////             GET            /////////////////////////////#

@userprueba.get("/")
async def root():
    return {"messaje":"soy router y estoy siendo importado al main"}




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
    
@userprueba.get("/user/{user_id}",response_model=Usernopass)#modelo sin contraseña
#ficha de user
async def get_individual_user(user_id =int):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id==user_id)).first()
        columns = users.columns.keys()
        # Convertir el resultado de un elemento de una lista a diccionario
        user_list = dict(zip(columns, result)) 
        return user_list


#! /////////////////////////////////      POST       ///////////////////////////////    
#esta creacion de usuario con has "pbkdf2:sha256:30"
@userprueba.post("/usuarios/pass/",status_code= status.HTTP_201_CREATED)
async def create_user(user: Userschemanoid):
    with engine.connect() as conn:
        userdict = user.model_dump()#dict()  tomo el usuario y lo convierto en diccionario
        userdict["passwd"] = generate_password_hash(user.passwd, "pbkdf2:sha256:30", 30)
        print(userdict)
        conn.execute(users.insert().values(**userdict))
        conn.commit()
    return HTTPException(status_code=status.HTTP_201_CREATED,
                         detail="usuario creado exitosamente")

#esta es fake CREACION SIN ID EN EL JSON
@userprueba.post("/usuariosfake/")
async def create_user(user: Userschemanoid):
    with engine.connect() as conn:
        userdict = user.model_dump()#dict()  tomo el usuario y lo convierto en diccionario
        # userdict.pop("id", None)  # Remove id as it's auto-generated    
        conn.execute(users.insert().values(**userdict))
        conn.commit()
        print(userdict)
    return {"message": "User created successfully."}


#! ///////////////////////////////////////         PUT         //////////////////////////////////////////
@userprueba.delete("/user/{id}",)
async def delete_user(id=int):
    with engine.connect() as conn:
        # conn.execute(f"DELETE FROM users WHERE id = {id}")
        conn.execute(users.delete().where((users.c.id==id)))
        conn.commit()
    return {"mensaje":"usuario borrado"}

@userprueba.put("/user/{id}",)
async def update_user( user_update: Userschemanoid, id=int):
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
    return values #me muestra los datos 
