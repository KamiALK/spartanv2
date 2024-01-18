
#! /////////////////////////////////    CONEXION UNO   ////////////////////////////////////////

from sqlalchemy import create_engine, MetaData

"""
base de datos : JUGADORES
TABLA: usuarios

"""
from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:123456@localhost:3306/JUGADORES")
Meta_Data = MetaData()
    
    
conn =engine.connect()
print("conexion exitosa")

#!----------------------------------   
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_CONECTION='mysql+pymysql://root:123456@localhost:3306/JUGADORES'
engine=create_engine(URL_CONECTION)
LocalSession =sessionmaker(autoflush=False, autocommit=False,bing=engine)
Base =declarative_base()

    















    


    
