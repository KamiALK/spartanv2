from fastapi import APIRouter
from pydantic import BaseModel
from schema.user_schema import UserSchema
from db.conection import conn, engine
from model.users import users


user = APIRouter()



@user.get("/")
async def root():
    return {"messaje":"soy router y estoy siendo importado al main"}


    