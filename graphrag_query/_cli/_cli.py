# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import argparse
import asyncio
import sys
import typing
import warnings

import pydantic

from . import (
    _api,
    _utils,
)
from .. import (
    __version__,
    errors as _errors,
)


class _Args(pydantic.BaseModel):
    verbose: bool
    engine: typing.Annotated[
        typing.Literal['local', 'global'],
        pydantic.Field(..., pattern=r"local|global")
    ]
    stream: bool
    chat_api_key: str
    chat_base_url: typing.Annotated[
        typing.Optional[str],
        pydantic.Field(..., pattern=r"https?://([a-zA-Z0-9\-.]+\.[a-zA-Z]{2,})(:[0-9]{1,5})?(/\s*)?")
    ]
    chat_model: str
    embedding_api_key: str
    embedding_base_url: typing.Annotated[
        typing.Optional[str],
        pydantic.Field(..., pattern=r"https?://([a-zA-Z0-9\-.]+\.[a-zA-Z]{2,})(:[0-9]{1,5})?(/\s*)?")
    ]
    embedding_model: str
    context_dir: str
    mode: typing.Annotated[
        typing.Literal['console', 'gui'],
        pydantic.Field(..., pattern=r"console|gui")
    ]


def _parse_args() -> _Args:
    parser = argparse.ArgumentParser(
        description="GraphRAG Query CLI",
        prog="python -m query",
        add_help=True,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="enable verbose logging",
    )
    parser.add_argument(
        "--engine", "-e",
        choices=["local", "global"],
        help="engine to use for the query",
        default="local",
    )
    parser.add_argument(
        "--stream", "-s",
        action="store_true",
        help="enable streaming output",
    )
    parser.add_argument(
        "--chat-api-key", "-k",
        type=str,
        required=True,
        help="API key for the Chat API",
    )
    parser.add_argument(
        "--chat-base-url", "-b",
        type=str,
        help="base URL for the chat API",
        default=None,
    )
    parser.add_argument(
        "--chat-model", "-m",
        type=str,
        required=True,
        help="model to use for the chat API",
    )
    parser.add_argument(
        "--embedding-api-key", "-K",
        type=str,
        required=True,
        help="API key for the embedding API",
    )
    parser.add_argument(
        "--embedding-base-url", "-B",
        type=str,
        help="base URL for the embedding API",
        default=None,
    )
    parser.add_argument(
        "--embedding-model", "-M",
        type=str,
        required=True,
        help="model to use for the embedding API",
    )
    parser.add_argument(
        "--context-dir", "-c",
        type=str,
        required=True,
        help="directory containing the context data",
    )
    parser.add_argument(
        "--mode", "-o",
        type=str,
        help="mode to execute the GraphRAG engine",
        choices=["console", "gui"],
        default="console",
    )

    parser.add_argument(
        "-V", "--version",
        action="version",
        version=__version__,
    )

    def _help() -> None:
        parser.print_help()
        sys.exit(0)

    parser.set_defaults(func=_help)

    return _Args.parse_obj(parser.parse_args().__dict__)


def main() -> int:
    warnings.filterwarnings("ignore", category=_errors.GraphRAGWarning)
    try:
        _main()
    except _errors.CLIError as err:
        msg = _utils.parse_cli_err(err)
        sys.stderr.write(f"Error Occurred: \n{msg}\n")
        sys.stderr.flush()
        return 1
    except KeyboardInterrupt:
        sys.stdout.write("\nBye!\n")
        sys.stdout.flush()
        return 0
    return 0


def _main() -> None:
    try:
        args = _parse_args()
    except pydantic.ValidationError as err:
        raise _errors.InvalidParameterError.from_pydantic_validation_error(err)

    cli: typing.Union[_api.AsyncGraphRAGCli, _api.GraphRAGCli]
    if args.mode == "console":
        sys.stdout.write("=== GraphRAG Query CLI ===\n\n")
        sys.stdout.write("Loading GraphRAG engine...\n\n")
        sys.stdout.flush()
        cli = _api.AsyncGraphRAGCli(
            verbose=args.verbose,
            chat_llm_base_url=args.chat_base_url,
            chat_llm_api_key=args.chat_api_key,
            chat_llm_model=args.chat_model,
            embedding_base_url=args.embedding_base_url,
            embedding_api_key=args.embedding_api_key,
            embedding_model=args.embedding_model,
            context_dir=args.context_dir,
            engine=args.engine,
            stream=args.stream,
        )
        sys.stdout.write("GraphRAG engine loaded.\n\n")

        asyncio.run(_chat_loop(cli))
    else:
        from . import _qt
        cli = _api.GraphRAGCli(
            verbose=args.verbose,
            chat_llm_base_url=args.chat_base_url,
            chat_llm_api_key=args.chat_api_key,
            chat_llm_model=args.chat_model,
            embedding_base_url=args.embedding_base_url,
            embedding_api_key=args.embedding_api_key,
            embedding_model=args.embedding_model,
            context_dir=args.context_dir,
            engine=args.engine,
            stream=args.stream,
        )
        _qt.main(cli)


async def _chat_loop(cli: _api.AsyncGraphRAGCli) -> None:
    async with cli:
        while True:
            user_input = input("You (type 'exit' to quit) >> ")
            if user_input.lower().strip() == "exit":
                break
            sys.stdout.write("Assistant >> \n")
            sys.stdout.flush()
            await cli.chat(user_input)
            sys.stdout.write("\n")
            sys.stdout.flush()
        sys.stdout.write("Bye!\n")
        sys.stdout.flush()
