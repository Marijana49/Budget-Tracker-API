from fastapi import APIRouter, Depends, status
from budget_tracker_api.database import get_session
from budget_tracker_api.schemas import MonthSummary
from budget_tracker_api.services.summaries import get_month_summary
from sqlalchemy.orm import Session
import datetime

router = APIRouter(prefix="/summaries", tags=["Summaries"])

@router.get("", response_model=MonthSummary, status_code=status.HTTP_200_OK)
def router_month_summary(month: datetime.date, session: Session = Depends(get_session)):
    return get_month_summary(session, month)