from tortoise.contrib.pydantic import pydantic_model_creator
from app.db.models import SharedResource as ShareModel

ViewShare = pydantic_model_creator(
    ShareModel, name=f'View{ShareModel.__name__}',
    include=['shared_user_email']
)

ShareType = ViewShare
