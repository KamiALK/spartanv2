from sqlalchemy import Table, column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import engine, Meta_Data


users = table("users", Meta_Data, 
              column("id", Integer, primary_key = True),
              column("username",String(255),nullable = False),
              column("name", String(255), nullable = False),
              column("apellido",String(255),nullable = False),
              column("celular", Integer(255),nullable = False),
              column("edad", Integer(255),nullable = False),
              column("password", String(255),nullable = False),
              column("password", String(255),nullable = False),
              column("email", String(255), nullable = False))

Meta_Data.create_all(engine)