from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma

store_in_memory = InMemoryVectorStore(
    embedding=DashScopeEmbeddings()
)
store_in_file = Chroma(
    collection_name="test", # 表名
    embedding_function=DashScopeEmbeddings(),
    persist_directory='./vector_db' # 存储路径
)
loader = CSVLoader(
    file_path="./data/stu.csv"
)
documents = loader.load()

vector_store= store_in_file

# 添加数据
vector_store.add_documents(
    documents=documents,
    ids=[f'id{i}' for i in range(0, len(documents))], # 指定每条数据的id索引
)
# 删除数据
vector_store.delete(['id1', 'id2'])
# 查找数据
result = vector_store.similarity_search(
    query="Hello",
    k=3, # 返回top-k条相关数据
)
print(result)
