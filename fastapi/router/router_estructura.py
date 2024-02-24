from schema.estructura_schema import EquipoSchema,PartidoBase,CampeonatoSchema,Campeonato
from fastapi import APIRouter, Depends, HTTPException, status
from  sqlalchemy.orm import Session
from model.Get_DB import get_db
import router.functions_structuctura as function

db:Session = Depends(get_db)


router = APIRouter()





#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    Partidos    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@router.post("/partidos/arbitro/create")
async def create_partido_jugador(partido: PartidoBase, db=Depends(get_db)):
    created_partido = function.create_partido(db=db, partido=partido)
    if created_partido is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Partido ya existe")
    
    return created_partido

#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~     equipo     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
