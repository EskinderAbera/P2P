from typing import List, Optional
from enum import Enum
from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr


class GenderType(str, Enum):
    male="male"
    female="female"
    
class UserType(str, Enum):
    borrower = "borrower"
    lender = "lender"

class UserBase(SQLModel):
    fullName: Optional[str]
    gender: Optional[GenderType] = GenderType.male
    userType: Optional[UserType]
    email: Optional[EmailStr]
    isActive: Optional[bool] = False
    phone_number: str
    username: Optional[str] = Field(index=True)
    password: Optional[str] = Field(max_length=256, min_length=4)
    motherName: Optional[str]
    
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    borrower: Optional["Borrower"] = Relationship(back_populates="user")
    lender: Optional["Lender"] = Relationship(back_populates="user")
         
class BorrowerBase(SQLModel):
    tinNumber: Optional[str]
    maritalStatus: Optional[bool] = False
    profile_status: Optional[float] = 0.00
    address: Optional[str]
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
class Borrower(BorrowerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: Optional[User] = Relationship(back_populates="borrower")
    loan: Optional["Loan"] = Relationship(back_populates="borrowers")
    
class Lender(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    address: Optional[str]
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="lender")
          
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

    
class BorrowerRead(BorrowerBase):
    id: int
    

class UserRead(UserBase):
    id: int
    
class UserWithType(UserRead):
    borrower: Optional[BorrowerRead] = None
    
class BorrowerWithType(BorrowerRead):
    user: Optional[UserRead] = None

class UserStatus(SQLModel):
    id: int

class LoanType(str, Enum):
    construction = "construction"
    personal = "personal"
    mortgage = "mortgage"

class LoanBase(SQLModel):
    title: Optional[str]
    amount: Optional[int]
    loanType: Optional[LoanType] = LoanType.construction
    loanDuration: Optional[str]
    borrower_id: Optional[int] = Field(default=None, foreign_key="borrower.id")
    
class Loan(LoanBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    borrowers: Optional[Borrower] = Relationship(back_populates="loan")
    
class LoanRead(LoanBase):
    id: int
    
class LoanWrite(LoanBase):
    pass