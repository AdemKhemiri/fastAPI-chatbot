from langchain_community.tools import WikipediaQueryRun
from langchain_community.tools import BaseTool
from math import pi
from typing import Union
import re
from config.database import db_rag

desc = (
    "use this tool when you need to get an ID or couple IDs from database"
    "To use the tool you MUST provide a parameters"
    "['in_content']."
    "This parameter should be the name so it can be a one, or 2 or 3 words"
    "if the parameter has spaces, Add \\s between each one"
    "only return the IDs, without extra text."
)

class GetIds(BaseTool):
    name = "Get Ids from DB"
    description = desc

    def _run(self, in_content):
        # results = MONGODB_COLLECTION.find({"text": {"$regex": in_content}})
        print("\nThe key sent to the function is", in_content)

        query = {"text": {"$regex": re.compile(in_content, re.IGNORECASE)}}
        result = db_rag.find(query)
        # Get the _id of documents

        ids = [doc["_id"] for doc in result]
        return ids

    def _arun(self, in_content):
        raise NotImplementedError("This tool does not support async")