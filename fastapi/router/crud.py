from sqlalchemy.orm import session
from model.users import User
from schema.user_schema import User


def get_user(db:session):
    return db.query(User).all()

def get_user(db:session):
    return db.query(User).filter(User.id==id).first()
def get_user_by_name(db:session,name:str):
    return db.query(User).filter(User.name==name).first()
def create_user(db:session,user:User)
    