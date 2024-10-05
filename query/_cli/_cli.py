# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License.
#
# Copyright (c) 2024 6ixGODD.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import argparse
import sys
import typing

import pydantic

from . import _utils
from .. import __version__, errors as _errors


class _Args(pydantic.BaseModel):
    config: typing.Annotated[str, pydantic.Field(..., pattern=r".*\.(json|yaml|toml)")]
    verbose: bool
    engine: typing.Annotated[str, pydantic.Field(..., pattern=r"local|global")]
    stream: bool
    api_key: typing.Optional[str]
    base_url: typing.Annotated[
        typing.Optional[str],
        pydantic.Field(..., pattern=r"https?://([a-zA-Z0-9\-.]+\.[a-zA-Z]{2,})(:[0-9]{1,5})?(/\s*)?")
    ]
    text: str


def _parse_args() -> _Args:
    parser = argparse.ArgumentParser(
        description="GraphRAG Query CLI",
        prog="python -m query",
        add_help=True,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Path to the configuration file. Can be in JSON, YAML, or TOML format. "
             "Defaults to 'config.yaml'.",
        default='config.yaml',
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging.",
    )
    parser.add_argument(
        "--engine", "-e",
        choices=["local", "global"],
        help="The search engine to use. Can be either 'local' or 'global'. Defaults to 'local'.",
        default="local",
    )
    parser.add_argument(
        "--stream", "-s",
        action="store_true",
        help="Enable streaming output.",
    )
    parser.add_argument(
        "--api-key", "-k",
        type=str,
        help="The API key to use for authentication.",
    )
    parser.add_argument(
        "--base-url", "-b",
        type=str,
        help="The base URL to use for the API.",
    )
    parser.add_argument(
        "text",
        type=str,
        help="The text to search for.",
        nargs=1,
    )
    parser.add_argument(
        "-V", "--version",
        action="version",
        version="%(prog)s" + __version__,
    )

    def _help() -> None:
        parser.print_help()
        sys.exit(0)

    parser.set_defaults(func=_help)

    return _Args.parse_obj(parser.parse_args())


def main() -> int:
    try:
        _main()
    except _errors.CLIError as err:
        msg = _utils.parse_cli_err(err)
        sys.stderr.write(f"Error Occurred: \n{msg}\n")
        return 1
    except KeyboardInterrupt:
        sys.stderr.write("\n")
        return 1
    return 0


def _main() -> None:
    try:
        args = _parse_args()
    except pydantic.ValidationError as err:
        err: pydantic.ValidationError
        raise _errors.InvalidParameterError.from_pydantic_validation_error(err)

    raise NotImplementedError("Not implemented yet")  # TODO: Implement the rest of the function
