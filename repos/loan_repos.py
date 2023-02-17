from sqlmodel import Session, select
from database import engine
from models.customer_models import Borrower, Lender
from models.loan_models import Amount, InterestRate, Loan, LoanType

async def check_loan(loan):
    with Session(engine) as session:
       
        statement = select(InterestRate).join(LoanType).where(LoanType.id == loan.loantype_id)
        res = session.exec(statement).first()
        if loan.interest_rate < res.min or loan.interest_rate > res.max:
            return {"error": "interest"}
        statement = select(Amount).join(LoanType).where(LoanType.id == loan.loantype_id)
        res = session.exec(statement).first()
        if loan.amount < res.min or loan.amount > res.max:
            return {"error": "amount"}
        statement = select(Loan).where(Loan.loantype_id == loan.loantype_id)
        res = session.exec(statement).first()
        if res:
            return {"error": "exist"}
        else:
            return {"error": "success"}