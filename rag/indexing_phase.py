from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore

pdf_path = Path(__file__).parent / "nodejs.pdf"


load_dotenv()
# Load file into the python program

loader = PyPDFLoader(file_path=pdf_path)
# page wise chunking
docs = loader.load()


print(docs[12])


# Split the docs into the smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)


chunks = text_splitter.split_documents(documents=docs)
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_rag",
)


print("INDEXING PHASE DONE")
