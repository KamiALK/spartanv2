from typing import Any, Dict, List
from fastapi import Depends, HTTPException, Query, status

# from typing import Optional
from fastapi import Cookie

# from pydantic import ValidationError
from model.Userdb import (
    Partido,
    Equipo,
    Jugadores,
    Campeonato,
    Arbitro_asignacion_Partido,
    Evaluaciones,
)
from sqlalchemy import desc
from sqlalchemy.orm import Session
from schema.estructura_schema import (
    EvaluacionesBase,
    PartidoBase,
    EquipoSchema,
    CampeonatoSchema,
    CampeonatosScheme,
    arbitro_asignacion_scheme,
)
#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    Partidos    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_all_partidos(db: Session):
    partidos = db.query(Partido).all()

    return partidos


def get_partido_by_equipo(db: Session, equipo_nombre: str, partido: PartidoBase):
    # Buscar el ID del equipo local usando el nombre del equipo proporcionado
    equipo_local = db.query(Equipo).filter(Equipo.nombre == equipo_nombre).first()
    if equipo_local:
        equipo_local_id = equipo_local.ID
    else:
        equipo_local_id = None

    # Buscar el ID del equipo visitante usando el nombre del equipo proporcionado
    equipo_visitante = (
        db.query(Equipo).filter(Equipo.nombre == partido.equipo_visitante_id).first()
    )
    if equipo_visitante:
        equipo_visitante_id = equipo_visitante.ID
    else:
        equipo_visitante_id = None

    # Verificar si se encontró el ID del equipo local o del equipo visitante
    if equipo_local_id is not None or equipo_visitante_id is not None:
        # Buscar el partido correspondiente en la base de datos
        partido_encontrado = (
            db.query(Partido)
            .filter(
                (Partido.equipo_local_id == equipo_local_id)
                | (Partido.equipo_visitante_id == equipo_visitante_id)
            )
            .first()
        )

        # Retornar el partido encontrado
        return partido_encontrado

    # Si no se encontró ni el equipo local ni el equipo visitante, retornar None
    return None


def get_partidos_by_id_partido(db, id_partido: int):
    # Utilizar el id_campeonato en la consulta
    partidos_encontrados: List[Partido] = (
        db.query(Partido).filter(Partido.ID == id_partido).all()
    )

    if partidos_encontrados:
        # Retornar todos los partidos encontrados
        return partidos_encontrados

    # Si no se encontraron partidos, retornar una lista vacía
    return []


def get_partidos_by_id_campeonato(db, id_campeonato: int):
    # Utilizar el id_campeonato en la consulta
    partidos_encontrados = (
        db.query(Partido).filter(Partido.campeonato_id == id_campeonato).all()
    )

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


def get_equipo_by_id_equipo(db, id_partido: int):
    # Utilizar el id_equipo en la consulta
    equipos_encontrados = db.query(Equipo).filter(Equipo.ID == id_partido).first()

    if equipos_encontrados:
        # Retornar todos los equipos encontrados
        return equipos_encontrados.nombre
    # Si no se encontraron equipos, retornar una lista vacía
    return []


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
    db_campeonato = Campeonato(nombre=campeonato.nombre)

    for equipo in campeonato.equipos:
        equipo_db = db.query(Equipo).filter(Equipo.ID == equipo.ID).first()
        if equipo_db:
            db_campeonato.equipos.append(equipo_db)

    db.add(db_campeonato)
    db.commit()
    db.refresh(db_campeonato)
    return db_campeonato


def get_campeonatos_all(db: Session):
    Campeonatos_encontrados = db.query(Campeonato).all()
    return Campeonatos_encontrados


#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    gestiones asignacion arbitros    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ahora tenemos q ue reguistra los partidos que pitan los arbitros


def asignar_arbitro_a_partido(
    db: Session, partido_arbitro_data: arbitro_asignacion_scheme
):
    # Buscar el partido en la base de datos
    partido = (
        db.query(Partido).filter(Partido.ID == partido_arbitro_data.partido_id).first()
    )
    if not partido:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Partido no encontrado"
        )

    # Buscar la asignación de árbitros para este partido
    partido_arbitro_entry = (
        db.query(Arbitro_asignacion_Partido)
        .filter(Arbitro_asignacion_Partido.partido_id == partido.ID)
        .first()
    )

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
            arbitro_4_id=arbitro_4_id,
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
    if evaluacion_id:
        # Actualiza el campo evaluacion_id en la tabla partido
        connection.execute(
            "UPDATE partido SET evaluacion_id = :evaluacion_id WHERE partido_id = :partido_id",
            {"evaluacion_id": evaluacion_id, "partido_id": target.partido_id},
        )


# Llama a la función actualizar_evaluacion_id con los argumentos adecuados


#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    evaluaciones    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def buscar_evaluacion_id_arbitro(db: Session, id: int) -> Evaluaciones:
    evaluacion: Evaluaciones = (
        db.query(Evaluaciones)
        .filter(Evaluaciones.arbitro_id == id)
        .order_by(desc(Evaluaciones.ID))
        .first()
    )
    # dict_evaluacion = Evaluaciones(**evaluacion.dict())
    return evaluacion


def buscar_evaluacion_id_evaluacion(db: Session, id: int) -> Evaluaciones:
    evaluacion: Evaluaciones = (
        db.query(Evaluaciones)
        .filter(Evaluaciones.ID == id)
        .order_by(desc(Evaluaciones.ID))
        .first()
    )
    # dict_evaluacion = Evaluaciones(**evaluacion.dict())
    return evaluacion


def buscar_all_evaluaciones(db: Session, id: int) -> List[Dict[str, Any]]:
    evaluaciones = (
        db.query(Evaluaciones)
        .filter(Evaluaciones.evaluador_id == id)
        .order_by(desc(Evaluaciones.ID))
        .all()
    )

    # Convertir objetos JSON a diccionarios
    evaluaciones_dicts = [evaluacion.__dict__ for evaluacion in evaluaciones]

    return evaluaciones_dicts if evaluaciones_dicts else []


def buscar_all_evaluaciones_arbitro(db: Session, id: int) -> List[Dict[str, Any]]:
    evaluaciones = (
        db.query(Evaluaciones)
        .filter(Evaluaciones.arbitro_id == id)
        .order_by(desc(Evaluaciones.ID))
        .all()
    )

    # Convertir objetos JSON a diccionarios
    evaluaciones_dicts = [evaluacion.__dict__ for evaluacion in evaluaciones]

    return evaluaciones_dicts if evaluaciones_dicts else []


def create_evaluacion(db: Session, Evaluacion: EvaluacionesBase):
    # Verificar si ya existe una evaluación para el partido proporcionado
    existing_evaluacion = (
        db.query(Evaluaciones).filter_by(partido_id=Evaluacion.partido_id).first()
    )
    if existing_evaluacion:
        return None  # Ya existe una evaluación para este partido

    # Si no existe, creamos una nueva instancia de Evaluaciones
    # se convierte el objeto a diccionario
    db_evaluacion = Evaluaciones(**Evaluacion.model_dump())

    # Agregamos y confirmamos los cambios en la base de datos
    db.add(db_evaluacion)
    db.commit()

    # Retornamos la evaluación creada
    return db_evaluacion


def actualizar_evaluacion_id(
    db: Session, partido_id: int, arbitro_id: int, created_evaluacion_id: int
):
    # Obtener la evaluación recién creada
    nueva_evaluacion = (
        db.query(Evaluaciones).filter_by(ID=created_evaluacion_id).first()
    )

    # Verificar si se encontró la evaluación
    if nueva_evaluacion:
        # Verificar si los IDs de partido y árbitro coinciden con los de la evaluación
        if (
            nueva_evaluacion.partido_id != partido_id
            or nueva_evaluacion.arbitro_id != arbitro_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Los IDs de partido y árbitro no coinciden con la evaluación creada",
            )

        # Consultar el registro más reciente en arbitros_partidos que coincida con el arbitro_id proporcionado
        latest_record = (
            db.query(Arbitro_asignacion_Partido)
            .filter(
                (Arbitro_asignacion_Partido.partido_id == partido_id)
                & (
                    (Arbitro_asignacion_Partido.arbitro_1_id == arbitro_id)
                    | (Arbitro_asignacion_Partido.arbitro_2_id == arbitro_id)
                    | (Arbitro_asignacion_Partido.arbitro_3_id == arbitro_id)
                    | (Arbitro_asignacion_Partido.arbitro_4_id == arbitro_id)
                )
            )
            .order_by(desc(Arbitro_asignacion_Partido.id))
            .first()
        )

        # Verificar si se encontró un registro
        if latest_record:
            # Actualizar el campo evaluacion_id en el registro encontrado
            latest_record.evaluacion_id = created_evaluacion_id
            db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró la evaluación recién creada",
        )


def buscar_partidos_evaluados(db: Session, arbitro_id: int):
    partidos_arbitrados_arbitro = (
        db.query(Arbitro_asignacion_Partido)
        .filter(
            (
                (Arbitro_asignacion_Partido.arbitro_1_id == arbitro_id)
                | (Arbitro_asignacion_Partido.arbitro_2_id == arbitro_id)
                | (Arbitro_asignacion_Partido.arbitro_3_id == arbitro_id)
                | (Arbitro_asignacion_Partido.arbitro_4_id == arbitro_id)
            )
        )
        .order_by(desc(Arbitro_asignacion_Partido.id))
        .all()
    )

    if partidos_arbitrados_arbitro:
        return partidos_arbitrados_arbitro
    else:
        # Manejo de error si el tipo de usuario no existe
        return []


def buscar_partidos_asignados(db: Session, arbitro_id: int):
    partidos_arbitrados_arbitro = (
        db.query(Arbitro_asignacion_Partido)
        .filter(
            (
                (Arbitro_asignacion_Partido.arbitro_1_id == arbitro_id)
                | (Arbitro_asignacion_Partido.arbitro_2_id == arbitro_id)
                | (Arbitro_asignacion_Partido.arbitro_3_id == arbitro_id)
                | (Arbitro_asignacion_Partido.arbitro_4_id == arbitro_id)
            )
        )
        .order_by(desc(Arbitro_asignacion_Partido.id))
        .all()
    )

    if partidos_arbitrados_arbitro:
        return partidos_arbitrados_arbitro
    else:
        # Manejo de error si el tipo de usuario no existe
        return []


def buscar_all_asignaciones(db: Session) -> arbitro_asignacion_scheme:
    return db.query(Arbitro_asignacion_Partido).all()

