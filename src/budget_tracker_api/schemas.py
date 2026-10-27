from pydantic import BaseModel, StringConstraints, Field, ConfigDict
from typing import Annotated, Optional
from datetime import date
from decimal import Decimal
from budget_tracker_api.enums import TransactionType

Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=30)]
HexColor = Annotated[str, StringConstraints(pattern=r"^#[0-9A-Fa-f]{6}$")]
Amount = Annotated[Decimal, Field(gt=0, le=Decimal("1000000.00"), max_digits=9, decimal_places=2)]
Description = Annotated[str, StringConstraints(max_length=200)]

# Category
class CategoryCreate(BaseModel):
    name: Name
    color: HexColor

class CategoryUpdate(BaseModel):
    name: Name | None = None
    color: HexColor | None = None

class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: Name
    color: HexColor

# Transaction
class TransactionCreate(BaseModel):
    type: TransactionType
    amount: Amount
    date: date
    description: Description | None = None
    category_id: int

class TransactionUpdate(BaseModel):
    type: TransactionType | None = None
    amount: Amount | None = None
    date: Optional[date] = None
    description: Description | None = None

class TransactionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: TransactionType
    amount: Amount
    date: date
    description: Description | None = None

class TransactionPage(BaseModel):
    items: list[TransactionRead]
    total: int
    page: int
    page_size: int
    
# Budget
class BudgetCreate(BaseModel):
    month: date
    amount: Amount
    category_id: int 

class BudgetUpdate(BaseModel):
    month: date | None = None
    amount: Amount | None = None
    category_id: int | None = None

class BudgetRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    month: date
    amount: Amount
    category_id: int 