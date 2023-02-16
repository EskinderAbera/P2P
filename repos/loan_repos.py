from sqlmodel import Session, select
from database import engine
from models.borrower_models import Borrower
from models.lender_models import Lender
from models.loan_models import Loan

async def check_loan(loantype):
    with Session(engine) as session:
        statement = select(Loan).where(Loan.id == loantype)
        res = session.exec(statement).first()
        return res