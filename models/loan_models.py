from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING, List
from enum import Enum as Enum_

if TYPE_CHECKING:
    from models.borrower_models import Borrower
    
    
class Enum(Enum_):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
    
class Status(str, Enum):
    pending = 'pending'
    active = 'active'
    funding = 'funding'
    completed = 'completed'
    paid = 'paid'
    
class InterestBase(SQLModel):
    min: float = 0.0
    max: float = 0.0
       
class InterestRate(InterestBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    loantypes: Optional["LoanType"] = Relationship(sa_relationship_kwargs={'uselist': False}, back_populates="interestrate")
    
class AmountBase(SQLModel):
    min: float = 0.0
    max: float = 0.0
    
class Amount(AmountBase, table = True):
    id: Optional[int] = Field(default=None, primary_key=True)
    loantype: Optional["LoanType"] = Relationship(sa_relationship_kwargs={'uselist':False}, back_populates="amount")
    
class LoanTypeBase(SQLModel):
    name: str
    interestrate_id: Optional[int] = Field(default=None, foreign_key="interestrate.id")
    amount_id: Optional[int] = Field(default=None, foreign_key="amount.id")

class LoanType(LoanTypeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    interestrate: Optional[InterestRate] = Relationship(back_populates="loantypes")
    amount: Optional[Amount] = Relationship(back_populates="loantype")
    loans: List["Loan"] = Relationship(back_populates="loantype")
    
class LoanBase(SQLModel):
    title: str
    description: str
    tin_no: str
    marital_status: bool = False
    image: Optional[str]
    video: Optional[str]
    interest_rate: float = 0.0
    amount: int = 0.0
    duration: str
    status: Status = Status.pending
    borrower_id: Optional[int] = Field(default=None, foreign_key="borrower.id")
    loantype_id: Optional[int] = Field(default=None, foreign_key="loantype.id")
    
class Loan(LoanBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    borrower: Optional["Borrower"] = Relationship(back_populates="loan")
    loantype: Optional[LoanType] = Relationship(back_populates="loans")
    
    
