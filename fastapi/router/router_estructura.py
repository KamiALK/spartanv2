from schema.estructura_schema import PartidoBase
from fastapi import APIRouter, Depends, HTTPException, status
from  sqlalchemy.orm import Session
from model.Get_DB import get_db
import router.functions_structuctura as function

db:Session = Depends(get_db)


router = APIRouter()





#!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    Partidos    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@router.post("/partidos/arbitro/create")
async def create_partido(partido: PartidoBase, db=Depends(get_db)):
    created_partido = function.create_partido(db=db, partido=partido)
    if created_partido is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Partido ya existe")
    
    return created_partido