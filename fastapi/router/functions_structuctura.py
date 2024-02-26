from typing import Annotated
from fastapi import Depends,  HTTPException, Query, status
from typing import Optional
from fastapi import Cookie
# from pydantic import ValidationError
from model.Userdb import   Partido, Equipo,Jugadores,Campeonato,Arbitro_asignacion_Partido,Evaluaciones
from sqlalchemy import DateTime, desc
from sqlalchemy.orm import Session
from model.Userdb import Partido
from schema.estructura_schema import EvaluacionesBase, PartidoBase, EquipoSchema, CampeonatoSchema,Campeonato,partido_arbitro_scheme, arbitro_asignacion_scheme
from sqlalchemy import event
#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    Partidos    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_partido_by_equipo(db: Session, equipo_nombre: str, partido: PartidoBase):
    # Buscar el ID del equipo local usando el nombre del equipo proporcionado
    equipo_local = db.query(Equipo).filter(Equipo.nombre == equipo_nombre).first()
    if equipo_local:
        equipo_local_id = equipo_local.ID
    else:
        equipo_local_id = None
    
    # Buscar el ID del equipo visitante usando el nombre del equipo proporcionado
    equipo_visitante = db.query(Equipo).filter(Equipo.nombre == partido.equipo_visitante_id).first()
    if equipo_visitante:
        equipo_visitante_id = equipo_visitante.ID
    else:
        equipo_visitante_id = None
    
    # Verificar si se encontró el ID del equipo local o del equipo visitante
    if equipo_local_id is not None or equipo_visitante_id is not None:
        # Buscar el partido correspondiente en la base de datos
        partido_encontrado = db.query(Partido).filter((Partido.equipo_local_id == equipo_local_id) | (Partido.equipo_visitante_id == equipo_visitante_id)).first()
        
        # Retornar el partido encontrado
        return partido_encontrado
    
    # Si no se encontró ni el equipo local ni el equipo visitante, retornar None
    return None






def get_partidos_by_id_campeonato(db, id_campeonato: int):
    # Utilizar el id_campeonato en la consulta
    partidos_encontrados = db.query(Partido).filter(Partido.campeonato_id == id_campeonato).all()
    
    if partidos_encontrados:
        # Retornar todos los partidos encontrados
        return partidos_encontrados
    
    # Si no se encontraron partidos, retornar una lista vacía
    return []



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


def get_equipos_all(db: Session):
    return db.query(Equipo).all()



def create_equipo(db: Session, equipo: EquipoSchema):
    db_equipo = Equipo(
        nombre=equipo.nombre
        
    )
    # Asociar jugadores existentes al equipo
    for lider_id in equipo.lider_id:
        jugador = db.query(Jugadores).filter(Jugadores.ID == lider_id).first() # type: ignore
        print(jugador)
        if jugador:
            db_equipo.lider_id = lider_id
    db.add(db_equipo)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo

#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    Campeonato    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~



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



#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    gestiones asignacion arbitros    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ahora tenemos q ue reguistra los partidos que pitan los arbitros



def asignar_arbitro_a_partido(db: Session, partido_arbitro_data: arbitro_asignacion_scheme):
    # Buscar el partido en la base de datos
    partido = db.query(Partido).filter(Partido.ID == partido_arbitro_data.partido_id).first()
    if not partido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado")

    # Buscar la asignación de árbitros para este partido
    partido_arbitro_entry = db.query(Arbitro_asignacion_Partido).filter(Arbitro_asignacion_Partido.partido_id == partido.ID).first()
    
    # Convertir 0 a None para manejar NULL en la base de datos
    arbitro_1_id = partido_arbitro_data.arbitro_1_id or None
    arbitro_2_id = partido_arbitro_data.arbitro_2_id or None
    arbitro_3_id = partido_arbitro_data.arbitro_3_id or None
    arbitro_4_id = partido_arbitro_data.arbitro_4_id or None

    # Si la asignación de árbitros para este partido ya existe, actualizarla
    if partido_arbitro_entry:
        partido_arbitro_entry.arbitro_1_id = arbitro_1_id
        partido_arbitro_entry.arbitro_2_id = arbitro_2_id
        partido_arbitro_entry.arbitro_3_id = arbitro_3_id
        partido_arbitro_entry.arbitro_4_id = arbitro_4_id
    # Si no existe, crear una nueva asignación de árbitros para este partido
    else:
        partido_arbitro_entry = Arbitro_asignacion_Partido(
            partido_id=partido_arbitro_data.partido_id,
            arbitro_1_id=arbitro_1_id,
            arbitro_2_id=arbitro_2_id,
            arbitro_3_id=arbitro_3_id,
            arbitro_4_id=arbitro_4_id
        )
        db.add(partido_arbitro_entry)

    # Confirmar los cambios en la base de datos
    db.commit()
    
    


# Define una función para manejar el evento de inserción de una nueva evaluación
# Modifica la función actualizar_evaluacion_id para que acepte los argumentos connection y target
def actualizar_evaluacion_id(connection, target):
    # Recupera el ID de la evaluación recién insertada
    evaluacion_id = target.ID
    
    # Si el ID de la evaluación es diferente de None y diferente de 0
    if evaluacion_id :
        # Actualiza el campo evaluacion_id en la tabla partido
        connection.execute(
            "UPDATE partido SET evaluacion_id = :evaluacion_id WHERE partido_id = :partido_id",
            {"evaluacion_id": evaluacion_id, "partido_id": target.partido_id}
        )

# Llama a la función actualizar_evaluacion_id con los argumentos adecuados



#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    evaluaciones    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def create_evaluacion(db: Session, Evaluacion: EvaluacionesBase):
    # Verificar si ya existe una evaluación para el partido proporcionado
    existing_evaluacion = db.query(Evaluaciones).filter_by(partido_id=Evaluacion.partido_id).first()
    if existing_evaluacion:
        return None  # Ya existe una evaluación para este partido
    
    # Si no existe, creamos una nueva instancia de Evaluaciones
    db_evaluacion = Evaluaciones(**Evaluacion.model_dump())
    
    # Agregamos y confirmamos los cambios en la base de datos
    db.add(db_evaluacion)
    db.commit()
    
    # Retornamos la evaluación creada
    return db_evaluacion


from sqlalchemy import or_

def actualizar_evaluacion_id(db: Session, partido_id: int, arbitro_id: int, created_evaluacion: int):
    # Consultar el registro más reciente en arbitros_partidos que coincida con el arbitro_id proporcionado
    latest_record = db.query(Arbitro_asignacion_Partido).filter(
        (Arbitro_asignacion_Partido.partido_id == partido_id) &
        (
            (Arbitro_asignacion_Partido.arbitro_1_id == arbitro_id) |
            (Arbitro_asignacion_Partido.arbitro_2_id == arbitro_id) |
            (Arbitro_asignacion_Partido.arbitro_3_id == arbitro_id) |
            (Arbitro_asignacion_Partido.arbitro_4_id == arbitro_id)
        )
    ).order_by(desc(Arbitro_asignacion_Partido.id)).first()
    
    # Verificar si se encontró un registro
    if latest_record:
        # Actualizar el campo evaluacion_id en el registro encontrado
        latest_record.evaluacion_id = created_evaluacion
        print(latest_record)
        db.commit()



