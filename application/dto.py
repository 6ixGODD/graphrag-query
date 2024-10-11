# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import typing

import pydantic
from openai.types import chat
from openai.types.chat import (
    chat_completion_assistant_message_param, chat_completion_system_message_param, chat_completion_user_message_param,
    completion_create_params, chat_completion_function_call_option_param
)

ChatCompletion = chat.ChatCompletion
ChatCompletionChunk = chat.ChatCompletionChunk

_CompletionCreateParams = chat.CompletionCreateParams
CompletionCreateParamsNonStreaming = completion_create_params.CompletionCreateParamsNonStreaming
CompletionCreateParamsStreaming = completion_create_params.CompletionCreateParamsStreaming


class CompletionCreateRequest(pydantic.BaseModel):
    messages: typing.Annotated[
        typing.List[
            typing.Union[
                chat_completion_system_message_param.ChatCompletionSystemMessageParam,
                chat_completion_user_message_param.ChatCompletionUserMessageParam,
                chat_completion_assistant_message_param.ChatCompletionAssistantMessageParam,
            ]
        ],
        pydantic.Field(...)
    ]
    model: typing.Annotated[str, pydantic.Field(..., min_length=1)]
    frequency_penalty: typing.Optional[float] = None
    function_call: [typing.Union[
        typing.Literal["none", "auto"],
        chat_completion_function_call_option_param.ChatCompletionFunctionCallOptionParam
    ]]
    functions: typing.Literal[None] = None
    logit_bias: typing.Literal[None] = None
    logprobs: typing.Literal[None] = None
    max_completion_tokens: typing.Literal[None] = None
    max_tokens: typing.Optional[int] = None
    metadata: typing.Literal[None] = None
    n: typing.Literal[None] = None
    parallel_tool_calls: typing.Literal[None] = None
    presence_penalty: typing.Literal[None] = None
    seed: typing.Literal[None] = None
    store: typing.Literal[None] = None


class ErrorResponse(pydantic.BaseModel):
    message: str
    code: typing.Optional[typing.Union[int, str]] = None
