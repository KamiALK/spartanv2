from fastapi import FastAPI, Request, Form, Response,Depends,HTTPException,APIRouter, status
from  sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from typing import Annotated
# from router.routers import appi
import router.crud 
from db.conection import engine,Session,Userdb,Base
from schema.user_schema import UserData,Userschemanoid,Usernopass, UserID







# 
appi =FastAPI()



def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


'''
uvicorn main:appi --reload 


'''





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
    u = router.crud.get_user_by_id(db=db,id=id)
    if u is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no se ha encontrado el usuario")
    return router.crud.get_user_by_id(db=db, id=id)

@appi.post("/api/create",response_model=UserData)
async def create_user(user:UserData,db:Session=Depends(get_db)):
    created_user = router.crud.create_user(db=db, user=user)
    if created_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario ya existe")
    
    return created_user