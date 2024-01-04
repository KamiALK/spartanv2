from fastapi import FastAPI
# from router.router import user
from router.routerPRUEBA import userprueba

app =FastAPI()

'''
 

'''
# app.include_router(user)
app.include_router(userprueba)


