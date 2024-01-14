#tenemos que diseñar el esquema para el usuario que entra del backend
from pydantic import BaseModel
from typing import Optional 



    
class UserSchemalogin (BaseModel):
    # id : Optional[str] =None
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
    
class Usernopass(BaseModel):
    id: Optional[int] = None
    username: str
    nombre: str
    apellido: str
    celular: int
    edad: int
    cedula: int
    email: str
    
    
class Userschemanoid(BaseModel):

    username: str
    nombre: str
    apellido: str
    celular: int
    edad: int
    cedula: int
    passwd: str
    email: str
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

    
    




    
    
        
    
    
    