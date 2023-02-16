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
    
async def select_customers(username):
    borrowers = await select_borrowers()
    lenders = await select_lenders()
    
    if any(lender.username == username for lender in lenders):
        return {"userType": "LENDER"}
    
    elif any(borrower.username == username for borrower in borrowers):
        return {"userType": "BORROWER"}
    else: 
        return {"userType": "wrong"}