from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from typing import Optional, TYPE_CHECKING, List
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
    
class GenderType(str, Enum):
    male="male"
    female="female"

class CustomerBase(SQLModel):
    full_name: Optional[str]
    gender: Optional[GenderType] = GenderType.male
    is_active: bool = False
    motherName: Optional[str]
    country: Optional[str] = "Ethiopia"
    city: Optional[str]
    customer_type: CustomerTypes = CustomerTypes.BORROWER
    phone_number: Optional[str]
    email: Optional[EmailStr]
    username: Optional[str]
    password: Optional[str]
    
class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    borrower: Optional["Borrower"] = Relationship(back_populates="customer")
    lender: Optional["Lender"] = Relationship(back_populates="customer")
    
class BorrowerBase(SQLModel):
    tinNumber: Optional[str]
    maritalStatus: Optional[bool] = False
    profile_status: Optional[float] = 0.00
    address: Optional[str]
    isMarried: Optional[bool] = False
    credit_score: Optional[float] = 0.0
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")

class Borrower(BorrowerBase, table=True):
    id: Optional[int] = Field(default = None, primary_key = True)
    customer: Optional[Customer] = Relationship(sa_relationship_kwargs={'uselist':False}, back_populates="borrower")
    loan: Optional["Loan"] = Relationship(sa_relationship_kwargs={'uselist':False}, back_populates="borrower")

class Lender(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    address: Optional[str]
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")
    customer: Optional[Customer] = Relationship(sa_relationship_kwargs={'uselist':False}, back_populates="lender")

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
    
class CustomerRead(SQLModel):
    id: int
    email: EmailStr
    phone_number: str
    username: str
    full_name: Optional[str]
    gender: Optional[GenderType]
    is_active: bool = False
    motherName: Optional[str]
    country: Optional[str]
    city: Optional[str]
    customer_type: Optional[CustomerTypes]
    borrower: List[Borrower]
    lender: List[Lender]
    
class CustomerForLoans(SQLModel):
    id: int
    email: EmailStr
    phone_number: str
    username: str
    full_name: Optional[str]
    gender: Optional[GenderType]
    is_active: bool = False
    motherName: Optional[str]
    country: Optional[str]
    city: Optional[str]
      
class BorrowerReadForLoans(BorrowerBase):
    id: int
    customer: CustomerForLoans  

class BorrowerRead(BorrowerBase):
    id: int
    customer: CustomerRead