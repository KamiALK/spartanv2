from fastapi import APIRouter


user = APIRouter()

@user.get("/")
def root():
    return {"messaje":"soy router y estoy siendo importado al main"}

@user.post("/api/user")
#data_user es la data del usuario que viene del backend
def create_user(data_user):
    return{}