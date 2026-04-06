"""
RAG向量存储功能
"""
from langchain_chroma import Chroma
from utils.config_handler import chroma_config
from utils.file_handler import check_md5_is_exist, save_md5_str, get_file_md5_hex, list_files, get_file_documents
from model.factory import embedding_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.logger_handler import logger
from utils.path_tool import get_abs_path

class VectorStore:
    def __init__(self):
        self.vector_data_base = Chroma(
            collection_name=chroma_config["collection_name"],
            embedding_function=embedding_model,
            persist_directory=get_abs_path(chroma_config["persist_directory"]),
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_config["chunk_size"],
            chunk_overlap=chroma_config["chunk_overlap"],
            separators=chroma_config["separators"],
            length_function=len
        )
    
    def get_retriever(self):
        return self.vector_data_base.as_retriever(search_kwargs={"k":chroma_config["k"]})
    
    def load_document(self):
        files_path = list_files(get_abs_path(chroma_config["data_path"]), tuple(chroma_config["allow_data_type"]))
        for path in files_path:
            md5_str = get_file_md5_hex(path)
            if check_md5_is_exist(md5_str):
                logger.info(f"[加载知识库]{path}内容已经存在，跳过")
                continue
            try:
                documents = get_file_documents(path)

                if not documents:
                    logger.warning(f"[加载知识库]{path}路径中文本为空")
                    continue

                split_document = self.spliter.split_documents(documents)

                if not split_document:
                    logger.warning(f"[加载知识库]{path}分片后没有有效内容")
                    continue

                # 将内容存入向量数据库
                self.vector_data_base.add_documents(split_document)
                
                save_md5_str(md5_str)
                logger.info(f"[加载知识库]{path}加载成功")
            except Exception as e:
                logger.error(f"[加载知识库]{path}加载失败: {str(e)}", exc_info=True)
                continue

if __name__ == "__main__":
    store = VectorStore()
    store.load_document()

    res = store.get_retriever().invoke("Hello")
    for output in  res:
        print(output.page_content)
        print("="*20)
