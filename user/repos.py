from sqlmodel import Session, select
from database import engine
from .models import User
from typing import TYPE_CHECKING

# if TYPE_CHECKING:
from borrower.models import Borrower
from lender.models import Lender


async def select_all_users():
    with Session(engine) as session:
        statement = select(User)
        res = session.exec(statement).all()
        return res
    
async def select_user(phone):
    with Session(engine) as session:
        statement = select(User).where(User.phone_number == phone)
        res = session.exec(statement).first()
        return res
    
async def find_user(name):
    with Session(engine) as session:
        statement = select(User).where(User.username == name, User.isActive == True)
        return session.exec(statement).first()
    
async def get_user(name):
    with Session(engine) as session:
        statement = select(User).where(User.username == name)
        return session.exec(statement).first()
    
async def select_borrower(user):
    with Session(engine) as session:
        statement = select(Borrower).where(Borrower.user_id == user.id)
        res = session.exec(statement).first()
        count = 0
        for _, value in res:
            if value is not None:
                count = count + 1
        res.profile_status = round((count/6) * 100, 2)
        session.add(res)
        session.commit()
        return res

async def borrower_status(id):
    with Session(engine) as session:
        statement = select(Borrower).where(Borrower.user_id == id)
        borrower = session.exec(statement).first()
        res = []
        if borrower.profile_status != 100:
            for key, value in borrower:
                if value == None:
                    res.append(key)
            # session.commit()
            # session.refresh(borrower.user)
            return res