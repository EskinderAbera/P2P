from sqlmodel import SQLModel, create_engine, Session
from models.borrower_models import Borrower
from models.lender_models import Lender
from models.loan_models import LoanType, Amount, InterestRate

DB_FILE = 'db.sqlite3'
engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)
session = Session(bind=engine)
    
def create_tables():
    SQLModel.metadata.create_all(engine)
    
if __name__ == '__main__':
    create_tables()