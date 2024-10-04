from typing import Optional

import tiktoken


def num_tokens(text: str, token_encoder: Optional[tiktoken.Encoding] = None) -> int:
    """Return the number of tokens in the given text."""
    token_encoder = token_encoder or tiktoken.get_encoding("cl100k_base")
    return token_encoder.encode(text).__len__()
