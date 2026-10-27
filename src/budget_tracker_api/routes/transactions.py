from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from budget_tracker_api.schemas import TransactionCreate, TransactionUpdate, TransactionRead, TransactionPage
from budget_tracker_api.database import get_session
from budget_tracker_api.services.transactions import create_transaction, get_transaction_by_id, delete_transaction, update_transaction, list_transactions
from budget_tracker_api.enums import TransactionType
import datetime

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def router_transaction_create(data: TransactionCreate, session: Session = Depends(get_session)):
    return create_transaction(session, data)


@router.get("/{transaction_id}", response_model=TransactionRead, status_code=status.HTTP_200_OK)
def router_get_transaction_by_id(transaction_id: int, session: Session = Depends(get_session)):
    return get_transaction_by_id(session, transaction_id)


@router.delete("/{transaction_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def router_delete_transaction(transaction_id: int, session: Session = Depends(get_session)):
    delete_transaction(session, transaction_id)


@router.patch("/{transaction_id}", response_model=TransactionRead)
def router_update_transaction(transaction_id: int, data: TransactionUpdate, session: Session = Depends(get_session)):
    return update_transaction(session, data, transaction_id)


@router.get("", response_model=TransactionPage)
def router_list_transactions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    date_from: datetime.date | None = None,
    date_to: datetime.date | None = None,
    category_id: int | None = None,
    type: TransactionType | None = None,
    text: str | None = None,
    session: Session = Depends(get_session),
):
    return list_transactions(session, page, page_size, date_from, date_to, category_id, type, text)