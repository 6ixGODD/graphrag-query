from __future__ import annotations

from abc import ABC, abstractmethod
from typing import (
    Any,
    Union,
)

import openai

from ..._search._llm import _types


class BaseChatLLM(ABC):
    _client: openai.OpenAI

    @abstractmethod
    def chat(
        self,
        msg: _types.MessageParam_T,
        *,
        stream: bool,
        **kwargs: Any
    ) -> Union[_types.ChatResponse_T, _types.SyncChatStreamResponse_T]: ...

    @property
    @abstractmethod
    def model(self) -> str: ...

    @model.setter
    @abstractmethod
    def model(self, value: str) -> None: ...


class BaseAsyncChatLLM(ABC):
    _aclient: openai.AsyncOpenAI

    @abstractmethod
    async def achat(
        self,
        msg: _types.MessageParam_T,
        *,
        stream: bool,
        **kwargs: Any
    ) -> Union[_types.ChatResponse_T, _types.AsyncChatStreamResponse_T]: ...

    @property
    @abstractmethod
    def model(self) -> str: ...

    @model.setter
    @abstractmethod
    def model(self, value: str) -> None: ...


class BaseEmbedding(ABC):
    _client: openai.OpenAI

    @abstractmethod
    def embed(self, text: str, **kwargs: Any) -> _types.EmbeddingResponse_T: ...

    @property
    @abstractmethod
    def model(self) -> str: ...

    @model.setter
    @abstractmethod
    def model(self, value: str) -> None: ...


class BaseAsyncEmbedding(ABC):
    _aclient: openai.AsyncOpenAI

    @abstractmethod
    async def aembed(self, text: str, **kwargs: Any) -> _types.EmbeddingResponse_T: ...

    @property
    @abstractmethod
    def model(self) -> str: ...

    @model.setter
    @abstractmethod
    def model(self, value: str) -> None: ...
