# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

from openai.types import chat
from openai.types.chat import completion_create_params

ChatCompletion = chat.ChatCompletion
ChatCompletionChunk = chat.ChatCompletionChunk

CompletionCreateParams = chat.CompletionCreateParams
CompletionCreateParamsNonStreaming = completion_create_params.CompletionCreateParamsNonStreaming
CompletionCreateParamsStreaming = completion_create_params.CompletionCreateParamsStreaming
