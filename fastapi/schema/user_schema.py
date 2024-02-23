#tenemos que diseñar el esquema para el usuario que entra del backend
from pydantic import BaseModel
from typing import Optional 



    
class UserSchemalogin (BaseModel):
    # id : Optional[str] =None
    username: str
    passwd: str
    



class UserData(BaseModel):
    
    username: str
    nombre: str
    apellido: str
    celular: int
    edad: int
    cedula: int
    genero:str
    email: str
    passwd: str
    
class UserID(UserData):
    ID: int |None=None

    
class Usernopass(BaseModel):
    ID: int |None=None
    username: str
    nombre: str
    apellido: str
    edad: int
    email: str
    
    
class Userschemanoid(BaseModel):

    username: str
    nombre: str
    apellido: str
    celular: int
    edad: int
    cedula: int
    email: str
    passwd: str
    

    
    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None





class UserInDB(Usernopass):
    passwd  : str

    


    

    
    




    
    
        
    
    
    