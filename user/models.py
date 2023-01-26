from typing import Optional, TYPE_CHECKING, List
from enum import Enum
from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr
from sqlalchemy import UniqueConstraint

# if TYPE_CHECKING:
from borrower.models import Borrower, BorrowerRead
from lender.models import Lender, LenderRead

class GenderType(str, Enum):
    male="male"
    female="female"
    
class UserType(str, Enum):
    borrower = "borrower"
    lender = "lender"
    
class UserBase(SQLModel):
    __table_args__ = (UniqueConstraint("phone_number"),)
    fullName: Optional[str]
    gender: Optional[GenderType] = GenderType.male
    userType: Optional[UserType]
    email: Optional[EmailStr]
    isActive: Optional[bool] = False
    phone_number: str = Field(index=True)
    username: Optional[str] = Field(index=True)
    password: Optional[str] = Field(max_length=256, min_length=4)
    motherName: Optional[str]
    
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    borrower: Optional["Borrower"] = Relationship(back_populates="user")
    lender: Optional["Lender"] = Relationship(back_populates="user")
    
class UserCreate(SQLModel):
    phone_number: str
    userType: UserType 
    
class UserRegister(SQLModel):
    username: str
    email: EmailStr
    phone_number: str
    password: str = Field(max_length=256, min_length=4)
    
class UserLogin(SQLModel):
    username: str
    password: str = Field(max_length=256, min_length=4) 
    
class UserActivate(SQLModel):
    isActive: bool
    username: str
    
class UserRead(SQLModel):
    id: Optional[int]
    fullName: Optional[str]
    gender: Optional[GenderType]
    userType: Optional[UserType]
    email: Optional[EmailStr]
    isActive: Optional[bool]
    phone_number: str
    username: Optional[str]
    motherName: Optional[str]

class UserDetail(UserRead):
    id: Optional[int]
    borrower: List[BorrowerRead]
    lender: List[LenderRead]