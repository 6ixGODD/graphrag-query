import logging
import sys

from ._search import (
    AsyncChatLLM, AsyncLocalSearchEngine, ConversationHistory, ConversationRole, Embedding, LocalContextLoader,
)  # ChatLLM, ConversationHistory, ConversationRole, Embedding, LocalContextLoader, LocalSearchEngine,

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
logger.info('Starting the LocalSearchEngine')
# logger.info('Starting the GlobalSearchEngine')

# with open('sys_prompt.txt', 'r') as f:
#     sys_prompt = f.read()
from ._search._defaults import (LOCAL_SEARCH__SYS_PROMPT)
sys_prompt = LOCAL_SEARCH__SYS_PROMPT
# noinspection PyTypeChecker
engine = AsyncLocalSearchEngine(
    chat_llm=AsyncChatLLM(
        model='glm-4-plus',
        api_key='de93b21f9b0d5ae4a697ed985fe0a5f2.bInHitqmRqTAfNZy',
        base_url='https://open.bigmodel.cn/api/paas/v4'
    ),
    embedding=Embedding(
        model='embedding-3',
        api_key='de93b21f9b0d5ae4a697ed985fe0a5f2.bInHitqmRqTAfNZy',
        base_url='https://open.bigmodel.cn/api/paas/v4'
    ),
    context_loader=LocalContextLoader.from_parquet_directory('kg/tcm-glm4_flash-glm_embedding_3'),
    logger=logger,
    sys_prompt=sys_prompt
)

# noinspection PyTypeChecker
# global_search_engine = AsyncGlobalSearchEngine(
#     chat_llm=AsyncChatLLM(
#         model='glm-4-flash',
#         api_key='de93b21f9b0d5ae4a697ed985fe0a5f2.bInHitqmRqTAfNZy',
#         base_url='https://open.bigmodel.cn/api/paas/v4'
#     ),
#     embedding=Embedding(
#         model='embedding-3',
#         api_key='de93b21f9b0d5ae4a697ed985fe0a5f2.bInHitqmRqTAfNZy',
#         base_url='https://open.bigmodel.cn/api/paas/v4'
#     ),
#     context_loader=GlobalContextLoader.from_parquet_directory('../kg/tcm-glm4_flash-glm_embedding_3'),
#     logger=logger
# )

conversation_history = ConversationHistory()
conversation_history.max_length = 10


# while True:
#     user_input = input('You: ')
#     conversation_history.add_turn(ConversationRole.USER, user_input)
#     response = engine.search(user_input, conversation_history=conversation_history, stream=True)
#     print(f"Response: ")
#     content = ''
#     for chunk in response:
#         c = chunk.choice.delta.content
#         print(c, end='')
#         content += c or ''
#     print('')
#     conversation_history.add_turn(ConversationRole.ASSISTANT, content)
async def main():
    while True:
        user_input = input('You: ')
        conversation_history.add_turn(ConversationRole.USER, user_input)
        response = await engine.asearch(user_input, conversation_history=conversation_history, stream=True)
        print(f"Response: ")
        content = ''
        async for chunk in response:
            c = chunk.choice.delta.content
            sys.stdout.write(c or '')
            sys.stdout.flush()
            content += c or ''
        sys.stdout.write('\n')
        conversation_history.add_turn(ConversationRole.ASSISTANT, content)
        # Exit when pressing Ctrl+C or Esc
        if user_input in ['\x03', '\x1b']:
            break


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
