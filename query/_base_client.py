from __future__ import annotations

import abc
import os
import pathlib
import typing

from . import (
    _config as _cfg,  # alias for _config attribute of Client class
    _search,
    _types,
)

_Response_T = typing.TypeVar('_Response_T')


class BaseClient(abc.ABC, typing.Generic[_Response_T]):
    _config: _cfg.GraphRAGConfig
    _chat_llm: typing.Union[_search.ChatLLM, _search.AsyncChatLLM]
    _embedding: _search.Embedding
    _local_context_loader: _search.LocalContextLoader
    _global_context_loader: _search.GlobalContextLoader
    _local_search_engine: typing.Union[_search.LocalSearchEngine, _search.AsyncLocalSearchEngine]
    _global_search_engine: typing.Union[_search.GlobalSearchEngine, _search.AsyncGlobalSearchEngine]
    _logger: typing.Optional[_types.Logger]

    @classmethod
    @abc.abstractmethod
    def from_config_file(cls, config_file: typing.Union[os.PathLike[str], pathlib.Path]) -> typing.Self: ...

    @classmethod
    @abc.abstractmethod
    def from_config_dict(cls, config_dict: typing.Dict[str, typing.Any]) -> typing.Self: ...

    @abc.abstractmethod
    def chat(
        self,
        *,
        engine: typing.Literal['local', 'global'],
        message: _types.MessageParam_T,
        stream: bool = False,
        verbose: bool = False,
        **kwargs: typing.Any
    ) -> _Response_T: ...

    @staticmethod
    def _verify_message(message: _types.MessageParam_T) -> bool:
        msg_list = [msg for msg in message]
        return (
                all(
                    msg_list[i]['role'] != msg_list[i + 1]['role'] for i in range(len(msg_list) - 1)
                )  # check if the roles are alternating
                and msg_list[-1]['role'] == 'user'  # check if the last role is user
        )
