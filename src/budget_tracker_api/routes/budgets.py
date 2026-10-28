from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from budget_tracker_api.schemas import BudgetCreate, BudgetRead, BudgetUpdate
from budget_tracker_api.database import get_session
from budget_tracker_api.services.budgets import set_budget, update_budget, remove_budget, get_budgets
from datetime import date

router = APIRouter(prefix="/budgets", tags=["Budgets"])

@router.post("", response_model=BudgetRead, status_code=status.HTTP_201_CREATED)
def router_set_budget(data: BudgetCreate, session: Session = Depends(get_session)):
    return set_budget(session, data)


@router.patch("/{category_id}/{month}", response_model=BudgetRead, status_code=status.HTTP_200_OK)
def router_update_budget(data: BudgetUpdate, category_id: int, month: date, session: Session = Depends(get_session)):
    return update_budget(session, category_id, month, data)


@router.delete("/{category_id}/{month}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def router_remove_budget(category_id: int, month: date, session: Session = Depends(get_session)):
    remove_budget(session, category_id, month)


@router.get("", response_model=list[BudgetRead], status_code=status.HTTP_200_OK)
def router_get_budgets(month: date, session: Session = Depends(get_session)):
    return get_budgets(session, month)
