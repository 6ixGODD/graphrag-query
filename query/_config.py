from __future__ import annotations

from typing import (
    Annotated,
    Any,
    Dict,
    Optional,
    Union,
)

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
    model: Annotated[str, pydantic.Field(..., env="CHAT_LLM_MODEL")]
    api_key: Annotated[str, pydantic.Field(..., env="CHAT_LLM_API_KEY")]
    base_url: Annotated[
        str,
        pydantic.Field(
            ...,
            env="CHAT_LLM_BASE_URL",
            pattern=r"https?://([a-zA-Z0-9\-.]+\.[a-zA-Z]{2,})(:[0-9]{1,5})?(/\s*)?"
        )
    ]

    # Optional fields
    organization: Annotated[Optional[str], pydantic.Field(..., env="CHAT_LLM_ORGANIZATION")]
    timeout: Annotated[Optional[float], pydantic.Field(..., env="CHAT_LLM_TIMEOUT", gt=0, lt=60)]
    max_retries: Annotated[Optional[int], pydantic.Field(..., env="CHAT_LLM_MAX_RETRIES", ge=0, le=10)]
    kwargs: Annotated[Optional[Dict[str, Any]], pydantic.Field(..., env="CHAT_LLM_KWARGS")]


class EmbeddingConfig(pydantic.BaseModel):
    model: Annotated[str, pydantic.Field(..., env="EMBEDDING_MODEL")]
    api_key: Annotated[str, pydantic.Field(..., env="EMBEDDING_API_KEY")]
    base_url: Annotated[
        str,
        pydantic.Field(
            ...,
            env="EMBEDDING_BASE_URL",
            pattern=r"https?://([a-zA-Z0-9\-.]+\.[a-zA-Z]{2,})(:[0-9]{1,5})?(/\s*)?"
        )
    ]

    # Optional fields
    organization: Annotated[Optional[str], pydantic.Field(..., env="EMBEDDING_ORGANIZATION")]
    timeout: Annotated[Optional[float], pydantic.Field(..., env="EMBEDDING_TIMEOUT", gt=0, lt=60)]
    max_retries: Annotated[Optional[int], pydantic.Field(..., env="EMBEDDING_MAX_RETRIES", ge=0, le=10)]
    max_tokens: Annotated[Optional[int], pydantic.Field(..., env="EMBEDDING_MAX_TOKENS", ge=1)]
    token_encoder: Annotated[
        Optional[str], pydantic.Field(..., env="EMBEDDING_TOKEN_ENCODER", regex=r"^[a-zA-Z0-9_]+$")
    ]
    kwargs: Annotated[Optional[Dict[str, Any]], pydantic.Field(..., env="EMBEDDING_KWARGS")]


class LoggingConfig(pydantic.BaseModel):
    enabled: Annotated[bool, pydantic.Field(..., env="LOGGING_ENABLED")]

    # Optional fields
    level: Annotated[
        Optional[str], pydantic.Field(..., env="LOGGING_LEVEL", pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    ]
    format: Annotated[Optional[str], pydantic.Field(..., env="LOGGING_FORMAT", min_length=1, max_length=50)]
    out_file: Annotated[Optional[str], pydantic.Field(..., env="LOGGING_OUT_FILE", min_length=1, max_length=50)]
    err_file: Annotated[Optional[str], pydantic.Field(..., env="LOGGING_ERR_FILE", min_length=1, max_length=50)]
    rotation: Annotated[
        Optional[str],
        pydantic.Field(
            ...,
            env="LOGGING_ROTATION",
            pattern=r"^\d+ (second|minute|hour|day|week|month|year)s?$"
        )
    ]
    retention: Annotated[
        Optional[str],
        pydantic.Field(
            ...,
            env="LOGGING_RETENTION",
            pattern=r"^\d+ (second|minute|hour|day|week|month|year)s?$"
        )
    ]
    serialize: Annotated[Optional[bool], pydantic.Field(..., env="LOGGING_SERIALIZE")]
    kwargs: Annotated[Optional[Dict[str, Any]], pydantic.Field(..., env="LOGGING_KWARGS")]


class ContextConfig(pydantic.BaseModel):
    directory: Annotated[str, pydantic.Field(..., env="CONTEXT_DIRECTORY", min_length=1, max_length=50)]

    # Optional fields
    kwargs: Annotated[Optional[Dict[str, Any]], pydantic.Field(..., env="CONTEXT_KWARGS")]


class LocalSearchConfig(pydantic.BaseModel):
    sys_prompt: Annotated[Optional[str], pydantic.Field(..., env="LOCAL_SEARCH_SYS_PROMPT", min_length=1)]
    community_level: Annotated[Optional[int], pydantic.Field(..., env="LOCAL_SEARCH_COMMUNITY_LEVEL", ge=0)]
    store_coll_name: Annotated[Optional[str], pydantic.Field(..., env="LOCAL_SEARCH_STORE_COLL_NAME", min_length=1)]
    store_uri: Annotated[
        Optional[str],
        pydantic.Field(
            ...,
            env="LOCAL_SEARCH_STORE_URI",
            min_length=1,
            max_length=50
        )
    ]
    encoding_model: Annotated[Optional[str], pydantic.Field(..., env="LOCAL_SEARCH_ENCODING_MODEL", min_length=1)]
    kwargs: Annotated[Optional[Dict[str, Any]], pydantic.Field(..., env="LOCAL_SEARCH_KWARGS")]


class GlobalSearchConfig(pydantic.BaseModel):
    map_sys_prompt: Annotated[Optional[str], pydantic.Field(..., env="GLOBAL_SEARCH_MAP_SYS_PROMPT", min_length=1)]
    reduce_sys_prompt: Annotated[
        Optional[str],
        pydantic.Field(..., env="GLOBAL_SEARCH_REDUCE_SYS_PROMPT", min_length=1)
    ]
    community_level: Annotated[Optional[int], pydantic.Field(..., env="GLOBAL_SEARCH_COMMUNITY_LEVEL", ge=0)]
    allow_general_knowledge: Annotated[
        Optional[bool],
        pydantic.Field(..., env="GLOBAL_SEARCH_ALLOW_GENERAL_KNOWLEDGE")
    ]
    general_knowledge_sys_prompt: Annotated[
        Optional[str],
        pydantic.Field(..., env="GLOBAL_SEARCH_GENERAL_KNOWLEDGE_SYS_PROMPT", min_length=1)
    ]
    no_data_answer: Annotated[Optional[str], pydantic.Field(..., env="GLOBAL_SEARCH_NO_DATA_ANSWER", min_length=1)]
    json_mode: Annotated[Optional[bool], pydantic.Field(..., env="GLOBAL_SEARCH_JSON_MODE")]
    max_data_tokens: Annotated[Optional[int], pydantic.Field(..., env="GLOBAL_SEARCH_MAX_DATA_TOKENS", ge=1)]
    encoding_model: Annotated[Optional[str], pydantic.Field(..., env="GLOBAL_SEARCH_ENCODING_MODEL", min_length=1)]
    kwargs: Annotated[Optional[Dict[str, Any]], pydantic.Field(..., env="GLOBAL_SEARCH_KWARGS")]


class GraphRAGConfig(pydantic_settings.BaseSettings):
    chat_llm: ChatLLMConfig
    embedding: EmbeddingConfig
    logging: LoggingConfig
    context: ContextConfig
    query: Union[LocalSearchConfig, GlobalSearchConfig]

    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix='GRAPHRAG_SERVER_', validate_default=False, env_nested_delimiter='__'
    )
