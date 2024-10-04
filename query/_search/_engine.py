import asyncio
import time
import warnings
from collections import defaultdict
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Union,
)

import tiktoken

from .. import _utils
from .._search import (
    _base,
    _context,
    _defaults,
    _llm,
    _types,
)


class LocalSearchEngine(_base.QueryEngine):
    _chat_llm: _llm.BaseChatLLM
    _embedding: _llm.BaseEmbedding
    _context_builder: _context.LocalContextBuilder
    _logger: Optional[_base.Logger]
    _sys_prompt: str

    def __init__(
        self,
        *,
        chat_llm: _llm.BaseChatLLM,
        embedding: _llm.BaseEmbedding,
        context_loader: _context.LocalContextLoader,

        sys_prompt: Optional[str] = None,
        community_level: Optional[int] = None,
        store_coll_name: Optional[str] = None,
        store_uri: Optional[str] = None,
        encoding_model: Optional[str] = None,

        logger: Optional[_base.Logger] = None,

        **kwargs: Any,
    ) -> None:
        super().__init__(
            chat_llm=chat_llm,
            embedding=embedding,
            context_builder=context_loader.to_context_builder(
                embedder=embedding,
                community_level=community_level or _defaults.DEFAULT__LOCAL_SEARCH__COMMUNITY_LEVEL,
                store_coll_name=store_coll_name or _defaults.DEFAULT__VECTOR_STORE__COLLECTION_NAME,
                store_uri=store_uri or _defaults.DEFAULT__VECTOR_STORE__URI,
                encoding_model=encoding_model or _defaults.DEFAULT__ENCODING_MODEL,
                **kwargs,
            ),
            logger=logger,
        )
        self._sys_prompt = sys_prompt or _defaults.LOCAL_SEARCH__SYS_PROMPT
        if '{context_data}' not in self._sys_prompt:
            warnings.warn('Local Search\'s System Prompt does not contain "{context_data}"', RuntimeWarning)

    def search(
        self,
        query: str,
        *,
        conversation_history: _types.ConversationHistory_T = None,
        verbose: bool = False,
        stream: bool = False,
        **kwargs: Any,
    ) -> Union[_types.SearchResult_T, _types.StreamSearchResult_T]:
        created = time.time()
        self._logger.info(f"Starting search for query: {query} at {created}") if self._logger else None
        if conversation_history is None:
            conversation_history = _context.ConversationHistory()
        elif isinstance(conversation_history, list):
            conversation_history = _context.ConversationHistory.from_list(conversation_history)

        context_text, context_records = self._context_builder.build_context(
            query=query,
            conversation_history=conversation_history,
            **kwargs,
        )
        prompt = self._sys_prompt.format_map(defaultdict(str, context_data=context_text))
        messages = ([{"role": "system", "content": prompt}] +
                    conversation_history.to_dict() +
                    [{"role": "user", "content": query}])
        self._logger.info(f"Constructed messages: {messages}") if self._logger else None

        result = self._chat_llm.chat(msg=cast(_llm.MessageParam_T, messages), stream=stream, **kwargs)
        self._logger.info(f"Received result: {result}") if self._logger else None

        if stream:
            result = cast(_llm.SyncChatStreamResponse_T, result)
            return self._parse_stream_result(
                result,
                verbose=verbose,
                created=created,
                context_data=context_records,
                context_text=context_text
            )
        else:
            result = cast(_llm.ChatResponse_T, result)
            return self._parse_result(
                result,
                verbose=verbose,
                created=created,
                context_data=context_records,
                context_text=context_text
            )


class AsyncLocalSearchEngine(_base.AsyncQueryEngine):
    _chat_llm: _llm.BaseAsyncChatLLM
    _embedding: _llm.BaseEmbedding
    _context_builder: _context.LocalContextBuilder
    _sys_prompt: str

    def __init__(
        self,
        *,
        chat_llm: _llm.BaseAsyncChatLLM,
        embedding: _llm.BaseEmbedding,
        context_loader: _context.LocalContextLoader,

        sys_prompt: Optional[str] = None,
        community_level: Optional[int] = None,
        store_coll_name: Optional[str] = None,
        store_uri: Optional[str] = None,
        encoding_model: Optional[str] = None,

        logger: Optional[_base.Logger] = None,

        **kwargs: Any,
    ) -> None:
        super().__init__(
            chat_llm=chat_llm,
            embedding=embedding,
            context_builder=context_loader.to_context_builder(
                community_level=community_level or _defaults.DEFAULT__LOCAL_SEARCH__COMMUNITY_LEVEL,
                embedder=embedding,
                store_coll_name=store_coll_name or _defaults.DEFAULT__VECTOR_STORE__COLLECTION_NAME,
                store_uri=store_uri or _defaults.DEFAULT__VECTOR_STORE__URI,
                encoding_model=encoding_model or _defaults.DEFAULT__ENCODING_MODEL,
                **kwargs,
            ),
            logger=logger,
        )
        self._sys_prompt = sys_prompt or _defaults.LOCAL_SEARCH__SYS_PROMPT
        if '{context_data}' not in self._sys_prompt:
            warnings.warn('Local Search\'s System Prompt does not contain "{context_data}"', RuntimeWarning)

    async def asearch(
        self,
        query: str,
        *,
        conversation_history: _types.ConversationHistory_T,
        verbose: bool = False,
        stream: bool = False,
        **kwargs: Any,
    ) -> Union[_types.SearchResult_T, _types.AsyncStreamSearchResult_T]:
        created = time.time()

        # Convert conversation_history to ConversationHistory object
        if conversation_history is None:
            conversation_history = _context.ConversationHistory()
        elif isinstance(conversation_history, list):
            conversation_history = _context.ConversationHistory.from_list(conversation_history)

        context_text, context_records = self._context_builder.build_context(
            query=query,
            conversation_history=conversation_history,
            **kwargs,
        )
        prompt = self._sys_prompt.format_map(defaultdict(str, context_data=context_text))
        messages = ([{"role": "system", "content": prompt}] +
                    conversation_history.to_dict() +
                    [{"role": "user", "content": query}])

        result = await self._chat_llm.achat(msg=cast(_llm.MessageParam_T, messages), stream=stream, **kwargs)

        if stream:
            result = cast(_llm.AsyncChatStreamResponse_T, result)
            return self._parse_stream_result(
                result,
                verbose=verbose,
                created=created,
                context_data=context_records,
                context_text=context_text
            )
        else:
            result = cast(_llm.ChatResponse_T, result)
            return self._parse_result(
                result,
                verbose=verbose,
                created=created,
                context_data=context_records,
                context_text=context_text
            )


class GlobalSearchEngine(_base.QueryEngine):
    _chat_llm: _llm.BaseChatLLM
    _embedding: _llm.BaseEmbedding
    _context_builder: _context.GlobalContextBuilder
    _sys_prompt: str

    def __init__(
        self,
        *,
        chat_llm: _llm.BaseChatLLM,
        embedding: _llm.BaseEmbedding,
        context_loader: _context.GlobalContextLoader,

        community_level: Optional[int] = None,
        map_sys_prompt: Optional[str] = None,
        reduce_sys_prompt: Optional[str] = None,
        allow_general_knowledge: bool = True,
        general_knowledge_sys_prompt: Optional[str] = None,
        no_data_answer: Optional[str] = None,
        json_mode: bool = True,
        max_data_tokens: int = 8000,
        encoding_model: Optional[str] = None,

        logger: Optional[_base.Logger] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            chat_llm=chat_llm,
            embedding=embedding,
            context_builder=context_loader.to_context_builder(
                community_level=community_level or _defaults.DEFAULT__GLOBAL_SEARCH__COMMUNITY_LEVEL,
                encoding_model=encoding_model or _defaults.DEFAULT__ENCODING_MODEL,
                **kwargs,
            ),
        )
        self._token_encoder = tiktoken.get_encoding(encoding_model or _defaults.DEFAULT__ENCODING_MODEL)
        self._map_sys_prompt = map_sys_prompt or _defaults.GLOBAL_SEARCH__MAP__SYS_PROMPT
        if '{context_data}' not in self._map_sys_prompt:
            warnings.warn('Global Search\'s Map System Prompt does not contain "{context_data}"', RuntimeWarning)
        self._reduce_sys_prompt = reduce_sys_prompt or _defaults.GLOBAL_SEARCH__REDUCE__SYS_PROMPT
        if '{report_data}' not in self._reduce_sys_prompt:
            warnings.warn('Global Search\'s Reduce System Prompt does not contain "{report_data}"', RuntimeWarning)
        self._allow_general_knowledge = allow_general_knowledge
        self._general_knowledge_sys_prompt = (general_knowledge_sys_prompt or
                                              _defaults.GLOBAL_SEARCH__REDUCE__GENERAL_KNOWLEDGE_INSTRUCTION)
        self._no_data_answer = no_data_answer or _defaults.GLOBAL_SEARCH__REDUCE__NO_DATA_ANSWER
        self._json_mode = json_mode
        self._data_max_tokens = max_data_tokens or _defaults.DEFAULT__GLOBAL_SEARCH__DATA_MAX_TOKENS
        self._logger = logger

    def search(
        self,
        query: str,
        *,
        conversation_history: _types.ConversationHistory_T = None,
        verbose: bool = False,
        stream: bool = False,
        **kwargs: Any,
    ) -> Union[_types.SearchResult_T, _types.StreamSearchResult_T]:
        created = time.time()
        self._logger.info(f"Starting search for query: {query} at {created}") if self._logger else None
        if conversation_history is None:
            conversation_history = _context.ConversationHistory()
        elif isinstance(conversation_history, list):
            conversation_history = _context.ConversationHistory.from_list(conversation_history)

        context_chunks, context_records = self._context_builder.build_context(
            conversation_history=conversation_history,
            **kwargs,
        )
        map_result = [self._map(query, context, verbose, **kwargs) for context in context_chunks]
        return self._reduce(map_result, query, verbose, stream, **kwargs)

    def _map(
        self,
        query: str,
        context: str,
        verbose: bool,
        **kwargs: Any
    ) -> _types.SearchResult_T:
        created = time.time()
        prompt = self._map_sys_prompt.format_map(defaultdict(str, context_data=context, query=query))
        msg = [{"role": "system", "content": prompt}, {"role": "user", "content": query}]
        response = cast(
            _llm.ChatResponse_T, self._chat_llm.chat(
                msg=cast(_llm.MessageParam_T, msg),
                stream=False,
                **_utils.filter_kwargs(self._chat_llm.chat, kwargs, prefix='map__')
            )
        )
        result = self._parse_map(response)

        usage = _types.Usage(
            completion_tokens=response.usage.completion_tokens,
            prompt_tokens=response.usage.prompt_tokens,
            total_tokens=response.usage.total_tokens,
        ) if response.usage else None

        if verbose:
            return _types.SearchResultVerbose(
                created=created.__int__(),
                model=self._chat_llm.model,
                system_fingerprint=response.system_fingerprint,
                choice=_types.Choice(
                    finish_reason=response.choices[0].finish_reason,
                    message=_types.Message(
                        content=result,
                        refusal=response.choices[0].message.refusal,
                    ),
                ),
                usage=usage,
                context_data=None,
                context_text=context,
                completion_time=time.time() - created,
                llm_calls=1,
            )
        else:
            return _types.SearchResult(
                created=created.__int__(),
                model=self._chat_llm.model,
                system_fingerprint=response.system_fingerprint,
                choice=_types.Choice(
                    finish_reason=response.choices[0].finish_reason,
                    message=_types.Message(
                        content=result,
                        refusal=response.choices[0].message.refusal,
                    ),
                ),
                usage=usage,
            )

    @staticmethod
    def _parse_map(response: _llm.ChatResponse_T) -> List[Dict[str, Any]]:
        default = [{"answer": "", "score": 0}]
        json_ = _utils.deserialize_json(response.choices[0].message.content or "")
        if json_ == {}:
            return default

        points = json_.get("points", [])
        if not isinstance(points, list):
            return default

        return [
            {"answer": point["description"], "score": int(point["score"])}
            for point in points
            if isinstance(point, dict) and "description" in point and "score" in point
        ]

    def _reduce(
        self,
        map_results: List[_types.SearchResult_T],
        query: str,
        verbose: bool,
        stream: bool,
        **kwargs: Any
    ) -> Union[_types.SearchResult_T, _types.StreamSearchResult_T]:
        created = time.time()
        key_points: List[Dict[str, Any]] = []
        for idx, map_ in enumerate(map_results):
            if not isinstance(map_.choice.message.content, list):
                continue
            for ele in map_.choice.message.content:
                if not isinstance(ele, dict) or "answer" not in ele or "score" not in ele:
                    continue
                key_points.append(
                    {
                        "analyst": idx,
                        "answer":  ele["answer"],
                        "score":   ele["score"]
                    }
                )

        key_points = [kp for kp in key_points if isinstance(kp["score"], (int, float)) and kp["score"] > 0]

        if not key_points.__len__() and not self._allow_general_knowledge:
            warnings.warn("No key points found from the map phase", RuntimeWarning)
            return _types.SearchResult(
                created=created.__int__(),
                model=self._chat_llm.model,
                choice=_types.Choice(
                    finish_reason="stop",
                    message=_types.Message(
                        content=self._no_data_answer,
                    ),
                ),
                usage=None,
            ) if not verbose else _types.SearchResultVerbose(
                created=created.__int__(),
                model=self._chat_llm.model,
                choice=_types.Choice(
                    finish_reason="stop",
                    message=_types.Message(
                        content=self._no_data_answer,
                    ),
                ),
                completion_time=time.time() - created,
                llm_calls=0,
            )

        key_points = sorted(
            key_points,
            key=lambda kp: kp["score"] if isinstance(kp["score"], (int, float)) else 0,
            reverse=True
        )

        data: List[str] = []
        total_tokens = 0
        for kp in key_points:
            formatted_response = '\n'.join(
                [f'----Analyst {kp["analyst"] + 1}----', f'Importance score: {kp["score"]}', kp["answer"]]
            )
            total_tokens += _utils.num_tokens(formatted_response, self._token_encoder)
            if total_tokens > self._data_max_tokens:
                warnings.warn("Data exceeds maximum token limit", RuntimeWarning)
                break
            data.append(formatted_response)

        report_data = '\n\n'.join(data)
        prompt = self._reduce_sys_prompt.format_map(defaultdict(str, report_data=report_data))
        if self._allow_general_knowledge:
            prompt += f'\n{self._general_knowledge_sys_prompt}'
        msg = [{"role": "system", "content": prompt}, {"role": "user", "content": query}]
        result = self._chat_llm.chat(
            msg=cast(_llm.MessageParam_T, msg),
            stream=stream,
            **_utils.filter_kwargs(self._chat_llm.chat, kwargs, prefix='reduce__')
        )

        if stream:
            result = cast(_llm.SyncChatStreamResponse_T, result)
            return self._parse_stream_result(
                result,
                verbose=verbose,
                created=created,
                context_data=None,
                context_text=report_data,
                map_result=map_results,
                reduce_context_data=None,
                reduce_context_text=report_data,
            )
        else:
            result = cast(_llm.ChatResponse_T, result)
            return self._parse_result(
                result,
                verbose=verbose,
                created=created,
                context_data=None,
                context_text=report_data,
                map_result=map_results,
                reduce_context_data=None,
                reduce_context_text=report_data,
            )


class AsyncGlobalSearchEngine(_base.AsyncQueryEngine):
    _chat_llm: _llm.BaseAsyncChatLLM
    _embedding: _llm.BaseEmbedding
    _context_builder: _context.GlobalContextBuilder
    _sys_prompt: str

    def __init__(
        self,
        *,
        chat_llm: _llm.BaseAsyncChatLLM,
        embedding: _llm.BaseEmbedding,
        context_loader: _context.GlobalContextLoader,

        community_level: Optional[int] = None,
        map_sys_prompt: Optional[str] = None,
        reduce_sys_prompt: Optional[str] = None,
        allow_general_knowledge: bool = True,
        general_knowledge_sys_prompt: Optional[str] = None,
        no_data_answer: Optional[str] = None,
        json_mode: bool = True,
        max_data_tokens: int = 8000,
        encoding_model: Optional[str] = None,
        concurrent_coroutines: int = 16,

        logger: Optional[_base.Logger] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            chat_llm=chat_llm,
            embedding=embedding,
            context_builder=context_loader.to_context_builder(
                community_level=community_level or _defaults.DEFAULT__GLOBAL_SEARCH__COMMUNITY_LEVEL,
                encoding_model=encoding_model or _defaults.DEFAULT__ENCODING_MODEL,
                **kwargs,
            ),
        )
        self._map_sys_prompt = map_sys_prompt or _defaults.GLOBAL_SEARCH__MAP__SYS_PROMPT
        self._reduce_sys_prompt = reduce_sys_prompt or _defaults.GLOBAL_SEARCH__REDUCE__SYS_PROMPT
        self._allow_general_knowledge = allow_general_knowledge
        self._general_knowledge_sys_prompt = (general_knowledge_sys_prompt or
                                              _defaults.GLOBAL_SEARCH__REDUCE__GENERAL_KNOWLEDGE_INSTRUCTION)
        self._no_data_answer = no_data_answer or _defaults.GLOBAL_SEARCH__REDUCE__NO_DATA_ANSWER
        self._json_mode = json_mode
        self._data_max_tokens = max_data_tokens or _defaults.DEFAULT__GLOBAL_SEARCH__DATA_MAX_TOKENS
        self._token_encoder = tiktoken.get_encoding(encoding_model or _defaults.DEFAULT__ENCODING_MODEL)
        self._logger = logger
        self._semaphore = asyncio.Semaphore(concurrent_coroutines)

    async def asearch(
        self,
        query: str,
        *,
        conversation_history: _types.ConversationHistory_T,
        verbose: bool = False,
        stream: bool = False,
        **kwargs: Any,
    ) -> Union[_types.SearchResult_T, _types.AsyncStreamSearchResult_T]:
        created = time.time()
        self._logger.info(f"Starting search for query: {query} at {created}") if self._logger else None

        if conversation_history is None:
            conversation_history = _context.ConversationHistory()
        elif isinstance(conversation_history, list):
            conversation_history = _context.ConversationHistory.from_list(conversation_history)

        context_chunks, context_records = self._context_builder.build_context(
            conversation_history=conversation_history,
            **kwargs,
        )
        map_results = list(
            await asyncio.gather(
                *[
                    self._map(query, context, verbose, **kwargs) for context in context_chunks
                ]
            )
        )
        return await self._reduce(map_results, query, verbose, stream, **kwargs)

    async def _map(
        self,
        query: str,
        context: str,
        verbose: bool,
        **kwargs: Any
    ) -> _types.SearchResult_T:
        created = time.time()
        prompt = self._map_sys_prompt.format_map(defaultdict(str, context_data=context, query=query))
        msg = [{"role": "system", "content": prompt}, {"role": "user", "content": query}]
        async with self._semaphore:
            response = cast(
                _llm.ChatResponse_T, (await self._chat_llm.achat(
                    msg=cast(_llm.MessageParam_T, msg),
                    stream=False,
                    **_utils.filter_kwargs(self._chat_llm.achat, kwargs, prefix='map__')
                ))
            )
        result = self._parse_map(response)

        usage = _types.Usage(
            completion_tokens=response.usage.completion_tokens,
            prompt_tokens=response.usage.prompt_tokens,
            total_tokens=response.usage.total_tokens,
        ) if response.usage else None

        if verbose:
            return _types.SearchResultVerbose(
                created=created.__int__(),
                model=self._chat_llm.model,
                system_fingerprint=response.system_fingerprint,
                choice=_types.Choice(
                    finish_reason=response.choices[0].finish_reason,
                    message=_types.Message(
                        content=result,
                        refusal=response.choices[0].message.refusal,
                    ),
                ),
                usage=usage,
                context_data=None,
                context_text=context,
                completion_time=time.time() - created,
                llm_calls=1,
            )
        else:
            return _types.SearchResult(
                created=created.__int__(),
                model=self._chat_llm.model,
                system_fingerprint=response.system_fingerprint,
                choice=_types.Choice(
                    finish_reason=response.choices[0].finish_reason,
                    message=_types.Message(
                        content=result,
                        refusal=response.choices[0].message.refusal,
                    ),
                ),
                usage=usage,
            )

    @staticmethod
    def _parse_map(response: _llm.ChatResponse_T) -> List[Dict[str, Any]]:
        default = [{"answer": "", "score": 0}]
        json_ = _utils.deserialize_json(response.choices[0].message.content or "")
        if json_ == {}:
            return default

        points = json_.get("points", [])
        if not isinstance(points, list):
            return default

        return [
            {"answer": point["description"], "score": int(point["score"])}
            for point in points
            if isinstance(point, dict) and "description" in point and "score" in point
        ]

    async def _reduce(
        self,
        map_results: List[_types.SearchResult_T],
        query: str,
        verbose: bool,
        stream: bool,
        **kwargs: Any
    ) -> Union[_types.SearchResult_T, _types.AsyncStreamSearchResult_T]:
        created = time.time()
        key_points: List[Dict[str, Any]] = []
        for idx, map_ in enumerate(map_results):
            if not isinstance(map_.choice.message.content, list):
                continue
            for ele in map_.choice.message.content:
                if not isinstance(ele, dict) or "answer" not in ele or "score" not in ele:
                    continue
                key_points.append(
                    {
                        "analyst": idx,
                        "answer":  ele["answer"],
                        "score":   ele["score"]
                    }
                )

        key_points = [kp for kp in key_points if isinstance(kp["score"], (int, float)) and kp["score"] > 0]

        if not key_points.__len__() and not self._allow_general_knowledge:
            warnings.warn("No key points found from the map phase", RuntimeWarning)
            return _types.SearchResult(
                created=created.__int__(),
                model=self._chat_llm.model,
                choice=_types.Choice(
                    finish_reason="stop",
                    message=_types.Message(
                        content=self._no_data_answer,
                    ),
                ),
                usage=None,
            ) if not verbose else _types.SearchResultVerbose(
                created=created.__int__(),
                model=self._chat_llm.model,
                choice=_types.Choice(
                    finish_reason="stop",
                    message=_types.Message(
                        content=self._no_data_answer,
                    ),
                ),
                completion_time=time.time() - created,
                llm_calls=0,
            )

        key_points = sorted(
            key_points,
            key=lambda kp: kp["score"] if isinstance(kp["score"], (int, float)) else 0,
            reverse=True
        )

        data: List[str] = []
        total_tokens = 0
        for kp in key_points:
            formatted_response = '\n'.join(
                [f'----Analyst {kp["analyst"] + 1}----', f'Importance score: {kp["score"]}', kp["answer"]]
            )
            total_tokens += _utils.num_tokens(formatted_response, self._token_encoder)
            if total_tokens > self._data_max_tokens:
                warnings.warn("Data exceeds maximum token limit", RuntimeWarning)
                break
            data.append(formatted_response)

        report_data = '\n\n'.join(data)
        prompt = self._reduce_sys_prompt.format_map(defaultdict(str, report_data=report_data))
        if self._allow_general_knowledge:
            prompt += f'\n{self._general_knowledge_sys_prompt}'

        msg = [{"role": "system", "content": prompt}, {"role": "user", "content": query}]
        async with self._semaphore:
            response = await self._chat_llm.achat(
                msg=cast(_llm.MessageParam_T, msg),
                stream=stream,
                **_utils.filter_kwargs(self._chat_llm.achat, kwargs, prefix='reduce__')
            )

        if stream:
            response = cast(_llm.AsyncChatStreamResponse_T, response)
            return self._parse_stream_result(
                response,
                verbose=verbose,
                created=created,
                context_data=None,
                context_text=report_data,
                map_result=map_results,
                reduce_context_data=None,
                reduce_context_text=report_data,
            )
        else:
            response = cast(_llm.ChatResponse_T, response)
            return self._parse_result(
                response,
                verbose=verbose,
                created=created,
                context_data=None,
                context_text=report_data,
                map_result=map_results,
                reduce_context_data=None,
                reduce_context_text=report_data,
            )
