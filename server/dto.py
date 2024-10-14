# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import typing

import pydantic
from openai.types import chat
from openai.types.chat import (
    chat_completion_assistant_message_param,
    chat_completion_stream_options_param,
    chat_completion_system_message_param,
    chat_completion_tool_choice_option_param,
    chat_completion_tool_param,
    chat_completion_user_message_param,
    completion_create_params,
)

ChatCompletion = chat.ChatCompletion
ChatCompletionChunk = chat.ChatCompletionChunk


class ChatCompletionMessage(pydantic.BaseModel):
    content: typing.Optional[str] = None
    refusal: typing.Optional[str] = None
    role: typing.Literal["assistant"]
    function_call: typing.Any = None
    tool_calls: typing.Any = None


class Choice(pydantic.BaseModel):
    finish_reason: typing.Optional[str] = None
    index: int
    logprobs: typing.Any = None
    message: ChatCompletionMessage


class ChunkChoice(pydantic.BaseModel):
    finish_reason: typing.Optional[str] = None
    index: int
    logprobs: typing.Any = None
    delta: ChatCompletionMessage


class ChatCompletionResponse(pydantic.BaseModel):
    id: str
    choices: typing.List[Choice]
    created: int
    model: str
    object: typing.Literal["chat.completion"]
    service_tier: typing.Optional[str] = None
    system_fingerprint: typing.Optional[str] = None
    usage: typing.Any = None


class ChatCompletionChunkResponse(pydantic.BaseModel):
    id: str
    choices: typing.List[ChunkChoice]
    created: int
    model: str
    object: typing.Literal["chat.completion.chunk"]
    service_tier: typing.Optional[str] = None
    system_fingerprint: typing.Optional[str] = None
    usage: typing.Any = None


class CompletionCreateRequest(pydantic.BaseModel):
    stream: bool = False
    messages: typing.Annotated[
        typing.List[typing.Union[
            chat_completion_system_message_param.ChatCompletionSystemMessageParam,
            chat_completion_user_message_param.ChatCompletionUserMessageParam,
            chat_completion_assistant_message_param.ChatCompletionAssistantMessageParam,
        ]], pydantic.Field(...)
    ]
    model: typing.Annotated[str, pydantic.Field(..., min_length=1)]
    frequency_penalty: typing.Optional[float] = None
    function_call: typing.Literal[None] = None
    functions: typing.Literal[None] = None
    logit_bias: typing.Optional[typing.Dict[str, int]] = None
    logprobs: typing.Optional[bool] = None
    max_completion_tokens: typing.Optional[int] = None
    max_tokens: typing.Optional[int] = None
    metadata: typing.Optional[typing.Dict[str, str]] = None
    n: typing.Optional[int] = None
    parallel_tool_calls: typing.Optional[bool] = None
    presence_penalty: typing.Optional[float] = None
    response_format: typing.Optional[completion_create_params.ResponseFormat] = None
    seed: typing.Optional[int] = None
    service_tier: typing.Optional[typing.Literal["auto", "default"]] = None
    stop: typing.Union[typing.Optional[str], typing.List[str]] = None
    store: typing.Optional[bool] = None
    stream_options: typing.Optional[chat_completion_stream_options_param.ChatCompletionStreamOptionsParam] = None
    temperature: typing.Optional[float] = None
    tool_choice: typing.Optional[chat_completion_tool_choice_option_param.ChatCompletionToolChoiceOptionParam] = None
    tools: typing.Optional[typing.Iterable[chat_completion_tool_param.ChatCompletionToolParam]] = None
    top_logprobs: typing.Optional[int] = None
    top_p: typing.Optional[float] = None
    user: typing.Optional[str] = None


class ErrorResponse(pydantic.BaseModel):
    message: str
    code: typing.Optional[typing.Union[int, str]] = None
