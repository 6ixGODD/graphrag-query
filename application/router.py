import typing

import fastapi
import pydantic

_root = fastapi.APIRouter()
_Response_T: typing.TypeAlias = typing.TypeVar('_Response_T', bound=pydantic.BaseModel)
_StreamResponse_T: typing.TypeAlias = typing.TypeVar('_StreamResponse_T', bound=pydantic.BaseModel)
@_root.post('chat/completions')
async def chat_completions() -> typing.Union[pydantic]:
    pass


