import os
from agno.document.base import Document

from agno.knowledge import AgentKnowledge
from agno.vectordb.milvus.milvus import Milvus
from agno.embedder.google import GeminiEmbedder


MILVUS_URI = os.environ["MILVUS_URI"]
MILVUS_TOKEN = os.environ["MILVUS_TOKEN"]
LLM_API_KEY = os.environ["LLM_API_KEY"]


knowledge_base = AgentKnowledge(
    vector_db=Milvus(
        uri=MILVUS_URI,
        token=MILVUS_TOKEN,
        collection="petra",
        embedder=GeminiEmbedder(api_key=LLM_API_KEY),
    )
)


def add_new_document(doc_text: str):
    knowledge_base.load_text(doc_text, upsert=True)


def add_documents(docs: list[Document]):
    knowledge_base.load_documents(docs, upsert=True)


def add_document(docs: list[Document]):
    knowledge_base.load_document(docs, upsert=True)
