import os
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
load_dotenv()


uri = os.getenv("MONGODB_TOKEN")
# Create a new client and connect to the server
client = MongoClient(uri)

# Define the MongoDB database and collection names
DB_NAME = "mydb"

# Connect to the specific collection in the database
db_chat = client[DB_NAME]["chat_logs"]

db_rag = client[DB_NAME]['Agent_RAG']