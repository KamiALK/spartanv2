from sqlalchemy import Table, Column, Select
from sqlalchemy.sql.sqltypes import Integer, String
from db.conection import engine, Meta_Data, MetaData


users = Table("usuarios", Meta_Data, 
              Column("id", Integer, nullable = False),
              Column("username", String(255), nullable = False),
              Column("nombre", String(255), nullable = False),
              Column("apellido",String (255),nullable = False),
              Column("celular", Integer,nullable = False),
              Column("edad", Integer, nullable = False),
              Column("cedula", Integer,primary_key = True ),
              Column("passwd", String(255),nullable = False),
              Column("email", String(255), nullable = False))

usersdos = Table("usuarios", Meta_Data, autoload_with=engine)
query = Select(users)




Meta_Data.create_all(engine)
