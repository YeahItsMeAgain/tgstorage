
from typing import List, Any

def chunker(seq: List[Any], size: int):
    for pos in range(0, len(seq), size):
        yield seq[pos:pos + size]
