






class User(Base):
    __tablename__ = "usuarios"
    ID = Column("ID",Integer, primary_key=True,autoincrement=True)
    username = Column("username", String(250), nullable = False)
    nombre = Column("nombre", String(250), nullable = False)
    apellido = Column("apellido", String(250) ,nullable = False)
    celular = Column("celular", Integer,nullable = False)
    edad = Column("edad", Integer, nullable = False)
    cedula = Column("cedula", Integer,unique=True,nullable = False)
    genero =Column("genero", String(250) ,nullable = False)
    email = Column("email", String(250), nullable = False)
    passwd = Column("passwd", String(250),nullable = False)

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
        return f"({self.ID}){self.username}{self.nombre}{self.apellido}({self.celular},{self.edad},{self.cedula}){self.genero}{self.email}{self.passwd}"
        