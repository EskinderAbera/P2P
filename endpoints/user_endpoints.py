from fastapi import APIRouter, HTTPException
from database import engine
from sqlmodel import Session, select
from models import User, UserCreate, UserType, Borrower, Lender, UserRegister, UserLogin, LoanWrite, Loan
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT
from repos.user_repos import select_all_users, select_user, find_user
from auth.auth import AuthHandler

user_router = APIRouter()
auth_handler = AuthHandler()

@user_router.post('/user/userCreate/')
async def userCreate(user: UserCreate):
    with Session(engine) as session:
        statement = select(User).where(User.phone_number == user.phone_number)
        getuser = session.execute(statement).first()
        
        if not getuser:
            newUser = User(phone_number=user.phone_number, userType=user.userType)
            if user.userType == UserType.borrower:
                borrower = Borrower(user=newUser)
                session.add(borrower)
                session.commit()
                session.refresh(borrower)
                return JSONResponse('success', status_code = 200)
            else:
                lender = Lender(user=newUser)
                session.add(lender)
                session.commit()
                session.refresh(lender)
                return JSONResponse('success', status_code = HTTP_201_CREATED)
        return JSONResponse("user already exist!", status_code=HTTP_409_CONFLICT)
    
@user_router.put('/user/register/')
async def userRegister(user: UserRegister):
    with Session(engine) as session:
        users = await select_all_users()
        if any(x.username == user.username for x in users):
            raise HTTPException(status_code=400, detail='Username is taken')
        us = await select_user(user.phone_number)
        hashed_pwd = auth_handler.get_password_hash(user.password)
        user.password = hashed_pwd
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(us, key, value)
        session.add(us)
        session.commit()
        statement = select(Borrower).where(Borrower.user_id == us.id)
        res = session.exec(statement).first()
        count = 0
        for key, value in res:
            if value is not None:
                count = count + 1
        res.profile_status = (count/6) * 100
        session.add(res)
        session.commit()
        return JSONResponse("success", status_code=HTTP_201_CREATED)

@user_router.post('/user/login/')
async def userLogin(user: UserLogin):
    user_found = await find_user(user.username)
    
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    with Session(engine) as session:
        statement = select(Borrower).where(Borrower.user_id == user_found.id)
        borrower = session.exec(statement).first()
        if borrower:
            res = []
            if borrower.profile_status != 100:
                for key, value in borrower:
                    if value == None:
                        res.append(key)
                session.commit()
                session.refresh(borrower.user)
                return res      
            else:
                return JSONResponse(borrower, status_code=200)
            
@user_router.post('/user/createloan/')
async def add_borrowers(loan: LoanWrite):
    with Session(engine) as session:
        loan = Loan(title=loan.title, 
                    amount=loan.amount, 
                    loanType=loan.loanType, 
                    loanDuration=loan.loanDuration, 
                    borrower_id=loan.borrower_id
                )
        session.add(loan)
        session.commit()
        session.refresh(loan)
        return JSONResponse('success', status_code = 200)
    
            
@user_router.get('/user/getloan')
async def get_borrowers():
    with Session(engine) as session:
        statement = select(Loan)
        borrowers = session.exec(statement).all()
        res = []
        ress = {}
        print(borrowers)
        for borrower in borrowers:
            ress['fullName'] = borrower.borrowers.user.username
            ress['title'] = borrower.title
            ress['loanType'] = borrower.loanType
            ress['loanDuration'] = borrower.loanDuration
            res.append(ress)
        return res