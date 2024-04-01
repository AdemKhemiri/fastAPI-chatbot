from langchain_openai import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain.agents import initialize_agent
from config.database import db_rag
from langchain.agents import Tool, load_tools
from utils.tools.mongo_id_tool import GetIds
from utils.tools.influxdb_tool import GetInfluxData
import os
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory, BaseChatMessageHistory

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGODB_TOKEN = os.getenv("MONGODB_TOKEN")
class Agent:

    def __init__(self, db_rag=db_rag, openai_api_key=OPENAI_API_KEY):
        self.vector_search = MongoDBAtlasVectorSearch(
            db_rag,
            OpenAIEmbeddings(),
            index_name="vector_index"
        )

        self.llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model_name='gpt-3.5-turbo',
            temperature=0.0
        )
        self.mongo_history = MongoDBChatMessageHistory(
            connection_string=MONGODB_TOKEN,
            session_id="id_aaaaaaaaaaa",
            database_name="mydb",
            collection_name="chat_histories"
        )
        self.conversational_memory = ConversationBufferWindowMemory(
            chat_memory = self.mongo_history,
            memory_key='chat_history',
            k=10,
            return_messages=True
        )
        # retrieval qa chain
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_search.as_retriever(search_kwargs={'k': 3})
        )
    def initializing_agent(self):
        # self.mongoMemoryChatHistory()
        tools = self.get_all_tools()
        agent = initialize_agent(
                agent="chat-conversational-react-description",
                tools=tools,
                llm=self.llm,
                verbose=True,
                max_iterations=5,
                early_stopping_method='generate',
                memory=self.conversational_memory,
                handle_parsing_errors=True
            )
        return agent
    
    def get_all_tools(self):
        tools = load_tools(
            ['llm-math'],
            llm=self.llm
        )
        knowledge_tool = Tool(
                            name='Knowledge Base',
                            func=self.qa.run,
                            description=(
                                'use this tool when answering general knowledge queries to get '
                                'more information about the topic'
                            )
                        )
        tools.append(knowledge_tool)
        tools.append(GetIds())
        tools.append(GetInfluxData())
        return tools
        

    def Clear_memory(self):
        self.conversational_memory.memory.clear() 


    def get_agent_memory_session_id(self, session_id):
        self.mongo_history = MongoDBChatMessageHistory(
            connection_string=MONGODB_TOKEN,
            session_id=session_id,
            database_name = "mydb",
            collection_name = "chat_histories"
        )
        self.conversational_memory = ConversationBufferWindowMemory(
            chat_memory=self.mongo_history,
            memory_key='chat_history',
            k=10,
            return_messages=True
        )
        return self.conversational_memory























