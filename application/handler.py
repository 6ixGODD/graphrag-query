# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

from http import HTTPStatus

import fastapi
from starlette.exceptions import HTTPException

from . import dto
from .common import const, ctx, errors


def init_handler(app: fastapi.FastAPI):
    r"""Register exception handlers for the FastAPI application."""

    @app.exception_handler(errors.BaseAppError)
    async def handle_base_error(_, exc: errors.BaseAppError):
        return fastapi.responses.JSONResponse(
            status_code=exc.status_code,
            content=dto.ErrorResponse(
                message=exc.message,
                code=exc.status_code
            ).dict()
        )

    @app.exception_handler(fastapi.exceptions.RequestValidationError)
    async def handle_request_validation_error(_, exc: fastapi.exceptions.RequestValidationError):
        return fastapi.responses.JSONResponse(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            content=dto.ErrorResponse(
                message=f"Validation Error: {exc.__str__()}.",
                code=fastapi.status.HTTP_400_BAD_REQUEST
            ).dict()
        )

    @app.exception_handler(HTTPException)
    async def handle_http_exception(_, exc: HTTPException):
        return fastapi.responses.JSONResponse(
            status_code=exc.status_code,
            content=dto.ErrorResponse(
                message=exc.detail, code=exc.status_code
            ).dict()
        )

    @app.exception_handler(Exception)
    async def handle_exception(_, __):
        return fastapi.responses.JSONResponse(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=dto.ErrorResponse(
                message=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
                code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
            ).dict(),
            headers={
                const.Constants.REQUEST_ID_HEADER: ctx.get_request_id()
            }
        )
