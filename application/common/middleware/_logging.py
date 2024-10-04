from http import HTTPStatus

from starlette.types import ASGIApp, Receive, Scope, Send

from application.common import const, ctx, errors


class LoggingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope[const.Constants.TYPE_SCOPE_KEY] != "http":  # pragma: no cover
            # Skip non-HTTP requests
            await self.app(scope, receive, send)
        logger = ctx.get_logger_with_context(tag=const.Constants.MIDDLEWARE_LOGGING_TAG)
        logger.bind(scope=scope).info(
            f"Request: {scope[const.Constants.CLIENT_SCOPE_KEY][0]}:{scope[const.Constants.CLIENT_SCOPE_KEY][1]} -> "
            f"{scope[const.Constants.SERVER_SCOPE_KEY][0]}:{scope[const.Constants.SERVER_SCOPE_KEY][1]} | "
            f"[ {scope[const.Constants.METHOD_SCOPE_KEY]} {scope[const.Constants.PATH_SCOPE_KEY]} ]"
        )

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                logger.bind(
                    status_code=message[const.Constants.STATUS_MESSAGE_KEY],
                    headers=message[const.Constants.HEADERS_MESSAGE_KEY]
                ).info(
                    f"Response: {message[const.Constants.STATUS_MESSAGE_KEY]} "
                    f"{HTTPStatus(message[const.Constants.STATUS_MESSAGE_KEY]).phrase}"
                )
            await send(message)

        with logger.catch(message="Failed to process request.", reraise=True, exclude=errors.BaseAppError):
            await self.app(scope, receive, send_wrapper)
