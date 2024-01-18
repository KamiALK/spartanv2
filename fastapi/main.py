from fastapi import FastAPI, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Annotated
from router.routerPRUEBA import userprueba,User
import router.routerPRUEBA
from model.users import users
from schema.user_schema import User,Userschemanoid,Usernopass




app =FastAPI()


Jinja2_Templates=Jinja2Templates(directory="templates")

'''
uvicorn main:app --reload 


'''
app.include_router(userprueba)

@app.get("/", response_class=HTMLResponse)
async def root(request:Request):
    return Jinja2_Templates.TemplateResponse("index.html", {"request":request})
                                         

@app.get("/user/dash/", response_class=HTMLResponse)
async def dashh(request:Request):
    return Jinja2_Templates.TemplateResponse("index.html", {"request":request})


@app.get("/signup")
async def singup(req: Request):
    return  Jinja2_Templates.TemplateResponse("signup.html", {"request": req})

@app.get("/user")
async def user (req:Request):
    return  Jinja2_Templates.TemplateResponse("user.html", {"request": req})



#paso uno el login 
@app.post("/loginfront")
async def login(username:Annotated[str,Form()], password:Annotated[str,Form()],request:Request):
    return  Jinja2_Templates.TemplateResponse("login.html", {"request":request})





