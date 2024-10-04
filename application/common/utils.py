import uuid


def gen_id(prefix: str | None = None, *, __split: str = '-') -> str:
    """Generate a random ID with the given prefix (optional)."""
    return prefix + __split + uuid.uuid4().__str__().replace('-', '') if prefix \
        else uuid.uuid4().__str__().replace('-', '')
