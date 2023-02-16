from fastapi import APIRouter, HTTPException
from sqlmodel import select
from database import session
from models.loan_models import *
from auth.auth import AuthHandler
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT
from starlette.responses import JSONResponse
from typing import List
from repos.loan_repos import check_loan

loan_router = APIRouter()
auth_handler = AuthHandler()

@loan_router.post("/loan/loantype/", tags=['loans'])
async def create_loantype(loantype: LoanTypeCreate):
    statement = select(LoanType).where(LoanType.name == loantype.name)
    res = session.exec(statement).first()
    if res:
        raise HTTPException(detail="Loan Type already exist!", status_code=HTTP_409_CONFLICT)
    loan_type = LoanType(name=loantype.name)
    session.add(loan_type)
    session.commit()
    return JSONResponse("success", status_code=HTTP_201_CREATED)

@loan_router.post("/loan/interestrate/", tags=['loans'])
async def create_interest(interesttype: InterestTypeCreate):
    statement = select(InterestRate).where(InterestRate.loantype_id == interesttype.loantype_id)
    res = session.exec(statement).first()
    if res:
        raise HTTPException(detail="Interest Rate exist!", status_code=HTTP_409_CONFLICT)
    interest = InterestRate(min=interesttype.min, max=interesttype.max, loantype_id=interesttype.loantype_id)
    session.add(interest)
    session.commit()
    return JSONResponse("success", status_code=HTTP_201_CREATED)

@loan_router.post("/loan/amount/", tags=['loans'])
async def create_amount(amount: CreateAmount):
    statement = select(Amount).where(Amount.loantype_id == amount.loantype_id)
    res = session.exec(statement).first()
    if res:
        raise HTTPException(detail="Amount Rate exist!", status_code=HTTP_409_CONFLICT)
    amount = Amount(min=amount.min, max=amount.max, loantype_id=amount.loantype_id)
    session.add(amount)
    session.commit()
    return JSONResponse("success", status_code=HTTP_201_CREATED)

@loan_router.get("/loan/getloan", tags=['loans'], response_model=List[LoanTypeRead])
async def get_loantype():
    statement = select(LoanType)
    res = session.exec(statement).all()
    return res

@loan_router.get("/loan/getamount", tags=['loans'], response_model=List[AmountRead])
async def get_loantype():
    statement = select(Amount)
    res = session.exec(statement).all()
    return res

@loan_router.get("/loan/getinterest", tags=['loans'], response_model=List[InterestRateRead])
async def get_loantype():
    statement = select(InterestRate)
    res = session.exec(statement).all()
    return res

@loan_router.post("/loan/create/", tags=['loans'])
async def create_loan(loan: LoanCreate):
    lo = await check_loan(loan.loantype_id)
    if lo:
        raise HTTPException(detail="Loan Exist!", status_code=HTTP_409_CONFLICT)
    loan_db = Loan.from_orm(loan)
    session.add(loan_db)
    session.commit()
    return JSONResponse("success", status_code=HTTP_201_CREATED)

@loan_router.get("/loan/getloans", tags=['loans'], response_model=List[LoanRead])
async def get_loans():
    loans = session.exec(select(Loan)).all()
    return loans
    