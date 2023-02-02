from sqlmodel import Session, select
from database import engine
from models.borrower_models import Borrower
from models.lender_models import Lender


async def select_borrower(phone_number):
    with Session(engine) as session:
        statement = select(Borrower).where(Borrower.phone_number == phone_number)
        res = session.exec(statement).first()
        return res
    
async def select_borrowers():
     with Session(engine) as session:
        statement = select(Borrower)
        res = session.exec(statement).all()
        return res
    
async def select_lender(phone_number):
    with Session(engine) as session:
        statement = select(Lender).where(Lender.phone_number == phone_number)
        res = session.exec(statement).first()
        return res
    
async def select_lenders():
     with Session(engine) as session:
        statement = select(Lender)
        res = session.exec(statement).all()
        return res

# async def select_all_users():
#     with Session(engine) as session:
#         statement = select(User)
#         res = session.exec(statement).all()
#         return res
    
# async def select_user(phone):
#     with Session(engine) as session:
#         statement = select(User).where(User.phone_number == phone)
#         res = session.exec(statement).first()
#         return res
    
# async def find_user(name):
#     with Session(engine) as session:
#         statement = select(User).where(User.username == name)
#         return session.exec(statement).first()
    
# async def find_borrower(user_id):
#     with Session(engine) as session:
#         statement = select(Borrower).where(Borrower.user_id == user_id)
#         res = session.exec(statement).first()
#         return res