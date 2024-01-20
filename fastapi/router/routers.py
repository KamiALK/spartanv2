from fastapi import FastAPI,Depends,HTTPException,APIRouter
from sqlalchemy.orm import session
# import crud
from db.conection import engine,LocalSession
from schema.user_schema import Userschemanoid
from model.users import Base


#si no estan creadas nuestras tablas vamos a crearlas 
# Base.MetaData.create_all(bing=engine)

#instanciamos
app =APIRouter()

def get_db():
    db =LocalSession()
    try:
        yield db
    finally:
        db.close()
        

@app.get("/")
async def root():
    return {"messaje":"hola soy root"}
