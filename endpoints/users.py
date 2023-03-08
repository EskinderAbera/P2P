from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select
from database import session
from models.customer_models import CustomerCreate, Customer, CustomerRead
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from auth.auth import AuthHandler

user_router = APIRouter()
auth_handler = AuthHandler()

@user_router.get('/customers/all', tags=['users'], response_model=List[CustomerRead])
async def customers():
    # if user:
    customers = session.exec(select(Customer)).all()
    return customers
        
    