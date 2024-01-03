from fastapi import FastAPI
from router.router import user
app =FastAPI()

'''
uvicorn main:app --reload

'''
app.include_router(user)

