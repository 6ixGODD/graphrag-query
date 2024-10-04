from starlette.types import ASGIApp, Receive, Scope, Send

from application.common import const, ctx, utils


class RequestIDMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope[const.Constants.TYPE_SCOPE_KEY] != "http":  # pragma: no cover
            # Skip non-HTTP requests
            await self.app(scope, receive, send)
            return
        headers = scope.get(const.Constants.HEADERS_SCOPE_KEY, [])
        request_id = next(
            (value.decode() for key, value in headers if
             key.decode().lower() == const.Constants.REQUEST_ID_HEADER.lower()), None
        )
        if request_id:
            ctx.set_request_id(request_id)
        else:
            ctx.clear_request_id()
            request_id = utils.gen_id(prefix=const.Constants.REQUEST_ID_PREFIX, __split='_')
            ctx.set_request_id(request_id)

        async def send_wrapper(message):
            # Add request ID to the response headers
            if message[const.Constants.TYPE_MESSAGE_KEY] == "http.response.start":
                message[const.Constants.HEADERS_MESSAGE_KEY].append(
                    (const.Constants.REQUEST_ID_HEADER.encode(), request_id.encode())
                )
            await send(message)

        await self.app(scope, receive, send_wrapper)
