from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from models.borrower_models import CustomerBase


class Lender(CustomerBase, table=True):
    id: Optional[int] = Field(default = None, primary_key = True)
    

    