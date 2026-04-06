import os
import json
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

try:
    with open("config.json", 'r') as f:
        config = json.load(f)
except: FileExistsError

def check_md5(md5_str):
    if os.path.exists(config["md5_path"]):
        for line in open(config["md5_path"], 'r', encoding="utf-8").readlines():
            line = line.strip()
            if line == md5_str:
                return True
    return False    
    
def save_md5(md5_str):
    with open(config["md5_path"], 'a', encoding="utf-8") as f:
        f.write(md5_str + '\n')

def string_to_md5(input_str:str):
    input_bytes = input_str.encode(encoding="utf-8")
    return hashlib.md5(input_bytes).hexdigest()

class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config["vector_db_dir"], exist_ok=True)
        self.chroma = Chroma(
            collection_name=config["vector_db_name"],
            embedding_function=DashScopeEmbeddings(),
            persist_directory=config["vector_db_dir"]
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config["chunk_size"],
            chunk_overlap=config["chunk_overlap"],
            separators=config["separators"],
            length_function=len,
        )

    # 向数据库中添加信息
    def upload_str(self, data: str, filename):
        str_md5 = string_to_md5(data)

        # 去除重复信息
        if check_md5(str_md5):
            return "File exists"
        if len(data) > config["max_split_len"]:
            chunks = self.spliter.split_text(data)
        else:
            chunks = [data]

        meta_data = {
            "source": filename,
            "create_time": datetime.now().strftime("%y-%m-%d %H:%M:%S")
        }
        self.chroma.add_texts(
            chunks,
            metadatas=[meta_data for _ in chunks]
        )
        save_md5(str_md5)
        return "Upload Success"
    
