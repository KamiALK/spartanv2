from fastapi import FastAPI, Query, Request, Form, Depends, HTTPException, status

# from sqlalchemy.orm import Session
import router.crud
from fastapi.responses import HTMLResponse
from db.conection import Session
from schema.user_schema import UserData
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from router.crud import login_for_access_token
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Path
import router.router_estructura as partido_router


# aqui la configuracion de archivos jin2
appi = FastAPI()


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


# aqui la configuracion de la base de datos
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


appi.include_router(partido_router.router)

"""
uvicorn main:appi --reload 


"""


@appi.get("/", response_class=HTMLResponse)
async def root(request: Request, tipo: str = Query(None)):
    if tipo in ["jugador", "arbitro", "evaluador", "normal"]:
        # Redirige al usuario a la ruta correspondiente
        return RedirectResponse(url=f"/{tipo}", status_code=status.HTTP_303_SEE_OTHER)
    else:
        # Si no se proporciona un tipo de usuario válido, simplemente muestra la página "dash"
        return templates.TemplateResponse("dash.html", {"request": request})


@appi.get("/{tipo}/", response_class=HTMLResponse)
async def get_users_all(request: Request, tipo: str = Path(...), db=Depends(get_db)):
    usuarios = router.crud.get_users(db=db, tipo=tipo)
    print("Valor de tipo antes de llamar a get_user_by_email:", tipo)
    return templates.TemplateResponse(
        "index.html", {"request": request, "tipo": tipo, "usuarios": usuarios}
    )


@appi.get("/{tipo}/{id:int}", response_class=HTMLResponse)  # Cambia ID a id
async def get_user_id(
    request: Request, id, db=Depends(get_db), tipo: str = Path(...)
):  # Cambia ID a id
    usuarios = router.crud.get_user_by_id(db=db, tipo=tipo, ID=id)  # Cambia ID a id

    if usuarios is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no se ha encontrado el usuario",
        )
    return templates.TemplateResponse(
        "lista_filter_id.html", {"request": request, "usuarios": usuarios}
    )


@appi.get("/{tipo}/cedula/{cedula:int}", response_class=HTMLResponse)  # Cambia ID a id
async def get_user_cc(
    request: Request, cedula, db=Depends(get_db), tipo: str = Path(...)
):  # Cambia a cedula
    usuarios = router.crud.get_user_by_cedula(
        db=db, tipo=tipo, cedula=cedula
    )  # Cambia ID a id

    if usuarios is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no se ha encontrado el usuario",
        )
    return templates.TemplateResponse(
        "lista_filter_cedula.html", {"request": request, "usuarios": usuarios}
    )


#!!!!!!!!!!!!!!!!!!!!!!!     creacion de usuario
@appi.post("/usuarios/registro", response_model=UserData)
async def create_user(
    request: Request,
    username: str = Form(...),
    nombre: str = Form(...),
    apellido: str = Form(...),
    celular: int = Form(...),
    edad: int = Form(...),
    cedula: int = Form(...),
    genero: str = Form(...),
    email: str = Form(...),
    passwd: str = Form(...),
    tipo: str = Form(...),
    db=Depends(get_db),
):
    user_data = UserData(
        username=username,
        nombre=nombre,
        apellido=apellido,
        celular=celular,
        edad=edad,
        cedula=cedula,
        genero=genero,
        email=email,
        passwd=passwd,
    )
    new_user = router.crud.create_new_user(db=db, user=user_data, tipo=tipo)
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario ya existe"
        )

    return new_user


@appi.get("/usuarios/registro", response_class=HTMLResponse)
async def create_user_get(
    request: Request,
    db=Depends(get_db),
):
    return templates.TemplateResponse("registro.html", {"request": request})


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!     login de usuario
@appi.get("/token")
async def obtener_tipo(request: Request, tipo: str):
    print("Valor de tipo antes de llamar a get_user_by_email:", tipo)
    print(tipo)
    return {"tipo": tipo}


@appi.post("/token")
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    tipo: str = Form(...),  # Agrega el parámetro tipo
    db=Depends(get_db),
):
    # print("Valor de tipo antes de llamar a get_user_by_email:", tipo)
    token_data = login_for_access_token(
        form_data=form_data, db=db, tipo=tipo
    )  # Pasa el tipo al método de autenticación
    token_type = token_data["token_type"]
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    response = RedirectResponse(url="/users/me", status_code=302)
    response.set_cookie(
        key="token", value=token_data["access_token"], domain="localhost", path="/"
    )
    response.set_cookie(
        key="token_type", value=token_type, domain="localhost", path="/"
    )

    # estoy intentanto inyectar el id para poder maniobrar en toda la pagina
    # response.set_cookie(key="ID", value=str(token_data['ID']), domain="localhost", path="/")
    return response


@appi.get("/users/me/", response_class=HTMLResponse)
async def read_users_me(
    request: Request,
    db=Depends(get_db),
    current_user: dict = Depends(router.crud.get_current_user),
):
    try:
        if current_user["tipo"] == "admin":
            return templates.TemplateResponse(
                "admin.html", {"request": request, "current_user": current_user}
            )
        elif current_user["tipo"] == "Arbitros":
            return templates.TemplateResponse(
                "user.html", {"request": request, "current_user": current_user}
            )
        elif current_user["tipo"] == "Evaluadores":
            return templates.TemplateResponse(
                "user_dos.html", {"request": request, "current_user": current_user}
            )
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
