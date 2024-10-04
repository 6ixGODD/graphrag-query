from typing import (
    Annotated,
    Any,
    Dict,
    Optional,
    Union,
)

import pydantic
import pydantic_settings


class ChatLLMConfig(pydantic.BaseModel):
    model: Annotated[str, pydantic.Field(..., env="CHAT_LLM_MODEL")]
    api_key: Annotated[str, pydantic.Field(..., env="CHAT_LLM_API_KEY")]
    base_url: Annotated[str, pydantic.Field(..., env="CHAT_LLM_BASE_URL")]

    # Optional fields
    organization: Annotated[Optional[str], pydantic.Field(..., env="CHAT_LLM_ORGANIZATION")]
    timeout: Annotated[Optional[float], pydantic.Field(..., env="CHAT_LLM_TIMEOUT")]
    max_retries: Annotated[Optional[int], pydantic.Field(..., env="CHAT_LLM_MAX_RETRIES")]
    kwargs: Annotated[Optional[Dict[str, Any]], pydantic.Field(..., env="CHAT_LLM_KWARGS")]


class EmbeddingConfig(pydantic.BaseModel):
    model: Annotated[str, pydantic.Field(..., env="EMBEDDING_MODEL")]
    api_key: Annotated[str, pydantic.Field(..., env="EMBEDDING_API_KEY")]
    base_url: Annotated[str, pydantic.Field(..., env="EMBEDDING_BASE_URL")]

    # Optional fields
    organization: Annotated[Optional[str], pydantic.Field(..., env="EMBEDDING_ORGANIZATION")]
    timeout: Annotated[Optional[float], pydantic.Field(..., env="EMBEDDING_TIMEOUT")]
    max_retries: Annotated[Optional[int], pydantic.Field(..., env="EMBEDDING_MAX_RETRIES")]
    max_tokens: Annotated[Optional[int], pydantic.Field(..., env="EMBEDDING_MAX_TOKENS")]
    token_encoder: Annotated[Optional[str], pydantic.Field(..., env="EMBEDDING_TOKEN_ENCODER")]
    kwargs: Annotated[Optional[Dict[str, Any]], pydantic.Field(..., env="EMBEDDING_KWARGS")]


class LoggingConfig(pydantic.BaseModel):
    enabled: Annotated[bool, pydantic.Field(..., env="LOGGING_ENABLED")]

    # Optional fields
    level: Annotated[Optional[str], pydantic.Field(..., env="LOGGING_LEVEL")]
    format: Annotated[Optional[str], pydantic.Field(..., env="LOGGING_FORMAT")]
    out_file: Annotated[Optional[str], pydantic.Field(..., env="LOGGING_OUT_FILE")]
    err_file: Annotated[Optional[str], pydantic.Field(..., env="LOGGING_ERR_FILE")]
    rotation: Annotated[Optional[str], pydantic.Field(..., env="LOGGING_ROTATION")]
    retention: Annotated[Optional[str], pydantic.Field(..., env="LOGGING_RETENTION")]
    serialize: Annotated[Optional[bool], pydantic.Field(..., env="LOGGING_SERIALIZE")]
    kwargs: Annotated[Optional[Dict[str, Any]], pydantic.Field(..., env="LOGGING_KWARGS")]


class ContextConfig(pydantic.BaseModel):
    directory: Annotated[str, pydantic.Field(..., env="CONTEXT_DIRECTORY")]

    # Optional fields
    kwargs: Annotated[Optional[Dict[str, Any]], pydantic.Field(..., env="CONTEXT_KWARGS")]


class LocalSearchConfig(pydantic.BaseModel):
    sys_prompt: Annotated[Optional[str], pydantic.Field(..., env="LOCAL_SEARCH_SYS_PROMPT")]
    community_level: Annotated[Optional[int], pydantic.Field(..., env="LOCAL_SEARCH_COMMUNITY_LEVEL")]
    store_coll_name: Annotated[Optional[str], pydantic.Field(..., env="LOCAL_SEARCH_STORE_COLL_NAME")]
    store_uri: Annotated[Optional[str], pydantic.Field(..., env="LOCAL_SEARCH_STORE_URI")]
    encoding_model: Annotated[Optional[str], pydantic.Field(..., env="LOCAL_SEARCH_ENCODING_MODEL")]
    kwargs: Annotated[Optional[Dict[str, Any]], pydantic.Field(..., env="LOCAL_SEARCH_KWARGS")]


class GlobalSearchConfig(pydantic.BaseModel):
    map_sys_prompt: Annotated[Optional[str], pydantic.Field(..., env="GLOBAL_SEARCH_MAP_SYS_PROMPT")]
    reduce_sys_prompt: Annotated[Optional[str], pydantic.Field(..., env="GLOBAL_SEARCH_REDUCE_SYS_PROMPT")]
    community_level: Annotated[Optional[int], pydantic.Field(..., env="GLOBAL_SEARCH_COMMUNITY_LEVEL")]
    allow_general_knowledge: Annotated[
        Optional[bool],
        pydantic.Field(..., env="GLOBAL_SEARCH_ALLOW_GENERAL_KNOWLEDGE")
    ]
    general_knowledge_sys_prompt: Annotated[
        Optional[str],
        pydantic.Field(..., env="GLOBAL_SEARCH_GENERAL_KNOWLEDGE_SYS_PROMPT")
    ]
    no_data_answer: Annotated[Optional[str], pydantic.Field(..., env="GLOBAL_SEARCH_NO_DATA_ANSWER")]
    json_mode: Annotated[Optional[bool], pydantic.Field(..., env="GLOBAL_SEARCH_JSON_MODE")]
    max_data_tokens: Annotated[Optional[int], pydantic.Field(..., env="GLOBAL_SEARCH_MAX_DATA_TOKENS")]
    encoding_model: Annotated[Optional[str], pydantic.Field(..., env="GLOBAL_SEARCH_ENCODING_MODEL")]
    kwargs: Annotated[Optional[Dict[str, Any]], pydantic.Field(..., env="GLOBAL_SEARCH_KWARGS")]


class Config(pydantic_settings.BaseSettings):
    chat_llm: ChatLLMConfig
    embedding: EmbeddingConfig
    logging: LoggingConfig
    context: ContextConfig
    query: Union[LocalSearchConfig, GlobalSearchConfig]
    # TODO: Config
