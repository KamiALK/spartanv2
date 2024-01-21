from sqlalchemy.orm import session
from model.users import User
from schema.user_schema import User


# def get_users(db:session):
#     return db.query(User).all()

# def get_user(db:session):
#     return db.query(User).filter(User.id==id).first()
# def get_user_by_name(db:session,name:str):
#     return db.query(User).filter(User.name==name).first()
# def create_user(db:session,user:User):
#     #aqui va la contraseña
#     passwdf = "contraseña encriptada"
#     new_user=User(name=user.name,password=passwdf)
#     db.add(new_user)
#     db.commit()
#     db.flush(new_user)
#     return new_user
    
    