from fastapi import  Depends, HTTPException, APIRouter
from sqlalchemy.orm import session
# import crud
from db.conection import engine, Session, Userdb
from schema.user_schema import Userschemanoid



# instanciamos
appi = APIRouter()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@appi.get("/")
async def root():
    return {"messaje": "hola soy root de rutas"}
