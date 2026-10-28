# Budget-Tracker-API
Backend task. A REST API for tracking personal finances. Users can manage income and expenses, organize transactions into categories, set monthly budgets, import transactions from CSV files, and review monthly financial summaries.

**Stack**

- Python 3.14

- FastAPI

- SQLAlchemy 2.0

- SQLite

- pytest

- uv


**Requirements**
 - Python 3.14

 - [uv](https://docs.astral.sh/uv/)


Install uv (one of):

**Windows (PowerShell)**

    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

**Linux/macOS**

      curl -LsSf https://astral.sh/uv/install.sh | sh


**With pip**

       pip install uv

To check that it works:

    uv --version

# Setup

1. Clone the repository:

        git clone https://github.com/Marijana49/Budget-Tracker-API.git
        cd Budget-Tracker-API

2. Install dependencies
 
         uv sync

3. Create a `.env` file (copy `.env.example`):

       DATABASE_URL=sqlite:///./task.db

4. Start the server:
   
       uv run .\app.py  (on Windows)

       uv run app.py  (on Linux/macOS)

5. Open the interactive docs at http://127.0.0.1:8000/docs

   Tables are created automatically on startup. Data is stored in `task.db`
and persists across restarts.

# Sample data

To fill an empty database with sample categories, transactions and budgets (October 2026), run:

    uv run python seed.py

The command does nothing if the database already has data.
To start over, stop the server, delete `task.db` and run the command again.


# Tests

To run the test use:

    uv run pytest

Tests use an in-memory database, so they never touch `task.db`.
They cover the monthly summary, validation rules, CSV import,
categories, transactions and budgets.


## API documentation

- Interactive: `/docs` (Swagger UI) and `/redoc`
- Specification file: [`openapi.json`](openapi.json)


## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/categories` | Create a category |
| GET | `/categories` | List categories sorted by name |
| PATCH | `/categories/{category_id}` | Change name and/or color |
| DELETE | `/categories/{category_id}` | Delete (409 if it has transactions; budgets are deleted with it) |
| POST | `/transactions` | Add a transaction |
| GET | `/transactions` | List with pagination and filters |
| GET | `/transactions/{transaction_id}` | Get one transaction |
| PATCH | `/transactions/{transaction_id}` | Change a transaction |
| DELETE | `/transactions/{transaction_id}` | Delete a transaction |
| POST | `/transactions/import` | Import transactions from a CSV file |
| POST | `/budgets` | Set a budget for a category and month |
| GET | `/budgets?month=YYYY-MM-DD` | List budgets of a month |
| PATCH | `/budgets/{category_id}/{month}` | Change the budget amount |
| DELETE | `/budgets/{category_id}/{month}` | Remove a budget |
| GET | `/summaries?month=YYYY-MM-DD` | Monthly summary |


## CSV import

Upload a UTF-8 file to `POST /transactions/import` (multipart field `file`).

- The category is matched by name, ignoring case, and must already exist.

- Valid rows are imported, invalid ones are skipped and reported.

- Rows are processed one by one and saved in batches of 1000,
  so large files do not need much memory.

- Importing the same file twice creates the transactions twice.
 
- An example file is in `samples.csv`.

- Expected header and example rows:

```
type,amount,date,description,category
expense,12.50,2026-10-08,Lunch,Hrana i piće
income,300.00,2026-10-09,,Plata
```

- Response: `{"imported": N, "failed": [{"row": R, "reason": "..."}]}`.
`row` is the line number in the file (the header is line 1).
An empty description means the transaction has no description.
A file with missing columns or the wrong encoding is rejected with 422.

## Transactions list

`GET /transactions` query parameters (all optional): `page` (default 1), `page_size` (default 20, max 100), `date_from`, `date_to` (both inclusive), `category_id`, `type` (`income` or `expense`), `text` (case-insensitive match in the description). Filters can be combined.

Sorted newest first; for the same date, the last added comes first.

Response: `items`, `total` (number of transactions matching the filters), `page`, `page_size`.


## Notes

- A budget month is stored as the first day of the month

- Errors: 422 invalid input, 404 not found, 409 broken rule (duplicate name,
  category with transactions, duplicate budget)

- There are no migrations: after changing a model, delete `task.db`
  and restart the server



   
