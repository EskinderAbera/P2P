from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from typing import Optional, TYPE_CHECKING
from enum import Enum as Enum_

if TYPE_CHECKING:
    from models.loan_models import Loan


class Enum(Enum_):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))


class CustomerTypes(str, Enum):
    BORROWER = 'BORROWER'
    LENDER = 'LENDER'

class CustomerBase(SQLModel):
    full_name: Optional[str]
    phone_number: Optional[str]
    email: Optional[EmailStr]
    is_active: bool = False
    username: Optional[str]
    password: Optional[str]
    customer_type: CustomerTypes = CustomerTypes.BORROWER
    

class Borrower(CustomerBase, table=True):
    id: Optional[int] = Field(default = None, primary_key = True)
    country: Optional[str] = "Ethiopia"
    city: Optional[str]
    credit_score: Optional[float] = 0.0
    profile_status: Optional[float] = 0.0
    isMarried: Optional[bool] = False
    loan: Optional["Loan"] = Relationship(sa_relationship_kwargs={'uselist':False}, back_populates="borrower")
    

class CustomerCreate(SQLModel):
    customer_type: CustomerTypes
    phone_number: str
    
class CustomerRegister(SQLModel):
    email: EmailStr
    phone_number: str
    username: str
    password: str
    
class CustomerLogin(SQLModel):
    username: str
    password: str
    
class BorrowerRead(CustomerBase):
    id: int
    country: str
    city: Optional[str]
    credit_score: float
    isMarried: bool