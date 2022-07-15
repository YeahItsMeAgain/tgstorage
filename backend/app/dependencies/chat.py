from typing import Union
from fastapi import Request

def get_current_chat(request: Request) -> Union[int, None]:
    return request.session.get('chat_id', None)
