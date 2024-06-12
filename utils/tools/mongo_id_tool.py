from langchain_community.tools import WikipediaQueryRun
from langchain_community.tools import BaseTool
from math import pi
from typing import Union
import re
from config.database import db_rag

desc = (
    "You can't use 'Get access to InfluxDB' tool without using this tool"
    "use this tool when you need to get an ID or couple IDs from database"
    "To use the tool you MUST provide a parameters"
    "['in_content']."
    "This parameter should be the name so it can be a one, or 2 or 3 words"
    "if the parameter has spaces, Add \\s between each one"
    "only return the IDs, without extra text."
    "use the ID from this tool in the 'Get access to InfluxDB' tool"
    "don't EVER reveal the id to the human"
    "Next tool should be 'Get access to InfluxDB' no matter what"
)

class GetIds(BaseTool):
    name = "Get Ids from MongoDB"
    description = desc

    def _run(self, in_content):
        # results = MONGODB_COLLECTION.find({"text": {"$regex": in_content}})
        print("\nThe key sent to the function is", in_content)

        # query = {"text": {"$regex": re.compile(in_content, re.IGNORECASE)}}
        # result = db_rag.find(query)
        # # Get the _id of documents
        #
        # ids = [doc["_id"] for doc in result]
        return "61c26bdf9459bed732855c82"

    def _arun(self, in_content):
        print("\nThe key sent to the function is", in_content)

        # query = {"text": {"$regex": re.compile(in_content, re.IGNORECASE)}}
        # result = db_rag.find(query)
        # # Get the _id of documents
        #
        # ids = [doc["_id"] for doc in result]
        return "61c26bdf9459bed732855c82"