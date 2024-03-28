from fastapi import APIRouter
from models.logs_model import LogsModel
from config.database import db_chat
from schema.schemas import list_serial
from bson import ObjectId
from utils.agent import Agent
from datetime import date
from pydantic import BaseModel
from datetime import datetime

import json
router = APIRouter()
print("LOADING THE AGENT...")
agent = Agent()
agent = agent.initializing_agent()
print("AGENT LOADED SUCCESSFULLY!")



# GET REQUEST METHOD
@router.get("/get-all-chat")
async def get_chat_logs():
    chat = list_serial(db_chat.find())

    return chat



# POST REQUEST METHOD
@router.post("/send-msg")
async def send_message(new_chat_message: LogsModel):
    # Get today's date as a string
    today = date.today().isoformat()
    id = ""
    documents = list(db_chat.find({"date": today}))
    l = len(documents)
    if l <= 0:
        print("IN THE POST FUNCTION")
        doc = db_chat.insert_one({
            "user_id": 2,
            "date": today,
            "logs": [dict(new_chat_message)]
        })
        id = doc.inserted_id
    else:
        print("IN THE PUT FUNCTION")
        # print(list(documents))
        id = documents[0]["_id"]
        doc = db_chat.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$push": {"logs": dict(new_chat_message)}}
        )
    # print("---------------------------")
    response = agent(new_chat_message.message)
    ai_chat_message = {
        "senderId": 9,
        "message": str(response["output"]),
        "timestamp": datetime.utcnow()
    }
    db_chat.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$push": {"logs": dict(ai_chat_message)}}
    )
    return ai_chat_message


    
    
    
# PUT REQUEST METHOD
@router.put("/{id}")
async def update_logs(id: str, new_chat_log):
    db_chat.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$push": {"logs": json.loads(new_chat_log)}}
    )