from sqlalchemy import func, select
from sqlalchemy.orm import Session
from budget_tracker_api.models import Transaction, Category
from budget_tracker_api.schemas import TransactionCreate, TransactionUpdate
from budget_tracker_api.enums import TransactionType
from budget_tracker_api.exceptions import CategoryNotFound, TransactionNotFound
import datetime

def create_transaction(session: Session, data: TransactionCreate) -> Transaction:
    category = session.get(Category, data.category_id)
    if category is None:
        raise CategoryNotFound()

    transaction = Transaction(
        type = data.type,
        amount = data.amount,
        date = data.date,
        description = data.description,
        category_id = data.category_id
    )

    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


def get_transaction_by_id(session: Session, transaction_id: int) -> Transaction:
    transaction = session.get(Transaction, transaction_id)
    if transaction is None:
        raise TransactionNotFound()

    return transaction


def delete_transaction(session: Session, transaction_id: int) -> None:
    transaction = session.get(Transaction, transaction_id)
    if transaction is None:
        raise TransactionNotFound()

    session.delete(transaction)
    session.commit()


def update_transaction(session: Session, data: TransactionUpdate, transaction_id: int) -> Transaction:
    transaction = session.get(Transaction, transaction_id)
    if transaction is None:
        raise TransactionNotFound()

    changes = data.model_dump(exclude_unset=True)

    if "category_id" in changes:
        if session.get(Category, changes["category_id"]) is None:
            raise CategoryNotFound()

    for required in ("type", "amount", "date", "category_id"):
        if required in changes and changes[required] is None:
            changes.pop(required)

    for field, value in changes.items():
        setattr(transaction, field, value)

    session.commit()
    session.refresh(transaction)
    return transaction


def list_transactions(
    session: Session, 
    page: int, 
    page_size: int, 
    date_from: datetime.time | None = None,
    date_to: datetime.time | None = None,
    category_id: int | None = None,
    type: TransactionType | None = None,
    text: str | None = None,
) -> dict:
    conditions = []

    if date_from is not None:
        conditions.append(Transaction.date >= date_from)
    if date_to is not None:
        conditions.append(Transaction.date <= date_to)
    if category_id is not None:
        conditions.append(Transaction.category_id == category_id)
    if type is not None:
        conditions.append(Transaction.type == type)
    if text:
        conditions.append(func.lower(Transaction.description).like(f"%{text.lower()}"))

    stmt = select(Transaction).where(*conditions)

    total = session.scalar(select(func.count()).select_from(Transaction).where(*conditions))

    items = session.scalars(
        stmt.order_by(Transaction.date.desc(), Transaction.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    ).all()

    return {"items": items, "total": total, "page": page, "page_size": page_size}