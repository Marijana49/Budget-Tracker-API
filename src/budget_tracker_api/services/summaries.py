import datetime
from decimal import Decimal
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from budget_tracker_api.models import Transaction, Category, Budget
from budget_tracker_api.enums import TransactionType
from budget_tracker_api.schemas import CategorySummary


def month_range(month: datetime.date) -> tuple[datetime.date, datetime.date]:
    start = datetime.date(month.year, month.month, 1)
    if month.month == 12:
        end = datetime.date(month.year + 1, 1, 1)
    else:
        end = datetime.date(month.year, month.month + 1, 1)

    return start, end


def get_month_summary(session: Session, month: datetime.date) -> dict:
    start, end = month_range(month)

    rows = session.execute(
        select(Transaction.type, func.sum(Transaction.amount))
        .where(Transaction.date >= start, Transaction.date < end)
        .group_by(Transaction.type)
    ).all()

    totals = {row_type: total for row_type, total in rows}
    income = totals.get(TransactionType.INCOME, Decimal("0"))
    expense = totals.get(TransactionType.EXPENSE, Decimal("0"))

    return {
        "month": start,
        "total_income": income,
        "total_expense": expense,
        "balance": income - expense,
        "categories": get_category_summaries(session, month),
    }


def get_category_summaries(session: Session, month: datetime.date) -> list[CategorySummary]:
    start, end = month_range(month)

    spent = session.execute(
        select(Transaction.category_id, func.sum(Transaction.amount))
        .where(
            Transaction.type == TransactionType.EXPENSE,
            Transaction.date >= start,
            Transaction.date < end
        ).group_by(Transaction.category_id)
    ).all()

    spent_by_category = {category_id: total for category_id, total in spent}

    budget = session.execute(
        select(Budget.category_id, Budget.amount).where(Budget.month == start)
    ).all()

    budget_by_category = {category_id: amount for category_id, amount in budget}

    category_ids = set(spent_by_category) | set(budget_by_category)
    if not category_ids:
        return []

    names = {
        category_id: name
        for category_id, name in session.execute(
            select(Category.id, Category.name).where(Category.id.in_(category_ids))
        )
    }

    result = []
    for category_id in category_ids:
        spent = spent_by_category.get(category_id, Decimal("0"))
        budget = budget_by_category.get(category_id)
        result.append(
            {
                "category": names[category_id],
                "spent": spent,
                "budget": budget,
                "left": budget - spent if budget is not None else None,
            }
        )

    result.sort(key=lambda item: (-item["spent"], item["category"].lower()))
    return result