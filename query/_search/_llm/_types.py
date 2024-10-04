from typing import (
    AsyncGenerator,
    Generator,
    Iterable,
    List,
    TypeAlias,
)

from openai.types import chat

ChatCompletionMessageParam = chat.ChatCompletionMessageParam
ChatCompletion = chat.ChatCompletion
ChatCompletionChunk = chat.ChatCompletionChunk

MessageParam_T: TypeAlias = Iterable[ChatCompletionMessageParam]
ChatResponse_T: TypeAlias = ChatCompletion
SyncChatStreamResponse_T: TypeAlias = Generator[ChatCompletionChunk, None, None]
AsyncChatStreamResponse_T: TypeAlias = AsyncGenerator[ChatCompletionChunk, None]

EmbeddingResponse_T: TypeAlias = List[float]
