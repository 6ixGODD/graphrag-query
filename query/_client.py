from __future__ import annotations

from os import PathLike
from pathlib import Path
from typing import Any, Dict, Self, Union

import tiktoken

from . import _config as _cfg, _defaults
from ._search import (
    AsyncChatLLM,
    AsyncGlobalSearchEngine,
    AsyncLocalSearchEngine,
    ChatLLM,
    Embedding,
    GlobalContextLoader,
    GlobalSearchEngine,
    LocalContextLoader,
    LocalSearchEngine,
)

__all__ = [
    'GraphRAGClient',
    'AsyncGraphRAGClient',
]


class GraphRAGClient:
    _config: _cfg.GraphRAGConfig
    _chat_llm: ChatLLM
    _embedding: Embedding
    _local_context_loader: LocalContextLoader
    _global_context_loader: GlobalContextLoader
    _local_search_engine: LocalSearchEngine
    _global_search_engine: GlobalSearchEngine
    _logger: Any = None  # TODO: protocol class for logger

    @classmethod
    def from_config_file(cls, config_file: Union[PathLike[str], Path]) -> Self:
        return cls(config=_cfg.GraphRAGConfig.from_config_file(config_file))

    @classmethod
    def from_config_dict(cls, config_dict: Dict[str, Any]) -> Self:
        return cls(config=_cfg.GraphRAGConfig(**config_dict))

    def __init__(
        self,
        *,
        config: _cfg.GraphRAGConfig,
        logger: Any = None,
    ) -> None:
        self._config = config
        self._logger = logger or _defaults.get_default_logger() if self._config.logging.enabled else None

        self._chat_llm = ChatLLM(
            model=self._config.chat_llm.model,
            api_key=self._config.chat_llm.api_key,
            organization=self._config.chat_llm.organization,
            base_url=self._config.chat_llm.base_url,
            timeout=self._config.chat_llm.timeout,
            max_retries=self._config.chat_llm.max_retries,
            **(self._config.chat_llm.kwargs or {}),
        )

        self._embedding = Embedding(
            model=self._config.embedding.model,
            api_key=self._config.embedding.api_key,
            organization=self._config.embedding.organization,
            base_url=self._config.embedding.base_url,
            timeout=self._config.embedding.timeout,
            max_retries=self._config.embedding.max_retries,
            max_tokens=self._config.embedding.max_tokens,
            token_encoder=tiktoken.get_encoding(
                self._config.embedding.token_encoder
            )
            if self._config.embedding.token_encoder
            else None,
            **(self._config.embedding.kwargs or {}),
        )

        self._local_context_loader = LocalContextLoader.from_parquet_directory(
            self._config.context.directory,
            **(self._config.context.kwargs or {}),
        )

        self._global_context_loader = GlobalContextLoader.from_parquet_directory(
            self._config.context.directory,
            **(self._config.context.kwargs or {}),
        )

        self._local_search_engine = LocalSearchEngine(
            chat_llm=self._chat_llm,
            embedding=self._embedding,
            context_loader=self._local_context_loader,
            sys_prompt=self._config.local_search.sys_prompt,
            community_level=self._config.local_search.community_level,
            store_coll_name=self._config.local_search.store_coll_name,
            store_uri=self._config.local_search.store_uri,
            encoding_model=self._config.local_search.encoding_model,
            logger=self._logger,
            **(self._config.local_search.kwargs or {}),
        )
        self._global_search_engine = GlobalSearchEngine(
            chat_llm=self._chat_llm,
            embedding=self._embedding,
            context_loader=self._global_context_loader,
            map_sys_prompt=self._config.global_search.map_sys_prompt,
            reduce_sys_prompt=self._config.global_search.reduce_sys_prompt,
            allow_general_knowledge=self._config.global_search.allow_general_knowledge,
            general_knowledge_sys_prompt=self._config.global_search.general_knowledge_sys_prompt,
            no_data_answer=self._config.global_search.no_data_answer,
            json_mode=self._config.global_search.json_mode,
            max_data_tokens=self._config.global_search.max_data_tokens,
            community_level=self._config.global_search.community_level,
            encoding_model=self._config.global_search.encoding_model,
            logger=self._logger,
            **(self._config.global_search.kwargs or {}),
        )


class AsyncGraphRAGClient:
    _config: _cfg.GraphRAGConfig
    _chat_llm: AsyncChatLLM
    _embedding: Embedding
    _local_context_loader: LocalContextLoader
    _global_context_loader: GlobalContextLoader
    _local_search_engine: AsyncLocalSearchEngine
    _global_search_engine: AsyncGlobalSearchEngine
    _logger: Any

    @classmethod
    def from_config_file(cls, config_file: Union[PathLike[str], Path]) -> Self:
        return cls(config=_cfg.GraphRAGConfig.from_config_file(config_file))

    @classmethod
    def from_config_dict(cls, config_dict: Dict[str, Any]) -> Self:
        return cls(config=_cfg.GraphRAGConfig(**config_dict))

    def __init__(
        self,
        *,
        config: _cfg.GraphRAGConfig,
        logger: Any = None,
    ) -> None:
        self._config = config
        self._logger = logger or _defaults.get_default_logger() if self._config.logging.enabled else None

        self._chat_llm = AsyncChatLLM(
            model=self._config.chat_llm.model,
            api_key=self._config.chat_llm.api_key,
            organization=self._config.chat_llm.organization,
            base_url=self._config.chat_llm.base_url,
            timeout=self._config.chat_llm.timeout,
            max_retries=self._config.chat_llm.max_retries,
            **(self._config.chat_llm.kwargs or {}),
        )

        self._embedding = Embedding(
            model=self._config.embedding.model,
            api_key=self._config.embedding.api_key,
            organization=self._config.embedding.organization,
            base_url=self._config.embedding.base_url,
            timeout=self._config.embedding.timeout,
            max_retries=self._config.embedding.max_retries,
            max_tokens=self._config.embedding.max_tokens,
            token_encoder=tiktoken.get_encoding(
                self._config.embedding.token_encoder
            )
            if self._config.embedding.token_encoder
            else None,
            **(self._config.embedding.kwargs or {}),
        )

        self._local_context_loader = LocalContextLoader.from_parquet_directory(
            self._config.context.directory,
            **(self._config.context.kwargs or {}),
        )

        self._global_context_loader = GlobalContextLoader.from_parquet_directory(
            self._config.context.directory,
            **(self._config.context.kwargs or {}),
        )

        self._local_search_engine = AsyncLocalSearchEngine(
            chat_llm=self._chat_llm,
            embedding=self._embedding,
            context_loader=self._local_context_loader,
            sys_prompt=self._config.local_search.sys_prompt,
            community_level=self._config.local_search.community_level,
            store_coll_name=self._config.local_search.store_coll_name,
            store_uri=self._config.local_search.store_uri,
            encoding_model=self._config.local_search.encoding_model,
            logger=self._logger,
            **(self._config.local_search.kwargs or {}),
        )

        self._global_search_engine = AsyncGlobalSearchEngine(
            chat_llm=self._chat_llm,
            embedding=self._embedding,
            context_loader=self._global_context_loader,
            map_sys_prompt=self._config.global_search.map_sys_prompt,
            reduce_sys_prompt=self._config.global_search.reduce_sys_prompt,
            allow_general_knowledge=self._config.global_search.allow_general_knowledge,
            general_knowledge_sys_prompt=self._config.global_search.general_knowledge_sys_prompt,
            no_data_answer=self._config.global_search.no_data_answer,
            json_mode=self._config.global_search.json_mode,
            max_data_tokens=self._config.global_search.max_data_tokens,
            community_level=self._config.global_search.community_level,
            encoding_model=self._config.global_search.encoding_model,
            logger=self._logger,
            **(self._config.global_search.kwargs or {}),
        )
