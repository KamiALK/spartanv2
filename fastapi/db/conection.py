


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
from model.Userdb import Base#todo lo referente a la base de datos
load_dotenv()
DB_NAME =os.getenv("DB_NAME") 
DB_HOST = os.getenv("DB_HOST")
DB_DIALECT = os.getenv("DB_DIALECT")
DB_PASSWORD =os.getenv("DB_PASSWORD")
DB_USER= os.getenv("DB_USER")
DB_PORT = os.getenv("DB_PORT")


#todo lo referente a la conexion
URL_CONECTION = f"{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(URL_CONECTION, )
Session = sessionmaker(autoflush=False, autocommit=False,bind=engine)




Base.metadata.create_all(bind=engine)
Session.close_all()


