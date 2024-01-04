#tenemos que diseñar el esquema para el usuario que entra del backend
from pydantic import BaseModel
from typing import Optional



    
class UserSchema (BaseModel):
    id : Optional[str] =None
    username: str
    passwd: str
    



class User(BaseModel):
    id: Optional[int] = None
    username: str
    nombre: str
    apellido: str
    celular: int
    edad: int
    cedula: int
    passwd: str
    email: str
    
class Usernoid(BaseModel):

    username: str
    nombre: str
    apellido: str
    celular: int
    edad: int
    cedula: int
    passwd: str
    email: str

    
    




    
    
        
    
    
    