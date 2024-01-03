
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
    















    


    
