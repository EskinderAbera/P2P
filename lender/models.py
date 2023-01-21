from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from user.models import User

class LenderBase(SQLModel):
    address: Optional[str]
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

class Lender(LenderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user:  Optional["User"] = Relationship(back_populates="lender")