# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import fastapi

from . import dto

_root = fastapi.APIRouter()


@_root.post('chat/completions')
async def chat_completions(request: dto.CompletionCreateRequest):
    ...
