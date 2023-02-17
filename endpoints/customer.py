from fastapi import APIRouter, HTTPException, Depends
from database import session
from sqlmodel import select
from models.customer_models import CustomerCreate, Borrower, CustomerRegister, CustomerLogin, Customer, CustomerTypes, Lender,  CustomerRead
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED
from models.loan_models import Loan, LoanRead
from repos.customer_repos import select_customer, find_customer
from auth.auth import AuthHandler
from typing import List

customer_router = APIRouter()
auth_handler = AuthHandler()


@customer_router.post('/customer/create/', tags=['customers'])
async def userCreate(customer: CustomerCreate):
    statement = select(Customer).where(Customer.phone_number == customer.phone_number)
    getuser = session.execute(statement).first()

    if not getuser:
        newUser = Customer(phone_number=customer.phone_number,
                        customer_type=customer.customer_type)
        if customer.customer_type == CustomerTypes.BORROWER:
            borrower = Borrower(customer=newUser)
            session.add(borrower)
            session.commit()
            return JSONResponse('success', status_code=200)
        else:
            lender = Lender(customer=newUser)
            session.add(lender)
            session.commit()
            return JSONResponse('success', status_code=HTTP_201_CREATED)
    return JSONResponse("user already exist!", status_code=HTTP_409_CONFLICT)

@customer_router.put('/customer/register/', tags=['customers'])
async def customer_register(customer: CustomerRegister):
    check_customer = await select_customer(customer.phone_number)
    if check_customer:
        statement = select(Customer).where(Customer.username == customer.username)
        res = session.exec(statement).first()
        if res:
            raise HTTPException(status_code=HTTP_409_CONFLICT, detail="username must be unique")
        update_customer = customer.dict(exclude_unset=True)
        for key, value in update_customer.items():
            setattr(check_customer, key, value)
        hashed_pwd = auth_handler.get_password_hash(customer.password)
        check_customer.password = hashed_pwd
        session.add(check_customer)
        session.commit()
        return JSONResponse("success", status_code=HTTP_200_OK)
    else:
        return JSONResponse("user does not exist!", status_code=HTTP_404_NOT_FOUND)
    
@customer_router.post('/customer/login/', tags=['customers'])
async def customer_login(customer: CustomerLogin):
    check_customer = await find_customer(customer.username)
    if check_customer:
       verified = auth_handler.verify_password(customer.password, check_customer.password) 
       if not verified:
           raise HTTPException(status_code=401, detail='Invalid username and/or password')
       token = auth_handler.encode_token(check_customer.id)
       return {'token': token}
    return JSONResponse('Invalid username and/or password', status_code=HTTP_401_UNAUTHORIZED)

@customer_router.get('/customer/me', tags=['customers'], response_model= CustomerRead)
async def get_current_customer(customer: Customer = Depends(auth_handler.get_current_user)):
    statement = select(Customer).where(Customer.id == customer)
    return session.exec(statement).first()

@customer_router.get('/customer/loan', tags=['customers'], response_model=List[LoanRead])
async def get_customer_loans(customer: Customer = Depends(auth_handler.get_current_user)):
    statement = select(Borrower).join(Customer).where(Customer.id == customer)
    res = session.exec(statement).first()
    if res:
        statement = select(Loan).join(Borrower).where(Borrower.id == res.id)
        res = session.exec(statement).all()
        return res
    
    # return session.exec(select(Loan).where(Loan.))

    