# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

from __future__ import annotations

import typing

import fastapi
import openai

import graphrag_query
from server import dto
from server.common import const, context, errors, graphrag, utils

_root = fastapi.APIRouter()


async def _parse_stream_response(response: graphrag_query.types.AsyncStreamResponse_T) -> typing.AsyncIterator[str]:
    id_ = utils.gen_id(const.Constants.CHAT_ID_PREFIX)
    async for chunk in response:
        chunk = typing.cast(graphrag_query.SearchResultChunk, chunk)
        data = dto.ChatCompletionChunkResponse(
            id=id_,
            choices=[dto.ChunkChoice(
                finish_reason=chunk.choice.finish_reason,
                index=0,
                delta=dto.ChatCompletionMessage(
                    content=chunk.choice.delta.content,
                    refusal=chunk.choice.delta.refusal,
                    role='assistant',
                    function_call=None,
                    tool_calls=None
                ),
            )],
            created=chunk.created,
            model=chunk.model,
            object='chat.completion.chunk',
            system_fingerprint=chunk.system_fingerprint,
            usage=chunk.usage,
        ).model_dump_json(exclude_none=True).__str__()
        yield f'data: {data}\n\n'

    yield 'data: [DONE]\n\n'


@_root.post('/chat/completions')
async def chat_completions(request: dto.CompletionCreateRequest):
    logger = context.get_logger_with_context(tag=const.Constants.ROUTER_LOGGING_TAG)
    with logger.catch(reraise=True, message="Failed to execute chat completions", exclude=errors.BaseAppError):
        client = graphrag.get_client(logger)
        response = await client.chat(
            engine='local',
            message=request.messages,
            stream=request.stream,
            verbose=False,
            frequency_penalty=request.frequency_penalty or openai.NOT_GIVEN,
            function_call=request.function_call or openai.NOT_GIVEN,
            functions=request.functions or openai.NOT_GIVEN,
            logit_bias=request.logit_bias or openai.NOT_GIVEN,
            logprobs=request.logprobs or openai.NOT_GIVEN,
            max_completion_tokens=request.max_completion_tokens or openai.NOT_GIVEN,
            max_tokens=request.max_tokens or openai.NOT_GIVEN,
            metadata=request.metadata or openai.NOT_GIVEN,
            n=request.n or openai.NOT_GIVEN,
            parallel_tool_calls=request.parallel_tool_calls or openai.NOT_GIVEN,
            presence_penalty=request.presence_penalty or openai.NOT_GIVEN,
            response_format=request.response_format or openai.NOT_GIVEN,
            seed=request.seed or openai.NOT_GIVEN,
            service_tier=request.service_tier or openai.NOT_GIVEN,
            stop=request.stop or openai.NOT_GIVEN,
            store=request.store or openai.NOT_GIVEN,
            stream_options=request.stream_options or openai.NOT_GIVEN,
            temperature=request.temperature or openai.NOT_GIVEN,
            tool_choice=request.tool_choice or openai.NOT_GIVEN,
            tools=request.tools or openai.NOT_GIVEN,
            top_logprobs=request.top_logprobs or openai.NOT_GIVEN,
            top_p=request.top_p or openai.NOT_GIVEN,
            user=request.user or openai.NOT_GIVEN
        )
        if request.stream:
            return fastapi.responses.StreamingResponse(
                _parse_stream_response(response),
                media_type='text/event-stream; charset=utf-8'
            )
        else:
            return fastapi.responses.JSONResponse(
                dto.ChatCompletionResponse(
                    id=utils.gen_id(const.Constants.CHAT_ID_PREFIX),
                    choices=[dto.Choice(
                        finish_reason=response.choice.finish_reason,
                        index=0,
                        message=dto.ChatCompletionMessage(
                            content=response.choice.message.content,
                            refusal=response.choice.message.refusal,
                            role='assistant',
                        ),
                    )],
                    created=response.created,
                    model=response.model,
                    object='chat.completion',
                    system_fingerprint=response.system_fingerprint,
                    usage=response.usage,
                ).model_dump_json(exclude_none=True)
            )


def init_router(app: fastapi.FastAPI, prefix: str = '') -> None:
    app.include_router(_root, prefix=prefix)
