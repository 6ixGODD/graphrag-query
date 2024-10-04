from __future__ import annotations

import pydantic


class Response(pydantic.BaseModel):
    ...


class ResponseVerbose(pydantic.BaseModel):
    ...


class ResponseChunk(pydantic.BaseModel):
    ...


class ResponseChunkVerbose(pydantic.BaseModel):
    ...
