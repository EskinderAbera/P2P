from fastapi import APIRouter, HTTPException
from database import session
from sqlmodel import select
from models.borrower_models import CustomerCreate, Borrower, CustomerRegister, CustomerLogin
from models.lender_models import Lender
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT
from repos.customer_repos import select_borrower, select_lender, select_customers
from auth.auth import AuthHandler

customer_router = APIRouter()
auth_handler = AuthHandler()


@customer_router.post('/customer/create/', tags=['customers'])
async def customer_create(customer: CustomerCreate):
    if customer.customer_type == 'BORROWER':
        statement = select(Borrower).where(Borrower.phone_number == customer.phone_number)
        get_user = session.execute(statement).first()
        
        if not get_user:
            new_borrower = Borrower(phone_number=customer.phone_number, customer_type=customer.customer_type)
            session.add(new_borrower)
            session.commit()
            return JSONResponse('success', status_code = 200)
        else:
           return JSONResponse("user already exist!", status_code=HTTP_409_CONFLICT)
       
    else: 
        statement = select(Lender).where(Lender.phone_number == customer.phone_number)
        get_user = session.execute(statement).first()
        
        if not get_user:
            new_lender = Lender(phone_number=customer.phone_number, customer_type=customer.customer_type)
            session.add(new_lender)
            session.commit()
            return JSONResponse('success', status_code = 200)
        else:
            return JSONResponse("user already exist!", status_code=HTTP_409_CONFLICT) 
        

@customer_router.put('/borrower/register/', tags=['customers'])
async def borrower_register(customer: CustomerRegister):
    borrow = await select_customers(customer)
    
    if borrow:
        raise HTTPException(status_code=400, detail="email and username must be unique")
        
    borrower = await select_borrower(customer.phone_number)
    update_borrower = customer.dict(exclude_unset=True)
    for key, value in update_borrower.items():
        setattr(borrower, key, value)
    hashed_pwd = auth_handler.get_password_hash(customer.password)
    borrower.password = hashed_pwd
    session.add(borrower)
    session.commit()
    return JSONResponse("success", status_code=HTTP_201_CREATED)

@customer_router.put('/lender/register/', tags=['customers'])
async def lender_register(customer: CustomerRegister):
    lender = await select_customers(customer)
    
    if lender:
        raise HTTPException(status_code=400, detail="email and username must be unique")
       
    lender = await select_lender(customer.phone_number)
    update_lender = customer.dict(exclude_unset=True)
    for key, value in update_lender.items():
        setattr(lender, key, value)
    hashed_pwd = auth_handler.get_password_hash(customer.password)
    lender.password = hashed_pwd
    session.add(lender)
    session.commit()
    return JSONResponse("success", status_code=HTTP_201_CREATED)

@customer_router.post('/customer/login/', tags=['customers'])
async def login(customer: CustomerLogin):
    borrower = await select_customers(customer)
    if borrower["userType"] == "BORROWER":
        statement = select(Borrower).where(Borrower.username==customer.username)
        res = session.exec(statement).first()
        verified = auth_handler.verify_password(customer.password, res.password)
        if not verified:
            raise HTTPException(status_code=401, detail='Invalid username and/or password')
        return JSONResponse("success", status_code=HTTP_201_CREATED)
    elif borrower["userType"] == "LENDER":
        statement = select(Lender).where(Lender.username==customer.username)
        res = session.exec(statement).first()
        verified = auth_handler.verify_password(customer.password, res.password)
        if not verified:
            raise HTTPException(status_code=401, detail='Invalid username and/or password')
        return JSONResponse("success", status_code=HTTP_201_CREATED)
    else:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
        
# @user_router.post('/user/userCreate/')
# async def userCreate(user: UserCreate):
#     with Session(engine) as session:
#         statement = select(User).where(User.phone_number == user.phone_number)
#         getuser = session.execute(statement).first()
        
#         if not getuser:
#             newUser = User(phone_number=user.phone_number, userType=user.userType)
#             if user.userType == UserType.borrower:
#                 borrower = Borrower(user=newUser)
#                 session.add(borrower)
#                 session.commit()
#                 session.refresh(borrower)
#                 return JSONResponse('success', status_code = 200)
#             else:
#                 lender = Lender(user=newUser)
#                 session.add(lender)
#                 session.commit()
#                 session.refresh(lender)
#                 return JSONResponse('success', status_code = HTTP_201_CREATED)
#         return JSONResponse("user already exist!", status_code=HTTP_409_CONFLICT)
    
# @user_router.put('/user/register/')
# async def userRegister(user: UserRegister):
#     with Session(engine) as session:
#         users = await select_all_users()
#         if any(x.username == user.username for x in users):
#             raise HTTPException(status_code=400, detail='Username is taken')
#         us = await select_user(user.phone_number)
#         hashed_pwd = auth_handler.get_password_hash(user.password)
#         user.password = hashed_pwd
#         user_data = user.dict(exclude_unset=True)
#         for key, value in user_data.items():
#             setattr(us, key, value)
#         session.add(us)
#         session.commit()
#         statement = select(Borrower).where(Borrower.user_id == us.id)
#         res = session.exec(statement).first()
#         count = 0
#         for key, value in res:
#             if value is not None:
#                 count = count + 1
#         res.profile_status = (count/6) * 100
#         session.add(res)
#         session.commit()
#         return JSONResponse("success", status_code=HTTP_201_CREATED)

# @user_router.post('/user/login/')
# async def userLogin(user: UserLogin):
#     user_found = await find_user(user.username)
    
#     if not user_found:
#         raise HTTPException(status_code=401, detail='Invalid username and/or password')
#     verified = auth_handler.verify_password(user.password, user_found.password)
#     if not verified:
#         raise HTTPException(status_code=401, detail='Invalid username and/or password')
#     with Session(engine) as session:
#         statement = select(Borrower).where(Borrower.user_id == user_found.id)
#         borrower = session.exec(statement).first()
#         if borrower:
#             res = []
#             if borrower.profile_status != 100:
#                 for key, value in borrower:
#                     if value == None:
#                         res.append(key)
#                 session.commit()
#                 session.refresh(borrower.user)
#                 return res      
#             else:
#                 return JSONResponse(borrower, status_code=200)
            
# @user_router.post('/user/createloan/')
# async def add_borrowers(loan: LoanWrite):
#     with Session(engine) as session:
#         loan = Loan(title=loan.title, 
#                     amount=loan.amount, 
#                     loanType=loan.loanType, 
#                     loanDuration=loan.loanDuration, 
#                     borrower_id=loan.borrower_id
#                 )
#         session.add(loan)
#         session.commit()
#         session.refresh(loan)
#         return JSONResponse('success', status_code = 200)
    
            
# @user_router.get('/user/getloan')
# async def get_borrowers():
#     with Session(engine) as session:
#         statement = select(Loan)
#         borrowers = session.exec(statement).all()
#         res = []
#         ress = {}
#         for borrower in borrowers:
#             ress['fullName'] = borrower.borrowers.user.username
#             ress['title'] = borrower.title
#             ress['loanType'] = borrower.loanType
#             ress['loanDuration'] = borrower.loanDuration
#             res.append(ress)
#         return res