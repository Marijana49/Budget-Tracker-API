from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from budget_tracker_api.schemas import TransactionCreate, TransactionUpdate, TransactionRead
from budget_tracker_api.database import get_session
from budget_tracker_api.services.transactions import create_transaction, get_transaction_by_id, delete_transaction, update_transaction

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
def router_transaction_create(data: TransactionCreate, session: Session = Depends(get_session)):
    return create_transaction(session, data)


@router.get("/{transaction_id}", response_model=TransactionRead, status_code=status.HTTP_200_OK)
def router_get_transaction_by_id(transaction_id: int, session: Session = Depends(get_session)):
    return get_transaction_by_id(session, transaction_id)


@router.delete("/{transaction_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def router_delete_transaction(transaction_id: int, session: Session = Depends(get_session)):
    return delete_transaction(session, transaction_id)


@router.patch("/{transaction_id}", response_model=TransactionRead)
def router_update_transaction(transaction_id: int, data: TransactionUpdate, session: Session = Depends(get_session)):
    return update_transaction(session, data, transaction_id)