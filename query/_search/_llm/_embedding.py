from __future__ import annotations

from typing import (
    Any,
    List,
    Optional,
)

import httpx
import openai
import tiktoken

from ... import _utils
from ..._search._llm import _base, _types


class Embedding(_base.BaseEmbedding):

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
        max_tokens: int = 8191,
        token_encoder: tiktoken.Encoding = tiktoken.get_encoding("cl100k_base"),
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
        self._max_tokens = max_tokens
        self._token_encoder = token_encoder

    def embed(self, text: str, **kwargs: Any) -> _types.EmbeddingResponse_T:
        chunk_embeddings: List[List[float]] = []
        chunk_lens: List[int] = []
        for chunk in _utils.chunk_text(text, self._max_tokens):
            embedding = self._client.embeddings.create(
                input=chunk,
                model=self._model,
                **_utils.filter_kwargs(self._client.embeddings.create, kwargs)
            ).data[0].embedding or []
            chunk_embeddings.append(embedding)
            chunk_lens.append(chunk.__len__() or 0)
        return _utils.combine_embeddings(chunk_embeddings, chunk_lens)

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str) -> None:
        self._model = value


class AsyncEmbedding(_base.BaseAsyncEmbedding):
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
        max_tokens: int = 8191,
        token_encoder: tiktoken.Encoding = tiktoken.get_encoding("cl100k_base"),
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
        self._max_tokens = max_tokens
        self._token_encoder = token_encoder

    async def aembed(self, text: str, **kwargs: Any) -> List[float]:
        chunk_embeddings: List[List[float]] = []
        chunk_lens: List[int] = []
        for chunk in _utils.chunk_text(text, self._max_tokens):
            embedding = (await self._aclient.embeddings.create(
                input=chunk,
                model=self._model,
                **_utils.filter_kwargs(self._aclient.embeddings.create, kwargs)
            )).data[0].embedding or []
            chunk_embeddings.append(embedding)
            chunk_lens.append(chunk.__len__() or 0)
        return _utils.combine_embeddings(chunk_embeddings, chunk_lens)

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str) -> None:
        self._model = value
