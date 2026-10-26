from sqlalchemy import func, select
from sqlalchemy.orm import Session
from budget_tracker_api.models import Transaction, Category
from budget_tracker_api.schemas import TransactionCreate, TransactionUpdate
from budget_tracker_api.enums import TransactionType
from budget_tracker_api.exceptions import CategoryNotFound, TransactionNotFound


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