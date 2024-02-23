# from  sqlalchemy.orm import Session
from db.conection import Session

#aqui la configuracion de la base de datos
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
