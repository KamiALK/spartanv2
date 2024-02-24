from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from model.Userdb import Jugadores, Arbitros
from model.Userdb import Partido, Campeonato, Evaluaciones, Equipo
from schema.user_schema import UserID,UserData
from typing import List, Optional

class JugadoresBase(UserID):
    pass

class ArbitrosBase(UserID):
    pass

class EvaluadoresBase(UserID):
    pass

class EvaluacionesBase(BaseModel):
    arbitro_id: int
    evaluador_id: int
    estado_fisico: int
    observacionesEF: Optional[str] = None
    desplazamiento: int
    observacionesD: Optional[str] = None
    lectura_de_juego: int
    observacionesL: Optional[str] = None
    control_de_juego: int
    observacionesCDJ: Optional[str] = None
    nivelDificultadTorneo: int
    DificultadEtapaTorneo: int
    temperaturaEquipos: int
    situacionesRealesA: int
    faltasNaturalezaA: int
    faltasTacticasA: int
    situacionesRealesI: int
    faltasNaturalezaI: int
    faltasTacticasI: int

class Arbitros(ArbitrosBase):
    ID: int

    class Config:
        from_attributes = True

class Evaluadores(EvaluadoresBase):
    ID: int

    class Config:
        from_attributes = True

class Evaluaciones(EvaluacionesBase):
    ID: int

    class Config:
        from_attributes = True
        
class PartidoBase(BaseModel):
    campeonato_id: int
    fecha: datetime
    lugar: str
    equipo_local_id: Optional[int]
    equipo_visitante_id: Optional[int]



class Partido(PartidoBase):
    ID: int
    arbitros: List[Arbitros] = []

    class Config:
        from_attributes = True

# class EquipoSchema(BaseModel):
#     ID: int
#     nombre: str
#     jugadores: Optional[List[JugadoresBase]] = None
class EquipoSchema(BaseModel):
    ID: Optional[int]
    nombre: str
    jugadores_id: Optional[List[int]] = None

    
    
class Jugadores(JugadoresBase):
    ID: int
    equipo: Optional[List[EquipoSchema]] = None

    class Config:
        from_attributes = True


class CampeonatoSchema(BaseModel):
    ID: int
    nombre: str
    equipos: List[EquipoSchema] = []
    partidos: List[PartidoBase] = []

    class Config:
        from_attributes = True
