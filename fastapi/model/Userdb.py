#aqui deben ir todos los modelos de la base de datos


from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


usuarios_equipos = Table('usuarios_equipos', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.ID'),nullable=True),
    Column('equipo_id', Integer, ForeignKey('equipos.ID'),nullable=True)
)
partido_arbitro = Table('partido_arbitro', Base.metadata,
    Column('arbitro_id', Integer, ForeignKey('arbitros.ID'),nullable=True),
    Column('partido_id', Integer, ForeignKey('partidos.ID'),nullable=True)
)
campeonatos_equipos = Table('campeonatos_equipos', Base.metadata,
                            Column('campeonato_id', Integer, ForeignKey('campeonatos.ID'),nullable=True),
                            Column('equipo_id', Integer, ForeignKey('equipos.ID'),nullable=True)
                            )


class Jugadores(Base):
    __tablename__ = "usuarios"
    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    username = Column("username", String(250), nullable=False)
    nombre = Column("nombre", String(250), nullable=False)
    apellido = Column("apellido", String(250), nullable=False)
    celular = Column("celular", Integer, nullable=False)
    edad = Column("edad", Integer, nullable=False)
    cedula = Column("cedula", Integer, unique=True, nullable=False)
    genero = Column("genero", String(250), nullable=False)
    email = Column("email", String(250), nullable=False)
    passwd = Column("passwd", String(250), nullable=False)
    equipos = relationship("Equipo", secondary=usuarios_equipos, back_populates="jugadores")
    def __init__(self, ID, username, nombre, apellido, celular, edad, cedula, genero, email, passwd):
        self.ID = ID
        self.username = username
        self.nombre = nombre
        self.apellido = apellido
        self.celular = celular
        self.edad = edad
        self.cedula = cedula
        self.genero = genero
        self.email = email
        self.passwd = passwd

    def __repr__(self):
        return f"({self.ID}){self.username}{self.nombre}{self.apellido}({self.celular},{self.edad},{self.cedula}){self.genero}{self.email}{self.passwd}"


class Arbitros(Base):
    __tablename__ = "arbitros"
    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    username = Column("username", String(250), nullable=False)
    nombre = Column("nombre", String(250), nullable=False)
    apellido = Column("apellido", String(250), nullable=False)
    celular = Column("celular", Integer, nullable=False)
    edad = Column("edad", Integer, nullable=False)
    cedula = Column("cedula", Integer, unique=True, nullable=False)
    genero = Column("genero", String(250), nullable=False)
    email = Column("email", String(250), nullable=False)
    passwd = Column("passwd", String(250), nullable=False)
    evaluaciones = relationship("Evaluaciones", back_populates="arbitro")
    def __init__(self, ID, username, nombre, apellido, celular, edad, cedula, genero, email, passwd):
        self.ID = ID
        self.username = username
        self.nombre = nombre
        self.apellido = apellido
        self.celular = celular
        self.edad = edad
        self.cedula = cedula
        self.genero = genero
        self.email = email
        self.passwd = passwd
        self.evaluaciones = []
    def __repr__(self):
        return f"({self.ID}){self.username}{self.nombre}{self.apellido}({self.celular},{self.edad},{self.cedula}){self.genero}{self.email}{self.passwd}"
    
    
    
    
class Evaluadores(Base):
    __tablename__ = "evaluadores"
    ID = Column("ID", Integer, primary_key=True, autoincrement=True)
    username = Column("username", String(250), nullable=False)
    nombre = Column("nombre", String(250), nullable=False)
    apellido = Column("apellido", String(250), nullable=False)
    celular = Column("celular", Integer, nullable=False)
    edad = Column("edad", Integer, nullable=False)
    cedula = Column("cedula", Integer, unique=True, nullable=False)
    genero = Column("genero", String(250), nullable=False)
    email = Column("email", String(250), nullable=False)
    passwd = Column("passwd", String(250), nullable=False)
    evaluaciones = relationship("Evaluaciones", back_populates="evaluador")
    
    def __init__(self, ID, username, nombre, apellido, celular, edad, cedula, genero, email, passwd):
        self.ID = ID
        self.username = username
        self.nombre = nombre
        self.apellido = apellido
        self.celular = celular
        self.edad = edad
        self.cedula = cedula
        self.genero = genero
        self.email = email
        self.passwd = passwd
        self.evaluaciones = []
    def __repr__(self):
        return f"({self.ID}){self.username}{self.nombre}{self.apellido}({self.celular},{self.edad},{self.cedula}){self.genero}{self.email}{self.passwd}"
    
    

class Equipo(Base):
    __tablename__ = "equipos"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(250), nullable=False)
    jugadores = relationship("Jugadores", secondary=usuarios_equipos, back_populates="equipos")
    partidos_local = relationship("Partido", foreign_keys="[Partido.equipo_local_id]", back_populates="equipo_local")
    partidos_visitante = relationship("Partido", foreign_keys="[Partido.equipo_visitante_id]", back_populates="equipo_visitante")
    campeonatos = relationship("Campeonato", secondary=campeonatos_equipos, back_populates="equipos")  

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f"Equipo(ID={self.ID}, nombre={self.nombre})"

    




# Tabla de asociación entre Campeonatos y Equipos

class Campeonato(Base):
    __tablename__ = "campeonatos"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(250), nullable=False)
    equipos = relationship("Equipo", secondary=campeonatos_equipos, back_populates="campeonatos")
    partidos = relationship("Partido", back_populates="campeonato")

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f"Campeonato(ID={self.ID}, nombre={self.nombre})"

    @classmethod
    def __get_pydantic_core_schema__(cls, model):
        # Aquí implementa la lógica para generar un esquema Pydantic para la clase Campeonato
        pass

class Partido(Base):
    __tablename__ = "partidos"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    campeonato_id = Column(Integer, ForeignKey('campeonatos.ID'), nullable=True)
    fecha = Column(DateTime, nullable=True)
    lugar = Column(String(250), nullable=True)
    equipo_local_id = Column(Integer, ForeignKey('equipos.ID'), nullable=True)
    equipo_visitante_id = Column(Integer, ForeignKey('equipos.ID'), nullable=True)

    # Relación con árbitros a través de la tabla de asociación partido_arbitro
    arbitros = relationship("Arbitros", secondary=partido_arbitro)

    campeonato = relationship("Campeonato", back_populates="partidos")
    equipo_local = relationship("Equipo", foreign_keys=[equipo_local_id])
    equipo_visitante = relationship("Equipo", foreign_keys=[equipo_visitante_id])

    def __repr__(self):
        return f"Partido(ID={self.ID}, campeonato_id={self.campeonato_id}, fecha={self.fecha}, lugar={self.lugar}, equipo_local_id={self.equipo_local_id}, equipo_visitante_id={self.equipo_visitante_id})"

class Evaluaciones(Base):
    __tablename__ = "evaluaciones"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    arbitro_id = Column(Integer, ForeignKey('arbitros.ID'), nullable=False)
    evaluador_id = Column(Integer, ForeignKey('evaluadores.ID'), nullable=False)
    estado_fisico = Column(Integer, nullable=False)
    observacionesEF = Column(String(250), nullable=True)
    desplazamiento = Column(Integer, nullable=False)
    observacionesD = Column(String(250), nullable=True)  
    lectura_de_juego = Column(Integer, nullable=False)
    observacionesL = Column(String(250), nullable=True)
    control_de_juego = Column(Integer, nullable=False)
    observacionesCDJ = Column(String(250), nullable=True)
    nivelDificultadTorneo = Column(Integer, nullable=False)
    DificultadEtapaTorneo = Column(Integer, nullable=False)    
    temperaturaEquipos = Column(Integer, nullable=False)
    situacionesRealesA = Column(Integer, nullable=False)
    faltasNaturalezaA = Column(Integer, nullable=False)
    faltasTacticasA = Column(Integer, nullable=False)
    situacionesRealesI = Column(Integer, nullable=False)
    faltasNaturalezaI = Column(Integer, nullable=False)
    faltasTacticasI = Column(Integer, nullable=False)
    # Establece las relaciones con las tablas Arbitros y Evaluadores
    arbitro = relationship("Arbitros", back_populates="evaluaciones")
    evaluador = relationship("Evaluadores", back_populates="evaluaciones")

    
    def __init__(self,arbitro_id,evaluador_id,estado_fisico,observacionesEF,desplazamiento,observacionesD,lectura_de_juego,observacionesL,control_de_juego,observacionesCDJ,nivelDificultadTorneo,DificultadEtapaTorneo,temperaturaEquipos,situacionesRealesI,faltasNAturalezaI,faltasTacticasI,situacionesRealesA,faltasNAturalezaA,faltasTacticasA):
        self.arbitro_id=arbitro_id
        self.evaluador_id=evaluador_id
        self.estado_fisico=estado_fisico
        self.observacionesEF=observacionesEF
        self.desplazamiento=desplazamiento
        self.observacionesD=observacionesD
        self.lectura_de_juego=lectura_de_juego
        self.observacionesL=observacionesL
        self.control_de_juego=control_de_juego
        self.observacionesCDJ=observacionesCDJ
        self.nivelDificultadTorneo=nivelDificultadTorneo
        self.DificultadEtapaTorneo=DificultadEtapaTorneo
        self.temperaturaEquipos=temperaturaEquipos
        self.situacionesRealesI=situacionesRealesI
        self.faltasNAturalezaI=faltasNAturalezaI
        self.faltasTacticasI=faltasTacticasI
        self.situacionesRealesA=situacionesRealesA
        self.faltasNAturalezaA=faltasNAturalezaA
        self.faltasTacticasA=faltasTacticasA
        
        
    def __repr__(self):
        
        return f"Evaluaciones(arbitro_id={self.arbitro_id}, evaluador_id={self.evaluador_id}, estado_fisico={self.estado_fisico}, observacionesEF={self.observacionesEF}, desplazamiento={self.desplazamiento}, observacionesD={self.observacionesD}, lectura_de_juego={self.lectura_de_juego}, observacionesL={self.observacionesL}, control_de_juego={self.control_de_juego}, observacionesCDJ={self.observacionesCDJ}, nivelDificultadTorneo={self.nivelDificultadTorneo}, DificultadEtapaTorneo={self.DificultadEtapaTorneo}, temperaturaEquipos={self.temperaturaEquipos}, situacionesRealesI={self.situacionesRealesI}, faltasNAturalezaI={self.faltasNAturalezaI}, faltasTacticasI={self.faltasTacticasI}, situacionesRealesA={self.situacionesRealesA}, faltasNAturalezaA={self.faltasNAturalezaA}, faltasTacticasA={self.faltasTacticasA})"


tipo_clase_mapping = {
    "Jugadores": Jugadores,
    "Arbitros": Arbitros,
    "Evaluadores": Evaluadores,
    
    
}