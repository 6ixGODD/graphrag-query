# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import abc
import time
import typing

import pandas as pd
import typing_extensions

from .. import (
    _context,
    _llm,
    _types,
)
from ... import types as _base_types

Logger: typing.TypeAlias = _base_types.Logger


class QueryEngine(abc.ABC):
    _chat_llm: _llm.BaseChatLLM
    _embedding: _llm.BaseEmbedding
    _context_builder: _context.BaseContextBuilder
    _logger: typing.Optional[Logger]

    @property
    @abc.abstractmethod
    def context_builder(self) -> _context.BaseContextBuilder:
        ...

    def __init__(
        self,
        *,
        chat_llm: _llm.BaseChatLLM,
        embedding: _llm.BaseEmbedding,
        context_builder: _context.BaseContextBuilder,
        logger: typing.Optional[Logger] = None,
    ):
        self._chat_llm = chat_llm
        self._embedding = embedding
        self._context_builder = context_builder
        self._logger = logger

    @abc.abstractmethod
    def search(
        self,
        query: str,
        *,
        conversation_history: _types.ConversationHistory_T = None,
        verbose: bool = True,
        stream: bool = False,
        **kwargs: typing.Any,
    ) -> typing.Union[_types.SearchResult_T, _types.StreamSearchResult_T]:
        ...

    def _parse_result(
        self,
        result: _llm.ChatResponse_T,
        *,
        verbose: bool,
        created: float,
        context_data: typing.Optional[typing.Dict[str, pd.DataFrame]] = None,
        context_text: typing.Optional[typing.Union[str, typing.List[str]]] = None,
        map_result: typing.Optional[typing.List[_types.SearchResult]] = None,
        reduce_context_data: typing.Optional[typing.Dict[str, pd.DataFrame]] = None,
        reduce_context_text: typing.Optional[typing.Union[str, typing.List[str]]] = None,
    ) -> _types.SearchResult_T:
        usage = _types.Usage(
            completion_tokens=result.usage.completion_tokens,
            prompt_tokens=result.usage.prompt_tokens,
            total_tokens=result.usage.total_tokens,
        ) if result.usage else None
        if not verbose:
            return _types.SearchResult(
                created=created.__int__(),
                model=self._chat_llm.model,
                system_fingerprint=result.system_fingerprint,
                choice=_types.Choice(
                    finish_reason=result.choices[0].finish_reason,
                    message=_types.Message(
                        content=result.choices[0].message.content,
                        refusal=result.choices[0].message.refusal,
                    ),
                ),
                usage=usage,
            )
        else:
            return _types.SearchResultVerbose(
                created=created.__int__(),
                model=self._chat_llm.model,
                system_fingerprint=result.system_fingerprint,
                choice=_types.Choice(
                    finish_reason=result.choices[0].finish_reason,
                    message=_types.Message(
                        content=result.choices[0].message.content,
                        refusal=result.choices[0].message.refusal,
                    ),
                ),
                usage=usage,
                context_data=context_data,
                context_text=context_text,
                completion_time=time.time() - created,
                llm_calls=1,
                map_result=map_result,
                reduce_context_data=reduce_context_data,
                reduce_context_text=reduce_context_text,
            )

    def _parse_stream_result(
        self,
        result: _llm.SyncChatStreamResponse_T,
        *,
        verbose: bool,
        created: float,
        context_data: typing.Optional[typing.Dict[str, pd.DataFrame]] = None,
        context_text: typing.Optional[typing.Union[str, typing.List[str]]] = None,
        map_result: typing.Optional[typing.List[_types.SearchResult]] = None,
        reduce_context_data: typing.Optional[typing.Dict[str, pd.DataFrame]] = None,
        reduce_context_text: typing.Optional[typing.Union[str, typing.List[str]]] = None,
    ) -> _types.StreamSearchResult_T:
        for chunk in result:
            usage = _types.Usage(
                completion_tokens=chunk.usage.completion_tokens,
                prompt_tokens=chunk.usage.prompt_tokens,
                total_tokens=chunk.usage.total_tokens,
            ) if chunk.usage else None
            if not verbose:
                yield _types.SearchResultChunk(
                    created=created.__int__(),
                    model=self._chat_llm.model,
                    system_fingerprint=chunk.system_fingerprint,
                    choice=_types.ChunkChoice(
                        finish_reason=chunk.choices[0].finish_reason,
                        delta=_types.Delta(
                            content=chunk.choices[0].delta.content,
                            refusal=chunk.choices[0].delta.refusal,
                        ),
                    ),
                    usage=usage,
                )
            else:
                if chunk.choices[0].finish_reason == "stop":
                    context_data_ = context_data
                    context_text_ = context_text
                    completion_time = time.time() - created
                    llm_calls = 1
                else:
                    context_data_ = None
                    context_text_ = None
                    completion_time = None
                    llm_calls = None
                yield _types.SearchResultChunkVerbose(
                    created=created.__int__(),
                    model=self._chat_llm.model,
                    system_fingerprint=chunk.system_fingerprint,
                    choice=_types.ChunkChoice(
                        finish_reason=chunk.choices[0].finish_reason,
                        delta=_types.Delta(
                            content=chunk.choices[0].delta.content,
                            refusal=chunk.choices[0].delta.refusal,
                        ),
                    ),
                    usage=usage,
                    context_data=context_data_,
                    context_text=context_text_,
                    completion_time=completion_time,
                    llm_calls=llm_calls,
                    map_result=map_result,
                    reduce_context_data=reduce_context_data,
                    reduce_context_text=reduce_context_text,
                )

    def close(self) -> None:
        self._chat_llm.close()
        self._embedding.close()

    @typing_extensions.override
    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"\tchat_llm={self._chat_llm},\n"
            f"\tembedding={self._embedding},\n"
            f"\tcontext_builder={self._context_builder},\n"
            f"\tlogger={self._logger}\n"
            f")"
        )

    @typing_extensions.override
    def __repr__(self) -> str:
        return self.__str__()


class AsyncQueryEngine(abc.ABC):
    _chat_llm: _llm.BaseAsyncChatLLM
    _embedding: _llm.BaseEmbedding
    _context_builder: _context.BaseContextBuilder
    _logger: typing.Optional[Logger]

    @property
    @abc.abstractmethod
    def context_builder(self) -> _context.BaseContextBuilder:
        ...

    def __init__(
        self,
        *,
        chat_llm: _llm.BaseAsyncChatLLM,
        embedding: _llm.BaseEmbedding,
        context_builder: _context.BaseContextBuilder,
        logger: typing.Optional[Logger] = None,
    ):
        self._chat_llm = chat_llm
        self._embedding = embedding
        self._context_builder = context_builder
        self._logger = logger

    @abc.abstractmethod
    async def asearch(
        self,
        query: str,
        *,
        conversation_history: _types.ConversationHistory_T,
        verbose: bool = True,
        stream: bool = False,
        **kwargs: typing.Any,
    ) -> typing.Union[_types.SearchResult_T, _types.AsyncStreamSearchResult_T]:
        ...

    def _parse_result(
        self,
        result: _llm.ChatResponse_T,
        *,
        verbose: bool,
        created: float,
        context_data: typing.Optional[typing.Dict[str, pd.DataFrame]] = None,
        context_text: typing.Optional[typing.Union[str, typing.List[str]]] = None,
        map_result: typing.Optional[typing.List[_types.SearchResult]] = None,
        reduce_context_data: typing.Optional[typing.Dict[str, pd.DataFrame]] = None,
        reduce_context_text: typing.Optional[typing.Union[str, typing.List[str]]] = None,
    ) -> _types.SearchResult_T:
        usage = _types.Usage(
            completion_tokens=result.usage.completion_tokens,
            prompt_tokens=result.usage.prompt_tokens,
            total_tokens=result.usage.total_tokens,
        ) if result.usage else None
        if not verbose:
            return _types.SearchResult(
                created=created.__int__(),
                model=self._chat_llm.model,
                system_fingerprint=result.system_fingerprint,
                choice=_types.Choice(
                    finish_reason=result.choices[0].finish_reason,
                    message=_types.Message(
                        content=result.choices[0].message.content,
                        refusal=result.choices[0].message.refusal,
                    ),
                ),
                usage=usage,
            )
        else:
            return _types.SearchResultVerbose(
                created=created.__int__(),
                model=self._chat_llm.model,
                system_fingerprint=result.system_fingerprint,
                choice=_types.Choice(
                    finish_reason=result.choices[0].finish_reason,
                    message=_types.Message(
                        content=result.choices[0].message.content,
                        refusal=result.choices[0].message.refusal,
                    ),
                ),
                usage=usage,
                context_data=context_data,
                context_text=context_text,
                completion_time=time.time() - created,
                llm_calls=1,
                map_result=map_result,
                reduce_context_data=reduce_context_data,
                reduce_context_text=reduce_context_text,
            )

    async def _parse_stream_result(
        self,
        result: _llm.AsyncChatStreamResponse_T,
        *,
        verbose: bool,
        created: float,
        context_data: typing.Optional[typing.Dict[str, pd.DataFrame]] = None,
        context_text: typing.Optional[typing.Union[str, typing.List[str]]] = None,
        map_result: typing.Optional[typing.List[_types.SearchResult]] = None,
        reduce_context_data: typing.Optional[typing.Dict[str, pd.DataFrame]] = None,
        reduce_context_text: typing.Optional[typing.Union[str, typing.List[str]]] = None,
    ) -> _types.AsyncStreamSearchResult_T:
        async for chunk in result:
            usage = _types.Usage(
                completion_tokens=chunk.usage.completion_tokens,
                prompt_tokens=chunk.usage.prompt_tokens,
                total_tokens=chunk.usage.total_tokens,
            ) if chunk.usage else None
            if not verbose:
                yield _types.SearchResultChunk(
                    created=created.__int__(),
                    model=self._chat_llm.model,
                    system_fingerprint=chunk.system_fingerprint,
                    choice=_types.ChunkChoice(
                        finish_reason=chunk.choices[0].finish_reason,
                        delta=_types.Delta(
                            content=chunk.choices[0].delta.content,
                            refusal=chunk.choices[0].delta.refusal,
                        ),
                    ),
                    usage=usage,
                )
            else:
                if chunk.choices[0].finish_reason == "stop":
                    context_data_ = context_data
                    context_text_ = context_text
                    completion_time = time.time() - created
                    llm_calls = 1
                else:
                    context_data_ = None
                    context_text_ = None
                    completion_time = None
                    llm_calls = None
                yield _types.SearchResultChunkVerbose(
                    created=created.__int__(),
                    model=self._chat_llm.model,
                    system_fingerprint=chunk.system_fingerprint,
                    choice=_types.ChunkChoice(
                        finish_reason=chunk.choices[0].finish_reason,
                        delta=_types.Delta(
                            content=chunk.choices[0].delta.content,
                            refusal=chunk.choices[0].delta.refusal,
                        ),
                    ),
                    usage=usage,
                    context_data=context_data_,
                    context_text=context_text_,
                    completion_time=completion_time,
                    llm_calls=llm_calls,
                    map_result=map_result,
                    reduce_context_data=reduce_context_data,
                    reduce_context_text=reduce_context_text,
                )

    async def aclose(self) -> None:
        await self._chat_llm.aclose()
        self._embedding.close()

    @typing_extensions.override
    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}(\n"
            f"\tchat_llm={self._chat_llm},\n"
            f"\tembedding={self._embedding},\n"
            f"\tcontext_builder={self._context_builder},\n"
            f"\tlogger={self._logger}\n"
            f")"
        )

    @typing_extensions.override
    def __repr__(self) -> str:
        return self.__str__()
