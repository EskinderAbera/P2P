from fastapi import APIRouter, HTTPException
from database import engine
from sqlmodel import Session, select
from .models import *
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT
from .repos import *
from auth.auth import AuthHandler
from borrower.models import Borrower
from lender.models import Lender
from typing import List

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
                Borrower(user=newUser)
            else:
                Lender(user=newUser)
            session.add(newUser)
            session.commit()
            return JSONResponse('success', status_code = 200)
        return JSONResponse("user already exist!", status_code=HTTP_409_CONFLICT)
    
@user_router.put('/user/register/')
async def userRegister(user: UserRegister):
    with Session(engine) as session:
        users = await select_all_users()
        if any(x.username == user.username or x.email == user.email for x in users):
            raise HTTPException(status_code=400, detail='Username/email is taken')
        us = await select_user(user.phone_number)
        hashed_pwd = auth_handler.get_password_hash(user.password)
        user.password = hashed_pwd
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(us, key, value)
        session.add(us)
        session.commit()
        session.refresh(us)
        if us.userType == "borrower":
            await select_borrower(us)
        return JSONResponse("success", status_code=HTTP_201_CREATED)
    
@user_router.post('/user/login/')
async def login(user: UserLogin):
    user_found = await find_user(user.username)    
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = auth_handler.verify_password(user.password, user_found.password)
    
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    if user_found.userType == "borrower":
        empty_field = await borrower_status(user_found.id)
        return JSONResponse(empty_field, status_code=200)
    return JSONResponse("success", status_code=200)

@user_router.put('/user/activate/')
async def activate_user(user: UserActivate):
    with Session(engine) as session:
        user_found = await get_user(user.username)
        if not user_found:
            raise HTTPException(status_code=401, detail='User does not exist!')
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(user_found, key, value)
        session.add(user_found)
        session.commit()
        return JSONResponse("success", status_code=200)

@user_router.get('/user/users', response_model=List[User])
async def all_user():
    users = await select_all_users()
    return users
                
    