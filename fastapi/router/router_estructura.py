from model.Userdb import Evaluaciones
from schema.estructura_schema import EquipoSchema, EvaluacionesBase,PartidoBase,CampeonatoSchema, partido_arbitro_scheme,arbitro_asignacion_scheme
from fastapi import APIRouter, Depends, HTTPException, status
from  sqlalchemy.orm import Session
from model.Get_DB import get_db
import router.functions_structuctura as function
from fastapi import FastAPI, HTTPException
import requests

db:Session = Depends(get_db)


router = APIRouter()






#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    Partidos    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@router.post("/get_partidos_nombre")
async def buscar_partido_by_nombre_equipo(equipo: str, partido: PartidoBase, db: Session = Depends(get_db)):
    if equipo and partido:
        # Llamar a la función para obtener el partido por equipo
        partido_encontrado = function.get_partido_by_equipo(db=db, equipo_nombre=equipo, partido=partido)
        
        if partido_encontrado:
            return partido_encontrado
        else:
            return {"message": "No se encontró ningún partido para el equipo proporcionado."}
    else:
        return {"message": "Se requieren tanto el nombre del equipo como los datos del partido para realizar la búsqueda."}

@router.post("/get_partidos_campeonato_id")
async def buscar_partidos_by_id_campeonato(id_campeonato: int,  db: Session = Depends(get_db)):
    partido_encontrado = function.get_partidos_by_id_campeonato(db=db, id_campeonato=id_campeonato)
    if partido_encontrado: 
        return partido_encontrado    
    else:
        return {"message": "No se encontró ningún partido con el ID del campeonato proporcionado."}





@router.post("/partidos/arbitro/create")
async def create_partido_jugador(partido: PartidoBase, db=Depends(get_db)):
    created_partido = function.create_partido(db=db, partido=partido)
    
    if created_partido is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Partido ya existe")
    
    return created_partido


#el arbitro tiene que registrar su partido e informar el partido 
from fastapi import HTTPException, status

@router.post("/partidos/evaluacion/update")
async def update_partido_evaluador(partido_evaluador_data: partido_arbitro_scheme, db: Session = Depends(get_db)):
    try:
        updated_partido = function.asignar_arbitro_a_partido(db=db, partido_arbitro_data=partido_evaluador_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    return updated_partido


@router.get("/partidos_asignados_arbitro")
async def get_partidos_evaluados(id: int, db=Depends(get_db)):
    return function.buscar_partidos_evaluados(db=db, arbitro_id=id)

@router.get("/mostrar_evaluacion")
async def mostrar_evaluacion(id: int, db=Depends(get_db)):
    return function.buscar_evaluacion_id(db=db, id=id)










#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     equipo     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@router.get("/get_equipos")
async def get_equipos(db=Depends(get_db)):
    return  function.get_equipos_all(db=db)

@router.post("/equipo/amistoso")
async def create_equipo_amistoso(equipo: EquipoSchema, db=Depends(get_db)):
    created_equipo = function.create_equipo(db=db, equipo=equipo)
    
    if created_equipo is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Partido ya existe")
    
    return created_equipo

#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     Campeonato     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@router.post("/campeonato/amistoso")
async def create_campeonato_amistoso(campeonato:CampeonatoSchema , db=Depends(get_db)):
    created_campeonato = function.create_campeonato(db=db, campeonato=campeonato)
    
    if created_campeonato is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Partido ya existe")
    
    
    return created_campeonato

#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    evaluacion Arbitro   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@router.post("/partidos/evaluacion")
async def create_evaluacion_arbitro(evaluacion_data: EvaluacionesBase, db: Session = Depends(get_db)):
    # Crear la evaluación
    created_evaluacion = function.create_evaluacion(db=db, Evaluacion=evaluacion_data)
    
    # Verificar si la evaluación se creó correctamente
    if created_evaluacion is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Evaluación ya existe")
    
    # Llamar a la función para actualizar el campo evaluacion_id en la tabla arbitros_partidos
    function.actualizar_evaluacion_id(
        db=db,
        partido_id=evaluacion_data.partido_id,
        arbitro_id=evaluacion_data.arbitro_id,
        created_evaluacion_id=created_evaluacion.ID
    )
    
    # Retornar la evaluación creada
    return created_evaluacion

#!~~~~~~~~~~~~~~~~~~~~~~    enviar evaluacion api   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

@router.get("/enviar_evaluacion_api")
async def enviar_evaluacion_api(id: int, db=Depends(get_db)):
    return function.buscar_evaluacion_id(db=db, id=id)



@router.post("/webhook")
async def enviar_evaluacion_api(id: int, db=Depends(get_db)):
    data = function.buscar_evaluacion_id(db=db, id=id)
    data_dict = data.__dict__
    print(data_dict)
    try:
        
        response = requests.post("http://localhost:8080/obtener_data", json=data_dict)
        response.raise_for_status()  # Esto generará una excepción si la solicitud falla
        return response
    except requests.exceptions.RequestException as e:
        return {"error": f"Error al enviar la solicitud a la segunda API: {str(e)}"}
    
@router.get("/mostrar_evaluacion")
async def mostrar_evaluacion(id: int, db=Depends(get_db)):
    return function.buscar_evaluacion_id(db=db, id=id)
    