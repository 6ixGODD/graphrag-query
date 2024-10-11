# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import typing

import pydantic
from openai.types import chat
from openai.types.chat import completion_create_params

ChatCompletion = chat.ChatCompletion
ChatCompletionChunk = chat.ChatCompletionChunk

_CompletionCreateParams = chat.CompletionCreateParams
CompletionCreateParamsNonStreaming = completion_create_params.CompletionCreateParamsNonStreaming
CompletionCreateParamsStreaming = completion_create_params.CompletionCreateParamsStreaming


class CompletionCreateRequest(pydantic.BaseModel):
    model: typing.Annotated[str, pydantic.Field(..., min_length=1)]
    messages: typing.List[typing.Union[typing.Dict[str, typing.Any], str]]
    store: typing.Literal[None] = None
    frequency_penalty: typing.Literal[None] = None


class ErrorResponse(pydantic.BaseModel):
    message: str
    code: typing.Optional[typing.Union[int, str]] = None
