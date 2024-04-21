from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import OpenAIEmbeddings

from config.database import db_rag

# Step 0: delete everything in mongo db
#db_rag.delete_many({})

# Step 1: Load
loaders = [
    PyPDFLoader("rag_data/CV_Adam_Khemiri.pdf"),
    PyPDFLoader("rag_data/best-practises-for-industrial-ee-web.pdf"),
    PyPDFLoader("rag_data/Electrical Installation Guide 2018.pdf"),
    PyPDFLoader("rag_data/Solutions de filtrage pour l'amélioration de l'efficacité énergétique.pdf"),
    PyPDFLoader("rag_data/ISO_500001_EN.pdf"),
    PyPDFLoader("rag_data/Household Appliances and Their Power Consumption.pdf"),
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