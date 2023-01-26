from sqlmodel import Session, select
from database import engine
from .models import InternalUser

async def select_all_users():
    with Session(engine) as session:
        statement = select(InternalUser)
        res = session.exec(statement).all()
        return res
    
async def select_user(username):
    with Session(engine) as session:
        statement = select(InternalUser).where(InternalUser.username == username)
        res = session.exec(statement).first()
        return res