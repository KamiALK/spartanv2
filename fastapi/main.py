from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse
from typing import Annotated
from router.routerPRUEBA import userprueba,User
from router.routers import app
import router.routerPRUEBA

from schema.user_schema import User,Userschemanoid,Usernopass




app =FastAPI()




'''
uvicorn main:app --reload 


'''
# app.include_router(userprueba)
app.include_router(app)



