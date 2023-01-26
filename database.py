from sqlmodel import SQLModel, create_engine, Session
from user.models import User
from borrower.models import Borrower
from lender.models import Lender
from internaluser.models import InternalUser

DB_FILE = 'db.sqlite3'
engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)
session = Session(bind=engine)
    
def create_tables():
    SQLModel.metadata.create_all(engine)
    
if __name__ == '__main__':
    create_tables()