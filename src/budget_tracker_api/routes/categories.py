from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from budget_tracker_api.schemas import CategoryCreate, CategoryUpdate, CategoryRead
from budget_tracker_api.database import get_session
from budget_tracker_api.services.categories import create_category, update_category, delete_category, get_categories

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def route_create_category(data: CategoryCreate, session: Session = Depends(get_session)):
    return create_category(session=session, data=data)


@router.get("", response_model=list[CategoryRead], status_code=status.HTTP_200_OK)
def router_get_categories(session: Session = Depends(get_session)):
    return get_categories(session)


@router.delete("/{category_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def router_delete_category(category_id: int, session: Session = Depends(get_session)):
    return delete_category(session, category_id)


@router.patch("/{category_id}", response_model=CategoryRead, status_code=status.HTTP_200_OK)
def router_update_category(data: CategoryUpdate, category_id: int, session = Depends(get_session)):
    return update_category(session, data, category_id)