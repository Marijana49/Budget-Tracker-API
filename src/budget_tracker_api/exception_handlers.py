from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from budget_tracker_api.exceptions import (
    CategoryNameTaken,
    CategoryNotFound,
    CategoryHasTransactions,
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