# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import sys
import typing

import loguru

_logger = loguru.logger


def init_logger(
    level: str = 'INFO',
    *,
    out_file: typing.Optional[str] = None,
    err_file: typing.Optional[str] = None,
    rotation: typing.Optional[str] = None,
    retention: typing.Optional[str] = None,
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
