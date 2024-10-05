# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License.

from __future__ import annotations

import os
import pathlib
import typing
import warnings

import pydantic
import pydantic_settings

__all__ = [
    'ChatLLMConfig',
    'EmbeddingConfig',
    'LoggingConfig',
    'ContextConfig',
    'LocalSearchConfig',
    'GlobalSearchConfig',
    'GraphRAGConfig',
]


class ChatLLMConfig(pydantic.BaseModel):
    model: typing.Annotated[str, pydantic.Field(..., env="CHAT_LLM_MODEL")]
    api_key: typing.Annotated[str, pydantic.Field(..., env="CHAT_LLM_API_KEY")]
    base_url: typing.Annotated[
        str,
        pydantic.Field(
            ...,
            env="CHAT_LLM_BASE_URL",
            pattern=r"https?://([a-zA-Z0-9\-.]+\.[a-zA-Z]{2,})(:[0-9]{1,5})?(/\s*)?"
        )
    ]

    # typing.Optional fields
    organization: typing.Annotated[
        typing.Optional[str], pydantic.Field(..., env="CHAT_LLM_ORGANIZATION")
    ] = None
    timeout: typing.Annotated[
        typing.Optional[float], pydantic.Field(..., env="CHAT_LLM_TIMEOUT", gt=0, lt=60)
    ] = None
    max_retries: typing.Annotated[
        typing.Optional[int], pydantic.Field(..., env="CHAT_LLM_MAX_RETRIES", ge=0, le=10)
    ] = None
    kwargs: typing.Annotated[
        typing.Optional[typing.Dict[str, typing.Any]], pydantic.Field(..., env="CHAT_LLM_KWARGS")
    ] = None


class EmbeddingConfig(pydantic.BaseModel):
    model: typing.Annotated[str, pydantic.Field(..., env="EMBEDDING_MODEL")]
    api_key: typing.Annotated[str, pydantic.Field(..., env="EMBEDDING_API_KEY")]
    base_url: typing.Annotated[
        str,
        pydantic.Field(
            ...,
            env="EMBEDDING_BASE_URL",
            pattern=r"https?://([a-zA-Z0-9\-.]+\.[a-zA-Z]{2,})(:[0-9]{1,5})?(/\s*)?"
        )
    ]

    # typing.Optional fields
    organization: typing.Annotated[
        typing.Optional[str], pydantic.Field(..., env="EMBEDDING_ORGANIZATION")
    ] = None
    timeout: typing.Annotated[
        typing.Optional[float], pydantic.Field(..., env="EMBEDDING_TIMEOUT", gt=0, lt=60)
    ] = None
    max_retries: typing.Annotated[
        typing.Optional[int], pydantic.Field(..., env="EMBEDDING_MAX_RETRIES", ge=0, le=10)
    ] = None
    max_tokens: typing.Annotated[
        typing.Optional[int], pydantic.Field(..., env="EMBEDDING_MAX_TOKENS", ge=1)
    ] = None
    token_encoder: typing.Annotated[
        typing.Optional[str], pydantic.Field(..., env="EMBEDDING_TOKEN_ENCODER", pattern=r"^[a-zA-Z0-9_]+$")
    ] = None
    kwargs: typing.Annotated[
        typing.Optional[typing.Dict[str, typing.Any]], pydantic.Field(..., env="EMBEDDING_KWARGS")
    ] = None


class LoggingConfig(pydantic.BaseModel):
    enabled: typing.Annotated[bool, pydantic.Field(..., env="LOGGING_ENABLED")]

    # typing.Optional fields
    level: typing.Annotated[
        typing.Optional[str],
        pydantic.Field(..., env="LOGGING_LEVEL", pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    ] = None
    format: typing.Annotated[
        typing.Optional[str], pydantic.Field(..., env="LOGGING_FORMAT", min_length=1)
    ] = None
    out_file: typing.Annotated[
        typing.Optional[str], pydantic.Field(..., env="LOGGING_OUT_FILE", min_length=1)
    ] = None
    err_file: typing.Annotated[
        typing.Optional[str], pydantic.Field(..., env="LOGGING_ERR_FILE", min_length=1)
    ] = None
    rotation: typing.Annotated[
        typing.Optional[str],
        pydantic.Field(..., env="LOGGING_ROTATION", pattern=r"^\d+ (second|minute|hour|day|week|month|year)s?$")
    ] = None
    retention: typing.Annotated[
        typing.Optional[str],
        pydantic.Field(..., env="LOGGING_RETENTION", pattern=r"^\d+ (second|minute|hour|day|week|month|year)s?$")
    ] = None
    serialize: typing.Annotated[
        typing.Optional[bool], pydantic.Field(..., env="LOGGING_SERIALIZE")
    ] = None
    kwargs: typing.Annotated[
        typing.Optional[typing.Dict[str, typing.Any]], pydantic.Field(..., env="LOGGING_KWARGS")
    ] = None


class ContextConfig(pydantic.BaseModel):
    directory: typing.Annotated[str, pydantic.Field(..., env="CONTEXT_DIRECTORY", min_length=1)]

    # typing.Optional fields
    kwargs: typing.Annotated[
        typing.Optional[typing.Dict[str, typing.Any]], pydantic.Field(..., env="CONTEXT_KWARGS")
    ] = None


class LocalSearchConfig(pydantic.BaseModel):
    sys_prompt: typing.Annotated[
        typing.Optional[str], pydantic.Field(..., env="LOCAL_SEARCH_SYS_PROMPT", min_length=1, repr=False)
    ] = None
    community_level: typing.Annotated[
        typing.Optional[int], pydantic.Field(..., env="LOCAL_SEARCH_COMMUNITY_LEVEL", ge=0)
    ] = None
    store_coll_name: typing.Annotated[
        typing.Optional[str], pydantic.Field(..., env="LOCAL_SEARCH_STORE_COLL_NAME", min_length=1)
    ] = None
    store_uri: typing.Annotated[
        typing.Optional[str],
        pydantic.Field(..., env="LOCAL_SEARCH_STORE_URI", min_length=1)
    ] = None
    encoding_model: typing.Annotated[
        typing.Optional[str], pydantic.Field(..., env="LOCAL_SEARCH_ENCODING_MODEL", min_length=1)
    ] = None
    kwargs: typing.Annotated[
        typing.Optional[typing.Dict[str, typing.Any]], pydantic.Field(..., env="LOCAL_SEARCH_KWARGS")
    ] = None


class GlobalSearchConfig(pydantic.BaseModel):
    map_sys_prompt: typing.Annotated[
        typing.Optional[str], pydantic.Field(..., env="GLOBAL_SEARCH_MAP_SYS_PROMPT", min_length=1, repr=False)
    ] = None
    reduce_sys_prompt: typing.Annotated[
        typing.Optional[str],
        pydantic.Field(..., env="GLOBAL_SEARCH_REDUCE_SYS_PROMPT", min_length=1, repr=False)
    ] = None
    community_level: typing.Annotated[
        typing.Optional[int], pydantic.Field(..., env="GLOBAL_SEARCH_COMMUNITY_LEVEL", ge=0)
    ] = None
    allow_general_knowledge: typing.Annotated[
        typing.Optional[bool],
        pydantic.Field(..., env="GLOBAL_SEARCH_ALLOW_GENERAL_KNOWLEDGE")
    ] = None
    general_knowledge_sys_prompt: typing.Annotated[
        typing.Optional[str],
        pydantic.Field(..., env="GLOBAL_SEARCH_GENERAL_KNOWLEDGE_SYS_PROMPT", min_length=1, repr=False)
    ] = None
    no_data_answer: typing.Annotated[
        typing.Optional[str], pydantic.Field(..., env="GLOBAL_SEARCH_NO_DATA_ANSWER", min_length=1)
    ] = None
    json_mode: typing.Annotated[
        typing.Optional[bool], pydantic.Field(..., env="GLOBAL_SEARCH_JSON_MODE")
    ] = None
    max_data_tokens: typing.Annotated[
        typing.Optional[int], pydantic.Field(..., env="GLOBAL_SEARCH_MAX_DATA_TOKENS", ge=1)
    ] = None
    encoding_model: typing.Annotated[
        typing.Optional[str], pydantic.Field(..., env="GLOBAL_SEARCH_ENCODING_MODEL", min_length=1)
    ] = None
    kwargs: typing.Annotated[
        typing.Optional[typing.Dict[str, typing.Any]], pydantic.Field(..., env="GLOBAL_SEARCH_KWARGS")
    ] = None


class GraphRAGConfig(pydantic_settings.BaseSettings):
    chat_llm: ChatLLMConfig
    embedding: EmbeddingConfig
    logging: LoggingConfig
    context: ContextConfig
    local_search: LocalSearchConfig
    global_search: GlobalSearchConfig

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix='GRAPHRAG_SERVER_',
        validate_default=False,
        env_nested_delimiter='__'
    )

    @classmethod
    def from_config_file(
        cls,
        config_file: typing.Union[str, os.PathLike[str], pathlib.Path],
        **kwargs: typing.Any,
    ) -> GraphRAGConfig:
        config_file_ = pathlib.Path(config_file)
        if not config_file_.exists():
            raise FileNotFoundError(f"Config file not found: {config_file_}")

        if config_file_.suffix not in ['.json', '.toml', '.yaml', '.yml']:
            raise ValueError(f"Unsupported config file format: {config_file_.suffix}")

        if config_file_.suffix == '.json':
            import json
            with open(config_file_, 'r') as f:
                config_dict = json.load(f)
        elif config_file_.suffix == '.toml':
            try:
                import toml
            except ImportError:
                raise ImportError("Please install the 'toml' package to read TOML files.")
            with open(config_file_, 'r') as f:
                config_dict = toml.load(f)
        else:
            try:
                import yaml
            except ImportError:
                raise ImportError("Please install the 'pyyaml' package to read YAML files.")
            with open(config_file_, 'r') as f:
                config_dict = yaml.safe_load(f)

        return cls(**config_dict, **kwargs)

    def __init__(self, **kwargs: typing.Any) -> None:
        # Ensure all fields are present
        for field in self.__fields__.keys():
            if field not in kwargs or not isinstance(kwargs[field], dict):
                warnings.warn(
                    f"Missing or invalid field: {field}, initializing to empty dict",
                    RuntimeWarning
                )
                kwargs[field] = {}
        super().__init__(**kwargs)
