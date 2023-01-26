from internaluser.models import InternalUser, CreateInternalUser, Login
from fastapi import APIRouter, HTTPException
from auth.auth import AuthHandler
from internaluser.models import CreateInternalUser, InternalUser
from .repos import select_all_users, select_user
from database import session
from starlette.responses import JSONResponse

int_user = APIRouter()
auth_handler = AuthHandler()

@int_user.post("/internal/createuser/")
async def create_user(user: CreateInternalUser):
    users = await select_all_users()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail="user with this username exist!")
    hashed_password = auth_handler.get_password_hash(user.password)
    us = InternalUser(username=user.username, user_role=user.user_role, password=hashed_password)
    session.add(us)
    session.commit()
    return JSONResponse('success', status_code = 200)
    
@int_user.post("/internal/login/")
async def login(user: Login):
    us = await select_user(user.username)
    if not us:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    
    verified = auth_handler.verify_password(user.password, us.password)
    
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    
    token = auth_handler.encode_token(us.username)
    return {'token' : token}
