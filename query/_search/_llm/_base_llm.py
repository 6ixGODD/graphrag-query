from __future__ import annotations

import abc
import typing

import openai

from ..._search._llm import _types


class BaseChatLLM(abc.ABC):
    _client: openai.OpenAI

    @abc.abstractmethod
    def chat(
        self,
        msg: _types.MessageParam_T,
        *,
        stream: bool,
        **kwargs: typing.Any
    ) -> typing.Union[_types.ChatResponse_T, _types.SyncChatStreamResponse_T]: ...

    @property
    @abc.abstractmethod
    def model(self) -> str: ...

    @model.setter
    @abc.abstractmethod
    def model(self, value: str) -> None: ...


class BaseAsyncChatLLM(abc.ABC):
    _aclient: openai.AsyncOpenAI

    @abc.abstractmethod
    async def achat(
        self,
        msg: _types.MessageParam_T,
        *,
        stream: bool,
        **kwargs: typing.Any
    ) -> typing.Union[_types.ChatResponse_T, _types.AsyncChatStreamResponse_T]: ...

    @property
    @abc.abstractmethod
    def model(self) -> str: ...

    @model.setter
    @abc.abstractmethod
    def model(self, value: str) -> None: ...


class BaseEmbedding(abc.ABC):
    _client: openai.OpenAI

    @abc.abstractmethod
    def embed(self, text: str, **kwargs: typing.Any) -> _types.EmbeddingResponse_T: ...

    @property
    @abc.abstractmethod
    def model(self) -> str: ...

    @model.setter
    @abc.abstractmethod
    def model(self, value: str) -> None: ...


class BaseAsyncEmbedding(abc.ABC):
    _aclient: openai.AsyncOpenAI

    @abc.abstractmethod
    async def aembed(self, text: str, **kwargs: typing.Any) -> _types.EmbeddingResponse_T: ...

    @property
    @abc.abstractmethod
    def model(self) -> str: ...

    @model.setter
    @abc.abstractmethod
    def model(self, value: str) -> None: ...
