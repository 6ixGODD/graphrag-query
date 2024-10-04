from __future__ import annotations

from typing import (
    Any,
    cast,
    Optional,
    Union,
)

import httpx
import openai

from ... import _utils
from ..._search._llm import _base, _types


class ChatLLM(_base.BaseChatLLM):
    def __init__(
        self,
        *,
        model: str,
        api_key: str,
        organization: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        http_client: Optional[httpx.Client] = None,
        **kwargs: Any
    ) -> None:
        self._client = openai.OpenAI(
            api_key=api_key,
            organization=organization,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            http_client=http_client,
            **_utils.filter_kwargs(openai.OpenAI, kwargs)
        )
        self._model = model

    def chat(
        self,
        msg: _types.MessageParam_T,
        *,
        stream: bool = False,
        **kwargs: Any
    ) -> Union[_types.ChatResponse_T, _types.SyncChatStreamResponse_T]:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=msg,
            stream=stream,
            **_utils.filter_kwargs(self._client.chat.completions.create, kwargs)
        )

        return cast(_types.ChatCompletion, response) \
            if not stream else (cast(_types.ChatCompletionChunk, c) for c in response)

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str) -> None:
        self._model = value


class AsyncChatLLM(_base.BaseAsyncChatLLM):
    def __init__(
        self,
        *,
        model: str,
        api_key: str,
        organization: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        max_retries: int = 3,
        http_client: Optional[httpx.AsyncClient] = None,
        **kwargs: Any
    ) -> None:
        self._aclient = openai.AsyncOpenAI(
            api_key=api_key,
            organization=organization,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            http_client=http_client,
            **_utils.filter_kwargs(openai.AsyncOpenAI, kwargs)
        )
        self._model = model

    async def achat(
        self,
        msg: _types.MessageParam_T,
        *,
        stream: bool = False,
        **kwargs: Any
    ) -> Union[_types.ChatResponse_T, _types.AsyncChatStreamResponse_T]:
        response = await self._aclient.chat.completions.create(
            model=self._model,
            messages=msg,
            stream=stream,
            **_utils.filter_kwargs(self._aclient.chat.completions.create, kwargs)
        )

        return cast(_types.ChatCompletion, response) if not stream else (
            c async for c in cast(_types.AsyncChatStreamResponse_T, response)
        )

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str) -> None:
        self._model = value
