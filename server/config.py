# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import typing

import pydantic
import pydantic_settings


class Config(pydantic_settings.BaseSettings):
    # Application Configurations
    app_name: typing.Annotated[
        str,
        pydantic.Field(..., min_length=1, max_length=50)
    ] = "GraphRAG OpenAI API Server"
    app_version: typing.Annotated[
        str,
        pydantic.Field(..., pattern=r"^\d+\.\d+\.\d+([ab]\d*)?$")
    ] = "1.0.0"
    app_route_prefix: typing.Annotated[
        str,
        pydantic.Field(..., pattern=r"^[a-z0-9_/]+$")
    ] = f"/api/v{app_version.split('.')[0]}"

    # Logging Configurations
    log_level: typing.Annotated[
        str,
        pydantic.Field(..., pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    ] = "INFO"
    log_out_file: typing.Annotated[
        str,
        pydantic.Field(..., min_length=1, max_length=50)
    ] = "out.json"
    log_err_file: typing.Annotated[
        str,
        pydantic.Field(..., min_length=1, max_length=50)
    ] = "err.json"
    log_rotation: typing.Annotated[
        str,
        pydantic.Field(..., pattern=r"^\d+ (second|minute|hour|day|week|month|year)s?$")
    ] = "1 week"
    log_retention: typing.Annotated[
        str,
        pydantic.Field(..., pattern=r"^\d+ (second|minute|hour|day|week|month|year)s?$")
    ] = "1 month"

    # Authentication Configurations
    api_keys: typing.Annotated[
        typing.List[str],
        pydantic.Field(..., min_items=1, repr=False)
    ] = []

    # GraphRAG Configurations
    graphrag_config_file: typing.Annotated[
        typing.Optional[str],
        pydantic.Field(
            ...,
            min_length=1, max_length=50, pattern=r".*\.(json|yaml|toml|yml)"
        )
    ] = None

    # Model Configurations
    model_config = pydantic_settings.SettingsConfigDict(
        env_prefix="GRAPH_RAG_OPENAI__",
        validate_default=False,
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


_config = Config()  # singleton instance


def get_config() -> Config:
    return _config
