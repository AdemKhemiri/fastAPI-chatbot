from datetime import datetime
from pydantic import BaseModel
from typing import List

class LogsModel(BaseModel):
    senderId: int
    message: str
    timestamp: datetime