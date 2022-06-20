
from typing import List, Any

# https://stackoverflow.com/a/434328
def chunker(seq: List[Any], size: int):
    for pos in range(0, len(seq), size):
        yield seq[pos:pos + size]
