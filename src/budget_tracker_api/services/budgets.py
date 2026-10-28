from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import date
from budget_tracker_api.models import Budget, Category
from budget_tracker_api.schemas import BudgetCreate, BudgetUpdate
from budget_tracker_api.exceptions import CategoryNotFound, BudgetAlreadyExists, BudgetNotFound

def _month_start(value: date) -> date:
    return date(value.year, value.month, 1)


def _find_budget(session: Session, category_id: int, month: date) -> Budget:
    budget = session.scalars(
        select(Budget).where(
            Budget.category_id == category_id,
            Budget.month == _month_start(month),
        )
    ).first()
    
    if budget is None:
        raise BudgetNotFound()
    return budget


def set_budget(session: Session, data: BudgetCreate) -> Budget:
    target_month = _month_start(data.month)

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


def update_budget(session: Session, category_id: int, month: date, data: BudgetUpdate) -> Budget:
    budget = _find_budget(session, category_id, month)
    
    budget.amount = data.amount

    session.commit()
    session.refresh(budget)
    return budget


def remove_budget(session: Session, category_id: int, month: date) -> None:
    budget = _find_budget(session, category_id, month)

    session.delete(budget)
    session.commit()


def get_budgets(session: Session, month: date) -> list[Budget]:
    target_month = _month_start(month)
    budgets = (select(Budget).join(Category).where(Budget.month == target_month).order_by(func.lower(Category.name)))

    return list(session.scalars(budgets).all())