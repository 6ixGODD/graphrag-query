# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import http
import typing

from starlette import types

from server import dto
from server.common import const


class AuthMiddleware:
    def __init__(
        self,
        app: types.ASGIApp,
        *,
        api_keys: typing.List[str],
    ):
        self.app = app
        self.api_keys = api_keys

    async def __call__(self, scope: types.Scope, receive: types.Receive, send: types.Send) -> None:
        if scope[const.Constants.TYPE_SCOPE_KEY] != "http":
            await self.app(scope, receive, send)
            return
        headers = scope.get(const.Constants.HEADERS_SCOPE_KEY, [])
        api_key = next(
            (value.decode() for key, value in headers if
             key.decode().lower() == const.Constants.AUTHORIZATION_HEADER.lower()), None
        )
        api_key = api_key.split(" ")[-1] if api_key else None
        if not api_key or api_key not in self.api_keys:
            await send(
                {
                    const.Constants.TYPE_MESSAGE_KEY:    "http.response.start",
                    const.Constants.STATUS_MESSAGE_KEY:  http.HTTPStatus.UNAUTHORIZED,
                    const.Constants.HEADERS_MESSAGE_KEY: [(b"content-type", b"application/json"), ]
                }
            )
            await send(
                {
                    const.Constants.TYPE_MESSAGE_KEY: "http.response.body",
                    const.Constants.BODY_MESSAGE_KEY: dto.ErrorResponse(
                        message=http.HTTPStatus.UNAUTHORIZED.phrase,
                    ).json().encode()
                }
            )
            return

        await self.app(scope, receive, send)
