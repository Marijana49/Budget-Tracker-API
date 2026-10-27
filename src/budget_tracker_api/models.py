from sqlalchemy import Integer, String, Numeric, Date, UniqueConstraint, ForeignKey, Enum as SQLAlchemyEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from decimal import Decimal
import datetime
from budget_tracker_api.enums import TransactionType

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
    color: Mapped[str] = mapped_column(String(7), nullable=False)

    budgets: Mapped[list["Budget"]] = relationship(cascade = "all, delete-orphan")


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[TransactionType] = mapped_column(SQLAlchemyEnum(TransactionType, name ="transactionType"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    description: Mapped[str | None] = mapped_column(String(200), nullable=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)


class Budget(Base):
    __tablename__ = "budgets"
    __table_args__ = (UniqueConstraint("category_id", "month"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    month: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)