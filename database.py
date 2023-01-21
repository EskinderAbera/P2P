from sqlmodel import SQLModel, create_engine
from user.models import User
from borrower.models import Borrower
from lender.models import Lender

DB_FILE = 'db.sqlite3'
engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)
    
def create_tables():
    SQLModel.metadata.create_all(engine)
    
if __name__ == '__main__':
    create_tables()