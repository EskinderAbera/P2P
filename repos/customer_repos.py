from sqlmodel import Session, select
from database import engine
from models.customer_models import Borrower, Customer
from database import session

async def select_all_customers():
    with Session(engine) as session:
        statement = select(Customer)
        res = session.exec(statement).all()
        return res
    
async def select_customer(phone):
    with Session(engine) as session:
        statement = select(Customer).where(Customer.phone_number == phone)
        res = session.exec(statement).first()
        return res
    
async def find_customer(username):
    statement = select(Customer).where(Customer.username == username)
    res = session.exec(statement).first()
    return res
    
# async def find_borrower(user_id):
#     with Session(engine) as session:
#         statement = select(Borrower).where(Borrower.customer_id == user_id)
#         res = session.exec(statement).first()
#         return res