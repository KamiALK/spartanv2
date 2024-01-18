from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import session
import crud
from db.conection import engine,LocalSession
from schema.user_schema import Userschemanoid
from model.users import Base


#si no estan creadas nuestras tablas vamos a crearlas 
Base.metada.create_all(bing=engine)

#instanciamos
app =FastAPI()

def get_db():
    db =LocalSession()
    try:
        yield db
    finally:
        db.close()
        

@app.get("/")
async def root():
    return {"messaje":"hola soy root"}

@app.get("/users",response_model=list[Userschemanoid])
def get_users(db:session =Depends(get_db)):
    
    return crud.get_user(db=db)