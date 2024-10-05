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

import abc
import typing

import openai
import typing_extensions

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

    @typing_extensions.override
    def __str__(self) -> str:
        return f"ChatLLM(model={self.model})"

    @typing_extensions.override
    def __repr__(self) -> str:
        return self.__str__()


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

    @typing_extensions.override
    def __str__(self) -> str:
        return f"AsyncChatLLM(model={self.model})"

    @typing_extensions.override
    def __repr__(self) -> str:
        return self.__str__()


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

    @typing_extensions.override
    def __str__(self) -> str:
        return f"Embedding(model={self.model})"

    @typing_extensions.override
    def __repr__(self) -> str:
        return self.__str__()


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

    @typing_extensions.override
    def __str__(self) -> str:
        return f"AsyncEmbedding(model={self.model})"

    @typing_extensions.override
    def __repr__(self) -> str:
        return self.__str__()
