from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from user.models import User

class BorrowerBase(SQLModel):
    tinNumber: Optional[str]
    maritalStatus: Optional[bool] = False
    profile_status: Optional[float] = 0.00
    address: Optional[str]
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

class Borrower(BorrowerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: Optional["User"] = Relationship(back_populates="borrower")
    