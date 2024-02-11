
#! /////////////////////////////////    CONEXION UNO   ////////////////////////////////////////

# from sqlalchemy import create_engine, MetaData

# """
# base de datos : JUGADORES
# TABLA: usuarios

# """
# from sqlalchemy import create_engine, MetaData

# engine = create_engine("mysql+pymysql://root:123@localhost:3306/JUGADORES")
# Meta_Data = MetaData()


# conn =engine.connect()
# print("conexion exitosa")

#!----------------------------------
from sqlalchemy import create_engine,  Column,  Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os



Base = declarative_base()
class Userdb(Base):
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



load_dotenv()


DB_NAME =os.getenv("DB_NAME") 
DB_HOST = os.getenv("DB_HOST")
DB_DIALECT = os.getenv("DB_DIALECT")
DB_PASSWORD =os.getenv("DB_PASSWORD")
DB_USER= os.getenv("DB_USER")



#! /////////////////////////////////    CONEXION UNO   ////////////////////////////////////////

# from sqlalchemy import create_engine, MetaData

# """
# base de datos : JUGADORES
# TABLA: usuarios

# """
# from sqlalchemy import create_engine, MetaData

# engine = create_engine("mysql+pymysql://root:172839@localhost:3306/JUGADORES")
# Meta_Data = MetaData()


# conn =engine.connect()
# print("conexion exitosa")

#!----------------------------------
from sqlalchemy import create_engine, Table, Column, Select, CHAR, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import os



Base = declarative_base()
class Userdb(Base):
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



load_dotenv()


DB_NAME =os.getenv("DB_NAME") 
DB_HOST = os.getenv("DB_HOST")
DB_DIALECT = os.getenv("DB_DIALECT")
DB_PASSWORD =os.getenv("DB_PASSWORD")
DB_USER= os.getenv("DB_USER")



# esto me lo dio chat
DB_PORT = os.getenv("DB_PORT")
URL_CONECTION = f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"



# URL_CONECTION = '{}://{}:{}@{}/{}'.format(DB_DIALECT,DB_USER,DB_PASSWORD,DB_HOST,DB_NAME)
engine = create_engine(URL_CONECTION, )
Session = sessionmaker(autoflush=False, autocommit=False,bind=engine)

Base.metadata.create_all(bind=engine)


Session.close_all()


# URL_CONECTION = '{}://{}:{}@{}/{}'.format(DB_DIALECT,DB_USER,DB_PASSWORD,DB_HOST,DB_NAME)
engine = create_engine(URL_CONECTION, )
Session = sessionmaker(autoflush=False, autocommit=False,bind=engine)

Base.metadata.create_all(bind=engine)


Session.close_all()

