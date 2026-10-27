from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date
from budget_tracker_api.models import Budget, Category
from budget_tracker_api.schemas import BudgetCreate, BudgetUpdate
from budget_tracker_api.exceptions import CategoryNotFound, BudgetAlreadyExists, BudgetNotFound

def set_budget(session: Session, data: BudgetCreate) -> Budget:
    target_month = date(data.month.year, data.month.month, 1)

    category = session.get(Category, data.category_id)
    if category is None:
        raise CategoryNotFound()

    existing_budget = session.scalars(
        select(Budget).where(Budget.category_id == data.category_id, Budget.month == target_month)
    ).first()

    if existing_budget:
        raise BudgetAlreadyExists()

    budget = Budget(
        month = target_month,
        amount = data.amount,
        category_id = data.category_id
    )

    session.add(budget)
    session.commit()
    session.refresh(budget)
    return budget


def update_budget(session: Session, budget_id: int, data: BudgetUpdate) -> Budget:
    budget = session.get(Budget, budget_id)
    if budget is None:
        raise BudgetNotFound()

    new_category_id = (
        data.category_id
        if data.category_id is not None
        else budget.category_id
    )

    new_month = (
        date(data.month.year, data.month.month, 1)
        if data.month is not None
        else budget.month
    )

    if data.category_id is not None and session.get(Category, new_category_id) is None:
        raise CategoryNotFound()

    duplicate = session.scalars(
        select(Budget).where(
            Budget.category_id == new_category_id,
            Budget.month == new_month,
            Budget.id != budget_id,
        )
    ).first()

    if duplicate:
        raise BudgetAlreadyExists()

    budget.category_id = new_category_id
    budget.month = new_month

    if data.amount is not None:
        budget.amount = data.amount

    session.commit()
    session.refresh(budget)
    return budget



def remove_budget(session: Session, category_id: int, month: date) -> None:
    target_month = date(month.year, month.month, 1)

    budget = session.scalars(
        select(Budget).where(
            Budget.category_id == category_id,
            Budget.month == target_month,
        )
    ).first()

    if budget is None:
        raise BudgetNotFound()

    session.delete(budget)
    session.commit()