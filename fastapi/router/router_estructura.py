

from model.Userdb import Evaluaciones
from schema.estructura_schema import EquipoSchema, EvaluacionesBase,PartidoBase,CampeonatoSchema, partido_arbitro_scheme,arbitro_asignacion_scheme
from fastapi import APIRouter, Depends, HTTPException, status
from  sqlalchemy.orm import Session
from model.Get_DB import get_db
import router.functions_structuctura as function
from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
import requests
from fastapi import  Request, Depends,HTTPException, status
from  sqlalchemy.orm import Session
import router.crud as functio
from fastapi.responses import HTMLResponse
from fastapi import Request
import os




db:Session = Depends(get_db)


router = APIRouter()

templates = Jinja2Templates(directory="templates")




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




    
@router.get("/mostrar_evaluacion")
async def mostrar_evaluacion(id: int, db=Depends(get_db)):
    return function.buscar_evaluacion_id(db=db, id=id)
    

from fastapi import Cookie

@router.get("/users/me/evaluaciones/grafica/")
async def grafica(
    request: Request,
    db=Depends(get_db),
    token: str = Cookie(None) # Obtén el token de la cookie
):
    if token is None:
        raise HTTPException(status_code=401, detail="Token not found in cookie")
    try:
        #obtiene el usuario
        id1= functio.get_current_user( token=token)
        # Alamcena el id del usuario
        number_id = int(id1["ID"])
        #obtengo la evaluacion
        evaluaciones:Evaluaciones = function.buscar_evaluacion_id(db=db, id=number_id)
        
        # Renderizar la plantilla con los datos
        data = {
            "estadofisico": evaluaciones.estado_fisico,
            "desplazamiento": evaluaciones.desplazamiento,
            "lectura_de_juego": evaluaciones.lectura_de_juego,
            "control_de_juego": evaluaciones.control_de_juego,
            "nivelDificultadTorneo":evaluaciones.nivelDificultadTorneo,
            "DificultadEtapaTorneo":evaluaciones.DificultadEtapaTorneo,
            "temperaturaEquipos": evaluaciones.temperaturaEquipos,
            
            "situacionesRealesA": evaluaciones.situacionesRealesA,
            "faltasNaturalezaA": evaluaciones.faltasNaturalezaA,
            "faltasTacticasA": evaluaciones.faltasTacticasA,
            
            "situacionesRealesI": evaluaciones.situacionesRealesI,
            "faltasNaturalezaI": evaluaciones.faltasNaturalezaI,
            "faltasTacticasI": evaluaciones.faltasTacticasI,
            
            
            
        }
        
        return templates.TemplateResponse("user_grafica.html", {"request": request, "data": data})
    except:
        data = {
            "estadofisico": None,
            "desplazamiento": None,
            "lectura_de_juego": None,
            "control_de_juego": None,
            "nivelDificultadTorneo": None,
            "temperaturaEquipos": None,
            
            
            
            
        }
    return templates.TemplateResponse("user_grafica.html", {"request": request, "data": data})

        





