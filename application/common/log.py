import sys

from loguru import logger as _logger


def init_logger(
    level: str = 'INFO',
    *,
    out_file: str | None = None,
    err_file: str | None = None,
    rotation: str | None = None,
    retention: str | None = None,
    serialize: bool = True
) -> None:
    _logger.remove()  # remove the default logger
    _logger.add(
        sys.stdout,
        level=level,
        catch=False,
        colorize=True,
        diagnose=False,
        backtrace=False,
        serialize=False
    )
    if out_file:
        _logger.add(
            out_file,
            level=level,
            catch=False,
            colorize=False,
            diagnose=False,
            backtrace=False,
            rotation=rotation,
            retention=retention,
            serialize=serialize
        )
    _logger.add(
        sys.stderr,
        level="ERROR",
        catch=False,
        colorize=True,
        diagnose=False,
        backtrace=False,
        serialize=False
    )
    if err_file:
        _logger.add(
            err_file,
            level='ERROR',
            catch=False,
            colorize=False,
            diagnose=False,
            backtrace=False,
            rotation=rotation,
            retention=retention,
            serialize=serialize
        )


def get_logger(**kwargs):
    return _logger.bind(**kwargs)
