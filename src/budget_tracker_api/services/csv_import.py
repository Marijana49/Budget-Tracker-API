import csv
import io
from typing import BinaryIO
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.orm import Session
from budget_tracker_api.exceptions import InvalidCsvFile
from budget_tracker_api.models import Category, Transaction
from budget_tracker_api.schemas import TransactionCreate

BATCH_SIZE = 1000
REQUIRED_COLUMNS = {"type", "amount", "date", "description", "category"}


def _clean(value: str | None) -> str:
    return (value or "").strip()


def import_transactions(session: Session, file: BinaryIO) -> dict:
    categories = {
        name.lower(): category_id
        for category_id, name in session.execute(select(Category.id, Category.name))
    }

    try:
        text = io.TextIOWrapper(file, encoding="utf-8-sig", newline="")
        reader = csv.DictReader(text)
        columns = {(c or "").strip().lower() for c in (reader.fieldnames or [])}
    except (UnicodeDecodeError, csv.Error):
        raise InvalidCsvFile("File is not a valid UTF-8 CSV")

    missing = REQUIRED_COLUMNS - columns
    if missing:
        raise InvalidCsvFile(f"Missing columns: {', '.join(sorted(missing))}")

    imported = 0
    failed: list[dict] = []
    batch: list[Transaction] = []

    try:
        for raw_row in reader:
            row_number = reader.line_num  
            row = {(k or "").strip().lower(): v for k, v in raw_row.items()}

            category_id = categories.get(_clean(row.get("category")).lower())
            if category_id is None:
                failed.append({"row": row_number, "reason": "category: category does not exist"})
                continue

            try:
                data = TransactionCreate(
                    type=_clean(row.get("type")).lower(),
                    amount=_clean(row.get("amount")),
                    date=_clean(row.get("date")),
                    description=_clean(row.get("description")) or None,
                    category_id=category_id,
                )
            except ValidationError as e:
                err = e.errors()[0]
                field = ".".join(str(p) for p in err["loc"])
                failed.append({"row": row_number, "reason": f"{field}: {err['msg']}"})
                continue

            batch.append(Transaction(**data.model_dump()))

            if len(batch) >= BATCH_SIZE:
                session.add_all(batch)
                session.commit()
                imported += len(batch)
                batch = []
    except (UnicodeDecodeError, csv.Error):
        session.rollback()
        raise InvalidCsvFile("File could not be read as a UTF-8 CSV")

    if batch:
        session.add_all(batch)
        session.commit()
        imported += len(batch)

    return {"imported": imported, "failed": failed}