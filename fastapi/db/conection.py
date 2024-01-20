
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
from sqlalchemy import create_engine,Table, Column, Select,CHAR,Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


Base =declarative_base()


class User(Base):
    __tablename__ = "usuarios"
    ID = Column("ID",Integer, primary_key=True,autoincrement=True)
    username = Column("username", String, nullable = False)
    nombre = Column("nombre", String, nullable = False)
    apellido = Column("apellido", String ,nullable = False)
    celular = Column("celular", Integer,nullable = False)
    edad = Column("edad", Integer, nullable = False)
    cedula = Column("cedula", Integer,nullable = False)
    genero =Column("genero", CHAR)
    email = Column("email", String, nullable = False)
    passwd = Column("passwd", String,nullable = False)

    def __init__(self,ID,username,nombre,apellido,celular,edad,cedula,genero,email,passwd):
        self.ID =ID
        self.username =username
        self.nombre = nombre
        self.apellido = apellido
        self.celular = celular
        self.edad=edad
        self.cedula= cedula
        self.genero = genero
        self.email= email
        self.passwd =passwd
    def __repr__(self):
        return f"({self.ID}){self.username}{self.nombre}{self.apellido}({self.celular},{self.edad},{self.cedula},{self.genero}){self.email}{self.passwd}"
        
URL_CONECTION='mysql+pymysql://root:172839@localhost:3306/JUGADORES'
engine=create_engine(URL_CONECTION,echo=True)  
Base.metadata.create_all(bind=engine)
LocalSession =sessionmaker(autoflush=False, autocommit=False,bing=engine)
session= LocalSession()


person =User(1,"andresito","andres","almanza",3143513617,31,1024,"M","andy@ffg",123)
session.add(person)
session.commit()
