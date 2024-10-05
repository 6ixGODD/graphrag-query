from __future__ import annotations

import os
import pathlib
import typing

import tiktoken
import typing_extensions

from . import (
    _base_client,
    _config as _cfg,  # alias for _config attribute of Client class
    _defaults,
    _search,
    errors as _errors,
    types as _types,
)

__all__ = [
    'GraphRAGClient',
    'AsyncGraphRAGClient',
]


class GraphRAGClient(
    _base_client.BaseClient[typing.Union[_types.Response_T, _types.StreamResponse_T]]
):
    _config: _cfg.GraphRAGConfig
    _chat_llm: _search.ChatLLM
    _embedding: _search.Embedding
    _local_context_loader: _search.LocalContextLoader
    _global_context_loader: _search.GlobalContextLoader
    _local_search_engine: _search.LocalSearchEngine
    _global_search_engine: _search.GlobalSearchEngine
    _logger: typing.Optional[_types.Logger]

    @classmethod
    @typing_extensions.override
    def from_config_file(cls, config_file: typing.Union[os.PathLike[str], pathlib.Path]) -> typing.Self:
        return cls(config=_cfg.GraphRAGConfig.from_config_file(config_file))

    @classmethod
    @typing_extensions.override
    def from_config_dict(cls, config_dict: typing.Dict[str, typing.Any]) -> typing.Self:
        return cls(config=_cfg.GraphRAGConfig(**config_dict))

    def __init__(
        self,
        *,
        config: _cfg.GraphRAGConfig,
        logger: typing.Optional[_types.Logger] = None,
    ) -> None:
        self._config = config
        self._logger = logger or _defaults.get_default_logger() if self._config.logging.enabled else None

        if self._logger:
            self._logger.info(f'Initializing the ChatLLM with model: {self._config.chat_llm.model}')
        self._chat_llm = _search.ChatLLM(
            model=self._config.chat_llm.model,
            api_key=self._config.chat_llm.api_key,
            organization=self._config.chat_llm.organization,
            base_url=self._config.chat_llm.base_url,
            timeout=self._config.chat_llm.timeout,
            max_retries=self._config.chat_llm.max_retries,
            **(self._config.chat_llm.kwargs or {}),
        )

        if self._logger:
            self._logger.info(f'Initializing the Embedding with model: {self._config.embedding.model}')
        self._embedding = _search.Embedding(
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

        if self._logger:
            self._logger.info(f'Initializing the LocalContextLoader with directory: {self._config.context.directory}')
        self._local_context_loader = _search.LocalContextLoader.from_parquet_directory(
            self._config.context.directory,
            **(self._config.context.kwargs or {}),
        )

        if self._logger:
            self._logger.info(f'Initializing the GlobalContextLoader with directory: {self._config.context.directory}')
        self._global_context_loader = _search.GlobalContextLoader.from_parquet_directory(
            self._config.context.directory,
            **(self._config.context.kwargs or {}),
        )

        if self._logger:
            self._logger.info('Initializing the LocalSearchEngine')
        self._local_search_engine = _search.LocalSearchEngine(
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
        if self._logger:
            self._logger.info('Initializing the GlobalSearchEngine')
        self._global_search_engine = _search.GlobalSearchEngine(
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

    @typing_extensions.override
    def chat(
        self,
        *,
        engine: typing.Literal['local', 'global'],
        message: _types.MessageParam_T,
        stream: bool = False,
        verbose: bool = False,
        **kwargs: typing.Any
    ) -> typing.Union[_types.Response_T, _types.StreamResponse_T]:
        if not self._verify_message(message):
            if self._logger:
                self._logger.error(f'Invalid message: {message}')
            raise _errors.InvalidMessageError()

        # Convert iterable objects to list
        msg_list = [typing.cast(typing.Dict[typing.Literal["role", "content"], str], msg) for msg in message]
        if engine == 'local':
            conversation_history = _search.ConversationHistory.from_list(msg_list[:-1])  # exclude the last message
            if self._logger:
                self._logger.info(f'Local search with message: {msg_list[-1]["content"]}')
            response = self._local_search_engine.search(
                msg_list[-1]['content'],
                conversation_history=conversation_history,
                stream=stream,
                verbose=verbose,
                **kwargs
            )
        elif engine == 'global':
            if self._logger:
                self._logger.info(f'Global search with message: {msg_list[-1]["content"]}')
            response = self._global_search_engine.search(
                msg_list[-1]['content'],
                stream=stream,
                verbose=verbose,
                **kwargs
            )
        else:
            raise _errors.InvalidEngineError(engine)

        return response


class AsyncGraphRAGClient(
    _base_client.BaseClient[typing.Awaitable[typing.Union[_types.Response_T, _types.AsyncStreamResponse_T]]]
):
    _config: _cfg.GraphRAGConfig
    _chat_llm: _search.AsyncChatLLM
    _embedding: _search.Embedding
    _local_context_loader: _search.LocalContextLoader
    _global_context_loader: _search.GlobalContextLoader
    _local_search_engine: _search.AsyncLocalSearchEngine
    _global_search_engine: _search.AsyncGlobalSearchEngine
    _logger: typing.Optional[_types.Logger]

    @classmethod
    @typing_extensions.override
    def from_config_file(cls, config_file: typing.Union[os.PathLike[str], pathlib.Path]) -> typing.Self:
        return cls(config=_cfg.GraphRAGConfig.from_config_file(config_file))

    @classmethod
    @typing_extensions.override
    def from_config_dict(cls, config_dict: typing.Dict[str, typing.Any]) -> typing.Self:
        return cls(config=_cfg.GraphRAGConfig(**config_dict))

    def __init__(
        self,
        *,
        config: _cfg.GraphRAGConfig,
        logger: typing.Optional[_types.Logger] = None,
    ) -> None:
        self._config = config
        self._logger = logger or _defaults.get_default_logger() if self._config.logging.enabled else None

        self._chat_llm = _search.AsyncChatLLM(
            model=self._config.chat_llm.model,
            api_key=self._config.chat_llm.api_key,
            organization=self._config.chat_llm.organization,
            base_url=self._config.chat_llm.base_url,
            timeout=self._config.chat_llm.timeout,
            max_retries=self._config.chat_llm.max_retries,
            **(self._config.chat_llm.kwargs or {}),
        )

        self._embedding = _search.Embedding(
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

        self._local_context_loader = _search.LocalContextLoader.from_parquet_directory(
            self._config.context.directory,
            **(self._config.context.kwargs or {}),
        )

        self._global_context_loader = _search.GlobalContextLoader.from_parquet_directory(
            self._config.context.directory,
            **(self._config.context.kwargs or {}),
        )

        self._local_search_engine = _search.AsyncLocalSearchEngine(
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

        self._global_search_engine = _search.AsyncGlobalSearchEngine(
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

    @typing_extensions.override
    async def chat(
        self,
        *,
        engine: typing.Literal['local', 'global'],
        message: _types.MessageParam_T,
        stream: bool = False,
        verbose: bool = False,
        **kwargs: typing.Any
    ) -> typing.Union[_types.Response_T, _types.AsyncStreamResponse_T]:
        if not self._verify_message(message):
            raise _errors.InvalidMessageError()

        # Convert iterable objects to list
        msg_list = [typing.cast(typing.Dict[typing.Literal["role", "content"], str], msg) for msg in message]

        if engine == 'local':
            conversation_history = _search.ConversationHistory.from_list(msg_list[:-1])
            response = await self._local_search_engine.asearch(
                msg_list[-1]['content'],
                conversation_history=conversation_history,
                stream=stream,
                verbose=verbose,
                **kwargs
            )
        elif engine == 'global':
            response = await self._global_search_engine.asearch(
                msg_list[-1]['content'],
                stream=stream,
                verbose=verbose,
                **kwargs
            )
        else:
            raise _errors.InvalidEngineError(engine)

        return response
