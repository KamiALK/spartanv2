from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Table, or_
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


usuarios_equipos = Table('usuarios_equipos', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.ID'),nullable=True),
    Column('equipo_id', Integer, ForeignKey('equipos.ID'),nullable=True)
)

class CampeonatoEquipo(Base):
    __tablename__ = "campeonatos_equipos"
    campeonato_id = Column(Integer, ForeignKey('campeonatos.ID'), primary_key=True)
    equipo_id = Column(Integer, ForeignKey('equipos.ID'), primary_key=True)
    campeonato = relationship("Campeonato", back_populates="equipos_asociados")
    equipo = relationship("Equipo", back_populates="campeonatos_asociados")

class Arbitro_asignacion_Partido(Base):
    __tablename__ = "arbitros_partidos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    partido_id = Column(Integer, ForeignKey("partidos.ID"))
    
    arbitro_1_id = Column(Integer, ForeignKey('arbitros.ID'))
    arbitro_2_id = Column(Integer, ForeignKey('arbitros.ID'))
    arbitro_3_id = Column(Integer, ForeignKey('arbitros.ID'))
    arbitro_4_id = Column(Integer, ForeignKey('arbitros.ID'))
    evaluacion_id = Column(Integer, ForeignKey("evaluaciones.ID"))  # Nueva columna para el ID de la evaluación

    partido = relationship("Partido", back_populates="arbitros")  # Corregir el nombre de la relación
    evaluacion = relationship("Evaluaciones")  
    arbitro_1 = relationship("Arbitros", foreign_keys=[arbitro_1_id])
    arbitro_2 = relationship("Arbitros", foreign_keys=[arbitro_2_id])
    arbitro_3 = relationship("Arbitros", foreign_keys=[arbitro_3_id])
    arbitro_4 = relationship("Arbitros", foreign_keys=[arbitro_4_id])




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
    ID = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250), nullable=False)
    nombre = Column(String(250), nullable=False)
    apellido = Column(String(250), nullable=False)
    celular = Column(Integer, nullable=False)
    edad = Column(Integer, nullable=False)
    cedula = Column(Integer, unique=True, nullable=False)
    genero = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    passwd = Column(String(250), nullable=False)
    evaluaciones = relationship("Evaluaciones", back_populates="evaluador")  # Corregir esta línea
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
        return f"Evaluadores(ID={self.ID}, username={self.username}, nombre={self.nombre}, apellido={self.apellido}, celular={self.celular}, edad={self.edad}, cedula={self.cedula}, genero={self.genero}, email={self.email}, passwd={self.passwd})"


class Equipo(Base):
    __tablename__ = "equipos"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(250), nullable=False)
    lider_id = Column(Integer, ForeignKey('usuarios.ID'), nullable=True)  # Campo opcional de líder
    jugadores = relationship("Jugadores", secondary=usuarios_equipos, back_populates="equipos")
    partidos_local = relationship("Partido", foreign_keys="[Partido.equipo_local_id]", back_populates="equipo_local")
    partidos_visitante = relationship("Partido", foreign_keys="[Partido.equipo_visitante_id]", back_populates="equipo_visitante")
    campeonatos_asociados = relationship("CampeonatoEquipo", back_populates="equipo")  

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return f"Equipo(ID={self.ID}, nombre={self.nombre})"


class Campeonato(Base):
    __tablename__ = "campeonatos"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(250), nullable=False)
    equipos_asociados = relationship("CampeonatoEquipo", back_populates="campeonato")
    partidos = relationship("Partido", back_populates="campeonato")

    def __init__(self, nombre):
        self.nombre = "nombre"

    def __repr__(self):
        return f"Campeonato(ID={self.ID}, nombre={self.nombre})"


class Partido(Base):
    __tablename__ = "partidos"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    campeonato_id = Column(Integer, ForeignKey('campeonatos.ID'), nullable=True)
    fecha = Column(DateTime, nullable=True)
    lugar = Column(String(250), nullable=True)
    publico_privado = Column(String(250), nullable=True)
    estado = Column(String(250), nullable=True)
    equipo_local_id = Column(Integer, ForeignKey('equipos.ID'), nullable=True)
    equipo_visitante_id = Column(Integer, ForeignKey('equipos.ID'), nullable=True)

    campeonato = relationship("Campeonato", back_populates="partidos")
    equipo_local = relationship("Equipo", foreign_keys=[equipo_local_id])
    equipo_visitante = relationship("Equipo", foreign_keys=[equipo_visitante_id])
    arbitros = relationship("Arbitro_asignacion_Partido", back_populates="partido")
    def __repr__(self):
        return f"Partido(ID={self.ID}, campeonato_id={self.campeonato_id}, fecha={self.fecha}, lugar={self.lugar}, equipo_local_id={self.equipo_local_id}, equipo_visitante_id={self.equipo_visitante_id})"


class Evaluaciones(Base):
    __tablename__ = "evaluaciones"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    arbitro_id = Column(Integer, ForeignKey('arbitros.ID'), nullable=True)
    evaluador_id = Column(Integer, ForeignKey('evaluadores.ID'), nullable=True)
    partido_id = Column(Integer, nullable=True)
    
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
    
    
    arbitro = relationship("Arbitros", foreign_keys=[arbitro_id], back_populates="evaluaciones")
    evaluador = relationship("Evaluadores", foreign_keys=[evaluador_id], back_populates="evaluaciones")  
    

    def __repr__(self):
        return f"Evaluaciones(ID={self.ID}, arbitro_id={self.arbitro_id}, evaluador_id={self.evaluador_id}, partido_id={self.partido_id})"

tipo_clase_mapping = {
    "Jugadores": Jugadores,
    "Arbitros": Arbitros,
    "Evaluadores": Evaluadores,
    
    
}