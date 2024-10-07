# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import http
import typing


class BaseAppError(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r}, status_code={self.status_code!r})"

    @property
    def dict(self) -> typing.Dict[str, typing.Union[str, int]]:
        return {
            'message':     self.message,
            'status_code': self.status_code,
        }


class BadRequestError(BaseAppError):
    def __init__(self, message: str = http.HTTPStatus.BAD_REQUEST.phrase):
        super().__init__(message, http.HTTPStatus.BAD_REQUEST.value)


class UnauthorizedError(BaseAppError):
    def __init__(self, message: str = http.HTTPStatus.UNAUTHORIZED.phrase):
        super().__init__(message, http.HTTPStatus.UNAUTHORIZED.value)


class ForbiddenError(BaseAppError):
    def __init__(self, message: str = http.HTTPStatus.FORBIDDEN.phrase):
        super().__init__(message, http.HTTPStatus.FORBIDDEN.value)


class NotFoundError(BaseAppError):
    def __init__(self, message: str = http.HTTPStatus.NOT_FOUND.phrase):
        super().__init__(message, http.HTTPStatus.NOT_FOUND.value)


class ConflictError(BaseAppError):
    def __init__(self, message: str = http.HTTPStatus.CONFLICT.phrase):
        super().__init__(message, http.HTTPStatus.CONFLICT.value)


class TooManyRequestsError(BaseAppError):
    def __init__(self, message: str = http.HTTPStatus.TOO_MANY_REQUESTS.phrase, *, retry_after: int = 10):
        super().__init__(message, http.HTTPStatus.TOO_MANY_REQUESTS.value)
        self.retry_after = retry_after


class InternalServerError(BaseAppError):
    def __init__(self, message: str = http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase):
        super().__init__(message, http.HTTPStatus.INTERNAL_SERVER_ERROR.value)
