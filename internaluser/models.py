from typing import Optional
from enum import Enum
from sqlmodel import Field, SQLModel

class UserRole(str, Enum):
    superadmin = "superadmin"
    admin = "admin"
    loan_officer = "loan_officer"
    customer_exp = "customer_exp"
    
class InternalUserBase(SQLModel):
    user_role: UserRole
    username: str
    password: str

class InternalUser(InternalUserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class CreateInternalUser(InternalUserBase):
    pass

class Login(SQLModel):
    username: str
    password: str
