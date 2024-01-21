from fastapi import FastAPI, Request, Form, Response,Depends,HTTPException,APIRouter, status
from  sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from typing import Annotated
# from router.routers import appi
import router.crud 
from db.conection import engine,Session,Userdb,Base
from schema.user_schema import User,Userschemanoid,Usernopass, UserID







# 
appi =FastAPI()



def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


'''
uvicorn main:app --reload 


'''
# appi.include_router(appi)


person =Userdb(1,"andresito","andres","almanza",3143513617,31,1024,"M","andy@ffg",123)
# @app.get("/")
# async def root():
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
    
    
@appi.get("/")
async def root():
    return {"messaje": "hola soy root de rutas"}


@appi.get("/api/users/", response_model=list[UserID])
def get_users (db:Session=Depends(get_db)):    
    return router.crud.get_users(db=db)

@appi.get("/api/user/{id:int}",response_model=UserID)
def get_user(id, db:Session=Depends(get_db)):
         
    if router.crud.get_user(db=db,id=id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no se ha encontrado el usuario")
    return router.crud.get_user(db=db, id=id)


#     return 
# @router.get("/")
# async def root():
#     return {"messaje": "hola soy root de rutas"}
# gsfdg
