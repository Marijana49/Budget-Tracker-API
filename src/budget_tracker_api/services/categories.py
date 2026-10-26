from sqlalchemy import func, select
from sqlalchemy.orm import Session
from budget_tracker_api.models import Category, Transaction
from budget_tracker_api.schemas import CategoryCreate, CategoryUpdate
from budget_tracker_api.exceptions import CategoryNameTaken, CategoryNotFound, CategoryHasTransactions


def create_category(session: Session, data: CategoryCreate) -> Category:
    category_exists = session.scalar(select(Category.id).where(func.lower(Category.name) == data.name.lower()))

    if category_exists is not None:
        raise CategoryNameTaken()

    category = Category(name=data.name, color=data.color)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def delete_category(session: Session, category_id: int) -> None:
    category_exists = session.get(Category, category_id)

    if category_exists is None:
        raise CategoryNotFound()

    has_transactions = session.scalar(select(Transaction.id).where(Transaction.category_id == category_id).limit(1))

    if has_transactions is not None:
        raise CategoryHasTransactions()

    session.delete(category_exists)
    session.commit()


def update_category(session: Session, data: CategoryUpdate, category_id: int) -> Category:
    category = session.get(Category, category_id)

    if category is None:
        raise CategoryNotFound()

    if data.name is not None and data.name.lower() != category.name.lower():
        name_taken = session.scalar(
            select(Category.id).where(
                func.lower(Category.name) == data.name.lower(), 
                Category.id != category_id
            )
        )
        
        if name_taken is not None:
            raise CategoryNameTaken()
        
        category.name = data.name

    if data.color is not None:
        category.color = data.color 

    session.commit()
    session.refresh(category)
    return category


def get_categories(session: Session) -> list[Category]:
    categories = select(Category).order_by(func.lower(Category.name))

    return list(session.scalars(categories).all())