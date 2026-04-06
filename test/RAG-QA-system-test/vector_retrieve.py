from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
import json

try:
    with open("config.json", 'r', encoding="utf-8") as f:
        config = json.load(f)
except: FileExistsError

class VectorRetrieve(object):
    def __init__(self):
        self.chroma = Chroma(
            collection_name=config["vector_db_name"],
            embedding_function=DashScopeEmbeddings(),
            persist_directory=config["vector_db_dir"]
        )

    def get_retriever(self):
        return self.chroma.as_retriever(search_kwargs={"k": config["retrieve_top_k"]})
    