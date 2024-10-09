# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import typing

import httpx
import openai
import tiktoken
import typing_extensions

from . import _base_llm, _types
from ... import _utils, errors as _errors


class Embedding(_base_llm.BaseEmbedding):
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
        max_tokens: typing.Optional[int] = None,
        token_encoder: typing.Optional[tiktoken.Encoding] = None,
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
        self._max_tokens = max_tokens or 8191
        self._token_encoder = token_encoder or tiktoken.get_encoding("cl100k_base")

    @typing_extensions.override
    def embed(self, text: str, **kwargs: typing.Any) -> _types.EmbeddingResponse_T:
        chunk_embeddings: typing.List[typing.List[float]] = []
        chunk_lens: typing.List[int] = []
        for chunk in _utils.chunk_text(text, self._max_tokens):
            try:
                embedding = self._client.embeddings.create(
                    input=chunk,
                    model=self._model,
                    **_utils.filter_kwargs(self._client.embeddings.create, kwargs)
                ).data[0].embedding or []
            except openai.APIError as e:
                raise _errors.OpenAIAPIError(e) from e
            chunk_embeddings.append(embedding)
            chunk_lens.append(chunk.__len__() or 0)
        return _utils.combine_embeddings(chunk_embeddings, chunk_lens)

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


class AsyncEmbedding(_base_llm.BaseAsyncEmbedding):
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
        max_tokens: typing.Optional[int] = None,
        token_encoder: typing.Optional[tiktoken.Encoding] = None,
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
        self._max_tokens = max_tokens or 8191
        self._token_encoder = token_encoder or tiktoken.get_encoding("cl100k_base")

    @typing_extensions.override
    async def aembed(self, text: str, **kwargs: typing.Any) -> typing.List[float]:
        chunk_embeddings: typing.List[typing.List[float]] = []
        chunk_lens: typing.List[int] = []
        for chunk in _utils.chunk_text(text, self._max_tokens):
            try:
                embedding = (await self._aclient.embeddings.create(
                    input=chunk,
                    model=self._model,
                    **_utils.filter_kwargs(self._aclient.embeddings.create, kwargs)
                )).data[0].embedding or []
            except openai.APIError as e:
                raise _errors.OpenAIAPIError(e) from e
            chunk_embeddings.append(embedding)
            chunk_lens.append(chunk.__len__() or 0)
        return _utils.combine_embeddings(chunk_embeddings, chunk_lens)

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
