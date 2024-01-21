from fastapi import  Depends, HTTPException, APIRouter
from sqlalchemy.orm import session
# import crud
from db.conection import engine, Session, Userdb
from schema.user_schema import Userschemanoid



# instanciamos
app = APIRouter()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"messaje": "hola soy root de rutas"}
