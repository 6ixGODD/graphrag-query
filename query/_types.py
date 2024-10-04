import pydantic


class Response(pydantic.BaseModel):
    ...


class ResponseVerbose(pydantic.BaseModel):
    ...


class ResponseChunk(pydantic.BaseModel):
    ...


class ResponseChunkVerbose(pydantic.BaseModel):
    ...
