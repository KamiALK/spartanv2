from fastapi import FastAPI, Request, Form, Response,Depends,HTTPException
from  sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from typing import Annotated
from router.routers import app
import router.crud
from db.conection import engine,Session,User,Base
from schema.user_schema import User,Userschemanoid,Usernopass








app =FastAPI()




'''
uvicorn main:app --reload 


'''
# app.include_router(userprueba)
app.include_router(app)



