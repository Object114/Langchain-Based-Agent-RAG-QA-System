"""
文件处理
"""
import os, hashlib
from utils.logger_handler import logger
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from utils.config_handler import chroma_config
from utils.path_tool import get_abs_path

def get_file_md5_hex(file_path: str):
    if not os.path.exists(file_path):
        logger.error(f"文件{file_path}不存在")
        return
    if not os.path.isfile(file_path):
        logger.error(f"路径{file_path}不是文件")
        return
    
    chunk_size = 4096 # 分块加载md5，以免文件过大
    md5_obj = hashlib.md5()
    try:
        with open(file_path, "rb") as f: # 以二进制形式读取
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
        return md5_obj.hexdigest()
    except Exception as e:
        logger.error(f"文件{file_path}md5计算失败.{str(e)}")
        return None
    
def check_md5_is_exist(str_md5: str) -> bool:
    # 检查该md5是否已经存在
    if os.path.exists(get_abs_path(chroma_config["md5_hex_path"])):
        with open(get_abs_path(chroma_config["md5_hex_path"]), "r", encoding="utf-8") as f:
            for line in f.readlines():
                line = line.strip()
                if line == str_md5:
                    return True
    return False

def save_md5_str(str_md5):
    with open(get_abs_path(chroma_config["md5_hex_path"]), 'a', encoding="utf-8") as f:
        f.write(str_md5 + '\n')

def list_files(path: str, types: tuple[str]):
    files = []
    if not os.path.isdir(path):
        logger.error(f"{path}不是文件夹")
        return None
    
    for file in os.listdir(path):
        if file.endswith(types):
            files.append(os.path.join(path, file))
    
    return tuple(files) # 转换成元组后续不允许修改

def pdf_loader(file_path:str, password=None) -> list[Document]:
    return PyPDFLoader(file_path, password).load()

def txt_loader(file_path:str) -> list[Document]:
    return TextLoader(file_path, encoding="utf-8").load()

def get_file_documents(read_path: str, password=None):
    if read_path.endswith("txt"):
        return txt_loader(read_path)
    elif read_path.endswith("pdf"):
        return pdf_loader(read_path, password)
    else:
        return []