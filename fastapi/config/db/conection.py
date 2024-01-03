
#! /////////////////////////////////    CONEXION UNO   ////////////////////////////////////////

from sqlalchemy import create_engine, MetaData


try:

    engine = create_engine("mysql+pymysql://root:123456@localhost:3306/JUGADORES")
    Meta_Data = MetaData()
    
    
    conn =engine.connect()
    print("conexion exitosa")
    
except Exception as ex:
    print(ex)














    


    
