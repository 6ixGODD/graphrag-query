# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import typing

import httpx
import openai
import typing_extensions

from ... import _utils
from . import _base_llm, _types


class ChatLLM(_base_llm.BaseChatLLM):
    def __init__(
        self,
        *,
        model: str,
        api_key: str,
        organization: typing.Optional[str] = None,
        base_url: typing.Optional[str] = None,
        timeout: typing.Optional[float] = None,
        max_retries: typing.Optional[int] = None,
        http_client: typing.Optional[httpx.Client] = None,
        **kwargs: typing.Any
    ) -> None:
        self._client = openai.OpenAI(
            api_key=api_key,
            organization=organization,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries or 3,
            http_client=http_client,
            **_utils.filter_kwargs(openai.OpenAI, kwargs)
        )
        self._model = model

    @typing_extensions.override
    def chat(
        self,
        msg: _types.MessageParam_T,
        *,
        stream: bool = False,
        **kwargs: typing.Any
    ) -> typing.Union[_types.ChatResponse_T, _types.SyncChatStreamResponse_T]:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=msg,
            stream=stream,
            **_utils.filter_kwargs(self._client.chat.completions.create, kwargs)
        )

        return typing.cast(_types.ChatCompletion, response) \
            if not stream else (typing.cast(_types.ChatCompletionChunk, c) for c in response)

    @property
    @typing_extensions.override
    def model(self) -> str:
        return self._model

    @model.setter
    @typing_extensions.override
    def model(self, value: str) -> None:
        self._model = value

    @typing_extensions.override
    def close(self) -> None:
        self._client.close()


class AsyncChatLLM(_base_llm.BaseAsyncChatLLM):
    def __init__(
        self,
        *,
        model: str,
        api_key: str,
        organization: typing.Optional[str] = None,
        base_url: typing.Optional[str] = None,
        timeout: typing.Optional[float] = None,
        max_retries: typing.Optional[int] = None,
        http_client: typing.Optional[httpx.AsyncClient] = None,
        **kwargs: typing.Any
    ) -> None:
        self._aclient = openai.AsyncOpenAI(
            api_key=api_key,
            organization=organization,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries or 3,
            http_client=http_client,
            **_utils.filter_kwargs(openai.AsyncOpenAI, kwargs)
        )
        self._model = model

    @typing_extensions.override
    async def achat(
        self,
        msg: _types.MessageParam_T,
        *,
        stream: bool = False,
        **kwargs: typing.Any
    ) -> typing.Union[_types.ChatResponse_T, _types.AsyncChatStreamResponse_T]:
        response = await self._aclient.chat.completions.create(
            model=self._model,
            messages=msg,
            stream=stream,
            **_utils.filter_kwargs(self._aclient.chat.completions.create, kwargs)
        )

        return typing.cast(_types.ChatCompletion, response) if not stream else (
            c async for c in typing.cast(_types.AsyncChatStreamResponse_T, response)
        )

    @property
    @typing_extensions.override
    def model(self) -> str:
        return self._model

    @model.setter
    @typing_extensions.override
    def model(self, value: str) -> None:
        self._model = value

    @typing_extensions.override
    async def aclose(self) -> None:
        await self._aclient.close()
