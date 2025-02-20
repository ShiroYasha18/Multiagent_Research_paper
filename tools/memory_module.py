# tools/memory_module.py

from camel.memories import (
    ChatHistoryBlock,
    LongtermAgentMemory,
    ScoreBasedContextCreator,
    VectorDBBlock,
)
from camel.utils import OpenAITokenCounter
from camel.types import ModelType

def create_memory_module():
    # Configure memory context management
    context_creator = ScoreBasedContextCreator(
        token_counter=OpenAITokenCounter(ModelType.MISTRAL_LARGE),
        token_limit=1024,  # Adjust based on needs
    )

    # Set up different memory types
    chat_history_block = ChatHistoryBlock()
    vector_db_block = VectorDBBlock()

    # Create a long-term memory module
    memory = LongtermAgentMemory(
        context_creator=context_creator,
        chat_history_block=chat_history_block,
        vector_db_block=vector_db_block,
    )

    return memory
