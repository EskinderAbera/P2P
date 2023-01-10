from sqlmodel import SQLModel, create_engine
from models import Lender, User

DB_FILE = 'db.sqlite3'
engine = create_engine(f"sqlite:///{DB_FILE}")
    
def create_tables():
    SQLModel.metadata.create_all(engine)
    
if __name__ == '__main__':
    create_tables()