from typing import Annotated
from fastapi import Depends,  HTTPException, Query, status
from typing import Optional
from fastapi import Cookie
from model.Userdb import   Partido
from sqlalchemy import DateTime
from sqlalchemy.orm import Session
from model.Userdb import Partido
from schema.estructura_schema import PartidoBase


def get_partido_by_username(db, username: str, tipo: str=Partido):
    # clase_usuario = tipo_clase_mapping.get(tipo)
    print(tipo)
    # user:UserID = db.query(clase_usuario).filter(email == username).first()
    user = db.query(tipo).filter_by(email=username).first()
    return user

def get_partido_by_id(db, ID: int, tipo: str = Partido):  # Cambia ID a id
    # clase_usuario = tipo_clase_mapping.get(tipo)
    # Utiliza filter para buscar usuarios por ID
    user = db.query(tipo).filter_by(ID=ID).first()  # Cambia ID a ID
    if user:
        # print(f"El tipo de usuario es: {clase_usuario}")
        return user
    else:
        # Manejo de error si el tipo de usuario no existe
        return None

    


# def get_user_by_cedula(db, cedula: int):
#     user = db.query(Userdb).filter(Userdb.cedula == cedula).first()
def get_partido_by_campeonato(db, cedula: int, tipo: str= Partido):  #
    
    # Utiliza filter para buscar usuarios por ID
    partido = db.query(tipo).filter_by(cedula=cedula).first() 
    if partido:
        # print(f"El tipo de usuario es: {clase_usuario}")
        return partido
    else:
        # Manejo de error si el tipo de usuario no existe
        return None







def create_partido(db: Session, partido: PartidoBase):
    # Creamos una instancia de la clase Partido con los datos proporcionados
    db_partido = Partido(
        campeonato_id=partido.campeonato_id,
        fecha=partido.fecha,
        lugar=partido.lugar,
        equipo_local_id=partido.equipo_local_id,
        equipo_visitante_id=partido.equipo_visitante_id,
    )
    
   

    db.add(db_partido)
    db.commit()
    db.refresh(db_partido)
    db.flush(db_partido)