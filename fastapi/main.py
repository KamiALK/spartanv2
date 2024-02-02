from fastapi import FastAPI, Request, Form, Response,Depends,HTTPException, status
from  sqlalchemy.orm import Session
import router.crud 
from fastapi.responses import HTMLResponse
from typing import Annotated
from db.conection import engine,Session,Userdb,Base
from schema.user_schema import UserData,Usernopass, UserID
from fastapi.middleware.cors import CORSMiddleware

# 
appi =FastAPI()

# appi.include_router(router.crud)

# Aca estamos configurando los cors
origin = [

    "http://localhost",
    "http://localhost:3000",
]

appi.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


'''
uvicorn main:appi --reload 


'''

    
@appi.get("/")
async def root():
    return {"messaje": "hola soy root de rutas"}


@appi.get("/api/users/", response_model=list[Usernopass])
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

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from router.crud import login_for_access_token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@appi.post("/token")
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db) ):
    return login_for_access_token( form_data=form_data,db=db)



@appi.get("/users/me/", response_model=Usernopass)
async def read_users_me(db:Session=Depends(get_db),
    current_user:Usernopass=Depends(router.crud.get_current_user)
):
    username=current_user
    user=router.crud.get_user_by_username(db=db,username=username)
    return user


@appi.get("/users/me/items/")
async def read_own_items(db:Session=Depends(get_db),
    current_user:Usernopass=Depends(router.crud.get_current_user)
):
    username=current_user
    user=router.crud.get_user_by_username(db=db,username=username)
    return [{"item_id": "Foo", "owner": user.username}]