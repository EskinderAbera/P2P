from fastapi import APIRouter, HTTPException
from database import session
from models.borrower_models import CustomerCreate
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from repos.customer_repos import select_borrower, select_lender
from auth.auth import AuthHandler

user_router = APIRouter()
auth_handler = AuthHandler()

@user_router.put('/customer/activate/', tags=['users'])
async def activate_customer(customer: CustomerCreate):
    if customer.customer_type == 'BORROWER':
        borrower = await select_borrower(customer.phone_number)
        if not borrower:
            raise HTTPException(status_code=404, detail="user does not exist")
        borrower.is_active = True
        session.add(borrower)
        session.commit()
        return JSONResponse("success", status_code=HTTP_200_OK)
    elif customer.customer_type == 'LENDER':
        lender = await select_lender(customer.phone_number)
        lender.is_active = True
        session.add(lender)
        session.commit()
        return JSONResponse("success", status_code=HTTP_200_OK)
    else:
        return JSONResponse("wrong user", status_code=HTTP_400_BAD_REQUEST)
        
    