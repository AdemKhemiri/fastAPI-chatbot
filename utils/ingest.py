from langchain.document_loaders import WebBaseLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings

from config.database import db_rag

# Step 1: Load
loaders = [
 PyPDFLoader("ResumeWorded.pdf"),
 WebBaseLoader("https://en.wikipedia.org/wiki/AT%26T"),
 WebBaseLoader("https://en.wikipedia.org/wiki/Bank_of_America"),
 PyPDFLoader("A_Compelling_Global_Resource.pdf"),
 PyPDFLoader("guidebook_for_energy_efficiency_evaluation_measurement_verification.pdf"),
]

data = []
for loader in loaders:
    data.extend(loader.load())
    
    
# Step 2: Transform (Split)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20,
                                               separators=["\n\n", "\n", "(?<=\. )", " "], length_function=len)
docs = text_splitter.split_documents(data)
print('Split into ' + str(len(docs)) + ' docs')

vector_search = MongoDBAtlasVectorSearch.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    collection=db_rag,
    index_name="vector_index"  # Use a predefined index name
)
print("-----------------------------------------------")
print("VECTORIZING COMPLETE")
print("-----------------------------------------------")