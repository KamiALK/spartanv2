from typing import Annotated
from fastapi import Depends,  HTTPException, Query, status
from typing import Optional
from fastapi import Cookie
from model.Userdb import   Partido, Equipo,Jugadores,Campeonato
from sqlalchemy import DateTime
from sqlalchemy.orm import Session
from model.Userdb import Partido
from schema.estructura_schema import PartidoBase, EquipoSchema, CampeonatoSchema,Campeonato

#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    Partidos    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
    # db.refresh(db_partido)
    db.flush(db_partido)

#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     Equipo     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# me falt la opcion de buscar partido por nombre

#me falt la opcion de buscar partido por id

def create_equipo(db: Session, equipo: EquipoSchema):
    db_equipo = Equipo(
        nombre=equipo.nombre
    )
    # Asociar jugadores existentes al equipo
    for jugador_id in equipo.jugadores_id:
        jugador = db.query(Jugadores).filter(Jugadores.ID == jugador_id).first()
        if jugador:
            db_equipo.jugadores.append(jugador)
    db.add(db_equipo)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo

#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    Campeonato    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# def create_campeonato(db: Session, campeonato: Campeonato):
#     db_campeonato = Campeonato(
#         nombre=campeonato.nombre
#     )
    
#     db.add(db_campeonato)
#     db.commit()
#     db.refresh(db_campeonato)
#     return db_campeonato


def create_campeonato(db: Session, campeonato: CampeonatoSchema):
    db_campeonato = Campeonato(
        nombre=campeonato.nombre
    )
    
 
    for equipo in campeonato.equipos:
        equipo_db = db.query(Equipo).filter(Equipo.ID == equipo.ID).first()
        if equipo_db:
            db_campeonato.equipos.append(equipo_db)
    
    db.add(db_campeonato)
    db.commit()
    db.refresh(db_campeonato)
    return db_campeonato



