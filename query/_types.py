from __future__ import annotations

import pydantic


__all__ = [
    'Response',
    'ResponseVerbose',
    'ResponseChunk',
    'ResponseChunkVerbose',
]


class Response(pydantic.BaseModel):
    ...


class ResponseVerbose(pydantic.BaseModel):
    ...


class ResponseChunk(pydantic.BaseModel):
    ...


class ResponseChunkVerbose(pydantic.BaseModel):
    ...
