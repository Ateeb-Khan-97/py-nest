from typing import Dict
from fastapi import FastAPI
from http import HTTPStatus
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from src.core.exceptions.http_exceptions import HTTPException


def handle_http_exception(_, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        content={
            "success": False,
            "status": exc.status,
            "message": exc.message,
            "data": None,
        },
    )


def unhandled_exception(_, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
            "message": "Internal Server Error",
            "data": None,
        },
    )


def handle_validation_exception(_, exc: ValidationError) -> JSONResponse:
    errors = exc.errors()
    error_messages: Dict[str, str] = {}
    for error in errors:
        error_msg = error["msg"]
        if error_msg.startswith("Value error, "):
            error_msg = error_msg.replace("Value error, ", "", 1)
        key = error["loc"][1]
        error_messages[key] = error_msg.lower()

    return JSONResponse(
        status_code=HTTPStatus.BAD_REQUEST,
        content={
            "success": False,
            "status": HTTPStatus.BAD_REQUEST,
            "message": "Validation Error",
            "data": error_messages,
        },
    )


def handle_starlette_http_exception(_, exc: StarletteHTTPException) -> JSONResponse:
    """Handle Starlette HTTPException (including 404 Not Found errors for non-existent endpoints)."""
    # Check if it's a 404 error
    if exc.status_code == HTTPStatus.NOT_FOUND:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={
                "success": False,
                "status": HTTPStatus.NOT_FOUND,
                "message": "Endpoint not found",
                "data": None,
            },
        )
    # For other Starlette HTTPExceptions, return a generic response
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status": exc.status_code,
            "message": exc.detail or "An error occurred",
            "data": None,
        },
    )


def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(HTTPException, handle_http_exception)
    app.add_exception_handler(RequestValidationError, handle_validation_exception)
    app.add_exception_handler(StarletteHTTPException, handle_starlette_http_exception)
    app.add_exception_handler(Exception, unhandled_exception)
