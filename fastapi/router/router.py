from fastapi import APIRouter


user = APIRouter()

@user.get("/")
def root():
    return {"messaje":"soy router y estoy siendo importado al main"}