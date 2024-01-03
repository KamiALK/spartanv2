#tenemos que diseñar el esquema para el usuario que entra del backend
from pydantic import BaseModel
from typing import Optional


class UserSchema (BaseModel):
    id: Optional[str]
    name: str
    username: str
    userpass: str
        
    
    
    