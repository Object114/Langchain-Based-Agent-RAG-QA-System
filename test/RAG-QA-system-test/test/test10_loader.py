from langchain_community.document_loaders import CSVLoader, JSONLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# CSV
# loader = CSVLoader(
#     file_path="./data/stu.csv",
#     csv_args={
#         "delimiter":",",
#         "quotechar":'"',
#         "fieldnames":['a', 'b', 'c', 'd']
#     }
#     )

# # print(loader.load())
# for document in loader.lazy_load():
#     print(document)

# Json
# loader = JSONLoader(
#     file_path="./data/stus.json",
#     jq_schema=".[].name",
#     text_content=False, # 选择False可以嵌套字典格式
#     json_lines=False, # 读取的文件是否是json lines的格式
# )
# print(loader.load())

# TextLoader和文档分割器
# loader = TextLoader(
#     file_path="./data/Python基础语法.txt",

# )
# # print(loader.load())

# spliter = RecursiveCharacterTextSplitter(
#     chunk_size=500,
#     chunk_overlap=50,
#     separators=["\n\n", "\n", ".", "!", "?", "。", "？", "！", " ", ""],
#     length_function=len,
# )
# split_docs = spliter.split_documents(loader.load())
# print(split_docs)
# print(len(split_docs))

# PDF
loader = PyPDFLoader(
    file_path="./data/pdf1.pdf",
    mode="page", # 指定page/singel模式，默认是page
)
for i, doc in enumerate(loader.lazy_load()):
    # print(i)
    print(doc)
