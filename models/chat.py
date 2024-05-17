from typing import List
from pydantic import BaseModel
from datetime import datetime


class Message(BaseModel):
    user_id: str
    message: str
    time: datetime


class ChatDB(BaseModel):
    laporan_id: str
    user_id: str
    messages: List[Message]


class Chat(BaseModel):
    laporan_id: str
    user_id: str
    sender: str = "user"
    messages: str
