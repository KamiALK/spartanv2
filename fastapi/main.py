from fastapi import FastAPI, Query, Request, Form, Response,Depends,HTTPException, status
from  sqlalchemy.orm import Session
import router.crud 
from fastapi.responses import HTMLResponse
from typing import Annotated
from db.conection import engine,Session,Base
from model.Userdb import tipo_clase_mapping as mapping
from model.Userdb import  Evaluadores,Arbitros,Jugadores
from schema.user_schema import UserData,Usernopass, UserID
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from router.crud import login_for_access_token
from fastapi import Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.responses import RedirectResponse








# aqui la configuracion de archivos jin2
from fastapi.staticfiles import StaticFiles
appi =FastAPI()
appi.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")



# Aca estamos configurando los cors
origin = [

    "http://localhost:4321",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

appi.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)


#aqui la configuracion de la base de datos
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


'''
uvicorn main:appi --reload 


'''

#aqui las rutas
# @appi.get("/", response_class=HTMLResponse)
# async def root(request: Request,):
#  return templates.TemplateResponse("dash.html", {"request": request, })#"current_user": current_user}
from fastapi.responses import RedirectResponse

@appi.get("/", response_class=HTMLResponse)
async def root(request: Request, tipo: str = Query(None)):
    if tipo in ["jugador", "arbitro", "evaluador", "normal"]:
        # Redirige al usuario a la ruta correspondiente
        return RedirectResponse(url=f"/{tipo}", status_code=status.HTTP_303_SEE_OTHER)
    else:
        # Si no se proporciona un tipo de usuario válido, simplemente muestra la página "dash"
        return templates.TemplateResponse("dash.html", {"request": request})

from fastapi import Path

@appi.get("/{tipo}", response_class=HTMLResponse)
async def get_users_tipolin(request: Request,tipo: str = Path(...),db=Depends(get_db)):
    usuarios = router.crud.get_users_tipo(db=db,tipo=tipo)
    
    # Aquí puedes acceder al tipo de usuario seleccionado (tipo)
    # y realizar las operaciones necesarias, como mostrar una página de inicio de sesión específica para ese tipo de usuario
    return templates.TemplateResponse("lista.html", {"request": request,  "usuarios": usuarios})

@appi.get("/api/users/", response_model=list[UserID])
def get_users (db=Depends(get_db)):    
    return router.crud.get_users(db=db)

@appi.get("/api/user/{id:int}",response_model=UserID)
def get_user(id, db=Depends(get_db)):
    u = router.crud.get_user_by_id(db=db,id=id)
    if u is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="no se ha encontrado el usuario")
    return router.crud.get_user_by_id(db=db, id=id)

@appi.post("/api/create",response_model=UserData)
async def create_user(user:UserData,db=Depends(get_db)):
    created_user = router.crud.create_user(db=db, user=user)
    if created_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario ya existe")
    
    return created_user








from fastapi import Cookie, HTTPException
from fastapi.responses import RedirectResponse
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@appi.get("/token", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




@appi.post("/token")
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    token_data = login_for_access_token(form_data=form_data, db=db)
    token_type = token_data['token_type']
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    response = RedirectResponse(url="/users/me", status_code=302)
    response.set_cookie(key="token", value=token_data['access_token'],domain="localhost", path="/")
    response.set_cookie(key="token_type", value=token_type, domain="localhost", path="/")

    return response

@appi.get("/users/me/", response_class=HTMLResponse)
async def read_users_me(request: Request, db=Depends(get_db),
                        current_user: dict = Depends(router.crud.get_current_user)):
    try:
        print(current_user) 

        return templates.TemplateResponse("user.html", {"request": request, "current_user": current_user})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")




    
    



