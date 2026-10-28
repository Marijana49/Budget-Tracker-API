from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from budget_tracker_api.exceptions import (
    CategoryNameTaken,
    CategoryNotFound,
    CategoryHasTransactions,
    TransactionNotFound,
    InvalidCsvFile,
    BudgetAlreadyExists,
    BudgetNotFound
)

def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(CategoryNameTaken)
    async def category_name_taken_handler(
        request: Request,
        exc: CategoryNameTaken,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={
                "detail": "Category with this name already exists"
            },
        )

    @app.exception_handler(CategoryNotFound)
    async def category_not_found_handler(
        request: Request,
        exc: CategoryNotFound,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"detail": "Category not found"},
        )

    @app.exception_handler(CategoryHasTransactions)
    async def category_has_transactions_handler(
        request: Request,
        exc: CategoryHasTransactions,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={
                "detail": "Cannot delete a category that has transactions"
            },
        )

    @app.exception_handler(TransactionNotFound)
    async def transaction_not_found_handler(
        request: Request,
        exc: TransactionNotFound,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"detail": "Transaction not found"},
        )

    @app.exception_handler(InvalidCsvFile)
    async def invalid_csv_file_handler(request: Request, exc: InvalidCsvFile) -> JSONResponse:
        return JSONResponse(
            status_code=422, content={"detail": str(exc) or "Invalid CSV file"}
            )

    @app.exception_handler(BudgetAlreadyExists)
    async def budget_already_exists_handler(
        request: Request,
        exc: BudgetAlreadyExists,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409, 
            content={"detail": "Budget already exists for this category and month"},
        )

    
    @app.exception_handler(BudgetNotFound)
    async def budget_not_found_handler(
        request: Request,
        exc: BudgetNotFound,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={"detail": "Budget not found"},
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"detail": "The request conflicts with existing data"},
        )