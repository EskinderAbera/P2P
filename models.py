# from typing import Optional
# from enum import Enum
# from sqlmodel import Field, Relationship, SQLModel
# from pydantic import EmailStr





    

         
# class BorrowerBase(SQLModel):
#     tinNumber: Optional[str]
#     maritalStatus: Optional[bool] = False
#     profile_status: Optional[float] = 0.00
#     address: Optional[str]
#     user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    
# class Borrower(BorrowerBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     user: Optional[User] = Relationship(back_populates="borrower")
#     loan: Optional["Loan"] = Relationship(back_populates="borrowers")
    
# class Lender(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     address: Optional[str]
#     user_id: Optional[int] = Field(default=None, foreign_key="user.id")
#     user: Optional[User] = Relationship(back_populates="lender")
          

    

    

 
# class BorrowerRead(BorrowerBase):
#     id: int
    
# # class UserRead(UserBase):
# #     id: int
    
# # class UserWithType(UserRead):
# #     borrower: Optional[BorrowerRead] = None
    
# class BorrowerWithType(BorrowerRead):
#     user: Optional[UserRead] = None

# class UserStatus(SQLModel):
#     id: int

# class LoanType(str, Enum):
#     construction = "construction"
#     personal = "personal"
#     mortgage = "mortgage"

# class LoanBase(SQLModel):
#     title: Optional[str]
#     amount: Optional[int]
#     loanType: Optional[LoanType] = LoanType.construction
#     loanDuration: Optional[str]
#     borrower_id: Optional[int] = Field(default=None, foreign_key="borrower.id")
    
# class InterestBase(SQLModel):
#     minimum: Optional[float]
#     maximum: Optional[float]
#     interestType: Optional[LoanType]
#     interest_rate: Optional[float]
    
# class Loan(LoanBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     borrowers: Optional[Borrower] = Relationship(back_populates="loan")
    
# class LoanRead(LoanBase):
#     id: int
    
# class LoanWrite(LoanBase):
#     pass
    