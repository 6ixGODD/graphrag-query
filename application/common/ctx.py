from contextvars import ContextVar

from application.common import const, log

_request_id_ctx_var: ContextVar[str] = ContextVar(const.Constants.REQUEST_ID_CTX_KEY, default='')
_ip_ctx_var: ContextVar[str] = ContextVar(const.Constants.IP_CTX_KEY, default='')


# Setter
def set_request_id(request_id: str) -> None:
    _request_id_ctx_var.set(request_id)


def set_ip(ip: str) -> None:
    _ip_ctx_var.set(ip)


def clear_request_id() -> None:
    _request_id_ctx_var.set('')


def clear_ip() -> None:
    _ip_ctx_var.set('')


# Getter
def get_request_id() -> str:
    return _request_id_ctx_var.get()


def get_ip() -> str:
    return _ip_ctx_var.get()


def get_logger_with_context(tag: str, **kwargs):
    return log.get_logger(tag=tag, request_id=get_request_id(), ip=get_ip(), **kwargs)
