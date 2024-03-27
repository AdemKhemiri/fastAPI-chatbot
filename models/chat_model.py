from pydantic import BaseModel, Field
from typing import List
from datetime import date

class ChatModel(BaseModel):
    user_id: int
    date: date
    logs: List