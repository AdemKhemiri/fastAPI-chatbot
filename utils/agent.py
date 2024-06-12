from langchain_openai import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain.agents import initialize_agent, AgentExecutor, create_react_agent
from config.database import db_rag
from langchain.agents import Tool, load_tools
from utils.tools.mongo_id_tool import GetIds
from utils.tools.influxdb_tool import GetInfluxData
import os
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory, BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGODB_TOKEN = os.getenv("MONGODB_TOKEN")

prompt = '''
You are Orbit Assistant, a large language model trained by OpenAI.

Orbit Assistant is an Energy Management Expert. Your mission is to provide insights, advice, and strategies related to 
energy efficiency, renewable sources, and sustainable practices. Engage with users by explaining concepts, 
analyzing data, and recommending solutions. Be informative, approachable, and adaptable to different energy-related 
topics. 

TOOLS: ------

Orbit Assistant has access to the following tools:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```
Before you use the tool named 'Get access to InfluxDB' make SURE you use the tool named 'Get Ids from MongoDB'
This is REALLY IMPORTANT thing to do, the order of the tools is important

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{chat_history}

New input: {input}
{agent_scratchpad}
'''

class Agent:
    chat_template = ChatPromptTemplate.from_messages(
        [
            ("system", prompt)
        ]
    )

    def __init__(self, db_rag=db_rag, openai_api_key=OPENAI_API_KEY):
        self.vector_search = MongoDBAtlasVectorSearch(
            db_rag,
            OpenAIEmbeddings(),
            index_name="vector_index"
        )

        self.llm = ChatOpenAI(
            openai_api_key=OPENAI_API_KEY,
            model_name='gpt-3.5-turbo',
            temperature=0.0
        )
        self.mongo_history = MongoDBChatMessageHistory(
            connection_string=MONGODB_TOKEN,
            session_id="id_aaa",
            database_name="mydb",
            collection_name="chat_histories"
        )
        self.conversational_memory = ConversationBufferWindowMemory(
            chat_memory=self.mongo_history,
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
        # agent = create_react_agent(self.llm, tools, self.chat_template)
        # agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        # memory = ChatMessageHistory(session_id="test-session")
        # agent_with_chat_history = RunnableWithMessageHistory(
        #     agent_executor,
        #     # This is needed because in most real world scenarios, a session id is needed
        #     # It isn't really used here because we are using a simple in memory ChatMessageHistory
        #     lambda session_id: memory,
        #     input_messages_key="input",
        #     history_messages_key="chat_history",
        # )
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
        # print(agent.agent.llm_chain.prompt.messages)
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
            database_name="mydb",
            collection_name="chat_histories"
        )
        self.conversational_memory = ConversationBufferWindowMemory(
            chat_memory=self.mongo_history,
            memory_key='chat_history',
            k=10,
            return_messages=True
        )
        return self.conversational_memory



