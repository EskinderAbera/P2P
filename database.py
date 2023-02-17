from sqlmodel import SQLModel, create_engine, Session
from models.customer_models import Borrower, Customer, Lender
from models.loan_models import LoanType, Amount, InterestRate

DB_FILE = 'db.sqlite3'
engine = create_engine(f"sqlite:///{DB_FILE}")
session = Session(bind=engine)
    
def create_tables():
    SQLModel.metadata.create_all(engine)
    
if __name__ == '__main__':
    create_tables()