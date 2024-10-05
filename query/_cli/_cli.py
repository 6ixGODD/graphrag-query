# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import argparse
import sys

import pydantic

from .. import errors as _errors


class _Args(pydantic.BaseModel):
    pass


def _parse_args() -> _Args:
    parser = argparse.ArgumentParser()
    # TODO: Add arguments
    return _Args.parse_obj(parser.parse_args())


def main() -> int:
    try:
        _main()
    except _errors.GraphRAGError as err:
        print(err)  # TODO: Implement parsing of GraphRAGError
        return 1
    except pydantic.ValidationError as err:
        print(err)  # TODO: Implement parsing of pydantic.ValidationError
        return 1
    except KeyboardInterrupt:
        sys.stderr.write("\n")
        return 1
    return 0


def _main() -> None:
    args = _parse_args()
    pass
