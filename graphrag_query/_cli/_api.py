# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import collections
import sys
import types
import typing

import typing_extensions

from . import _utils
from .. import (
    _base_client,
    _client,
    _config,
    types as _types,
)
from .._search import _types as _search_types


class GraphRAGCli(_base_client.ContextManager):
    _verbose: bool
    _engine: typing.Literal['local', 'global']
    _stream: bool
    _conversation_history: typing.Deque[typing.Dict[typing.Literal['role', 'content'], str]]
    _graphrag_client: _client.GraphRAGClient

    @property
    def stream(self) -> bool:
        return self._stream

    def __init__(
        self,
        *,
        verbose: bool,
        chat_llm_base_url: typing.Optional[str],
        chat_llm_api_key: str,
        chat_llm_model: str,
        embedding_base_url: typing.Optional[str],
        embedding_api_key: str,
        embedding_model: str,
        context_dir: str,
        engine: typing.Literal['local', 'global'],
        stream: bool,
    ):
        self._verbose = verbose
        self._engine = engine
        self._stream = stream
        self._conversation_history = collections.deque(maxlen=10)
        self._logger = _utils.CLILogger()

        self._graphrag_client = _client.GraphRAGClient(
            config=_config.GraphRAGConfig(
                chat_llm=_config.ChatLLMConfig(
                    base_url=chat_llm_base_url,
                    api_key=chat_llm_api_key,
                    model=chat_llm_model,
                ),
                embedding=_config.EmbeddingConfig(
                    base_url=embedding_base_url,
                    api_key=embedding_api_key,
                    model=embedding_model,
                ),
                context=_config.ContextConfig(
                    directory=context_dir,
                ),
                logging=_config.LoggingConfig(
                    enabled=verbose,
                ),
            ),
            logger=self._logger,
        )

    def chat(self, message: str, **kwargs: typing.Any) -> typing.Union[typing.Iterator[str], str]:
        self._conversation_history.append({'role': 'user', 'content': message})
        response = self._graphrag_client.chat(
            engine=self._engine,
            message=typing.cast(_types.MessageParam_T, self._conversation_history),
            stream=self._stream,
            **kwargs,
        )
        if self._stream:
            response = typing.cast(_search_types.StreamSearchResult_T, response)
            return self._parse_stream_response(response)
        else:
            response = typing.cast(_search_types.SearchResult_T, response)
            return self._parse_response(response)

    def clear_history(self) -> None:
        self._conversation_history.clear()

    def _parse_stream_response(self, response: _search_types.StreamSearchResult_T) -> typing.Iterator[str]:
        content = ''
        response = typing.cast(_search_types.StreamSearchResult_T, response)
        for chunk in response:
            sys.stdout.write(chunk.choice.delta.content or '')
            sys.stdout.flush()
            yield chunk.choice.delta.content or ''
            content += chunk.choice.delta.content or ''
        sys.stdout.write('\n')
        sys.stdout.flush()
        self._conversation_history.append({'role': 'assistant', 'content': content})

    def _parse_response(self, response: _search_types.SearchResult_T) -> str:
        response = typing.cast(_search_types.SearchResult_T, response)
        sys.stdout.write(str(response.choice.message.content) or '')
        sys.stdout.write('\n')
        sys.stdout.flush()
        self._conversation_history.append({'role': 'assistant', 'content': str(response.choice.message.content)})
        return str(response.choice.message.content)

    def close(self) -> None:
        self._graphrag_client.close()

    @typing_extensions.override
    def __enter__(self) -> GraphRAGCli:
        return self

    @typing_extensions.override
    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        traceback: typing.Optional[types.TracebackType],
    ) -> typing.Literal[False]:
        self.close()
        return False

    @typing_extensions.override
    def __str__(self):
        return str(self._graphrag_client)

    @typing_extensions.override
    def __repr__(self):
        return repr(self._graphrag_client)


class AsyncGraphRAGCli(_base_client.AsyncContextManager):
    _verbose: bool
    _engine: typing.Literal['local', 'global']
    _stream: bool
    _conversation_history: typing.Deque[typing.Dict[typing.Literal['role', 'content'], str]]
    _graphrag_client: _client.AsyncGraphRAGClient

    def __init__(
        self,
        *,
        verbose: bool,
        chat_llm_base_url: typing.Optional[str],
        chat_llm_api_key: str,
        chat_llm_model: str,
        embedding_base_url: typing.Optional[str],
        embedding_api_key: str,
        embedding_model: str,
        context_dir: str,
        engine: typing.Literal['local', 'global'],
        stream: bool,
    ):
        self._verbose = verbose
        self._engine = engine
        self._stream = stream
        self._conversation_history = collections.deque(maxlen=10)  # only keep the last 10 messages
        self._logger = _utils.CLILogger()
        self._graphrag_client = _client.AsyncGraphRAGClient(
            config=_config.GraphRAGConfig(
                chat_llm=_config.ChatLLMConfig(
                    base_url=chat_llm_base_url,
                    api_key=chat_llm_api_key,
                    model=chat_llm_model,
                ),
                embedding=_config.EmbeddingConfig(
                    base_url=embedding_base_url,
                    api_key=embedding_api_key,
                    model=embedding_model,
                ),
                context=_config.ContextConfig(
                    directory=context_dir,
                ),
                logging=_config.LoggingConfig(
                    enabled=verbose,
                ),
            ),
            logger=self._logger,
        )

    async def chat(self, message: str, **kwargs: typing.Any) -> None:
        self._conversation_history.append({'role': 'user', 'content': message})
        response = await self._graphrag_client.chat(
            engine=self._engine,
            message=typing.cast(_types.MessageParam_T, self._conversation_history),
            stream=self._stream,
            **kwargs,
        )
        if self._stream:
            content = ''
            response = typing.cast(_search_types.AsyncStreamSearchResult_T, response)
            async for chunk in response:
                sys.stdout.write(chunk.choice.delta.content or '')
                sys.stdout.flush()
                content += chunk.choice.delta.content or ''
            sys.stdout.write('\n')
            sys.stdout.flush()
            self._conversation_history.append({'role': 'assistant', 'content': content})
        else:
            response = typing.cast(_search_types.SearchResult_T, response)
            sys.stdout.write(str(response.choice.message.content) or '')
            sys.stdout.write('\n')
            sys.stdout.flush()
            self._conversation_history.append({'role': 'assistant', 'content': str(response.choice.message.content)})

    async def close(self) -> None:
        await self._graphrag_client.close()

    @typing_extensions.override
    async def __aenter__(self) -> AsyncGraphRAGCli:
        return self

    @typing_extensions.override
    async def __aexit__(
        self,
        exc_type: typing.Optional[typing.Type[BaseException]],
        exc_value: typing.Optional[BaseException],
        traceback: typing.Optional[types.TracebackType],
    ) -> typing.Literal[False]:
        await self.close()
        return False

    @typing_extensions.override
    def __str__(self):
        return str(self._graphrag_client)

    @typing_extensions.override
    def __repr__(self):
        return repr(self._graphrag_client)
