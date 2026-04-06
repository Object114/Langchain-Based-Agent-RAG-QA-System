from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

model = ChatTongyi(model="qwen3-max-2026-01-23")
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "请根据以下提供资料, 简介回复用户问题, 参考资料：{context}"),
        ("user", "用户提问：{input}")
    ]
)
vector_db = InMemoryVectorStore(embedding=DashScopeEmbeddings())
vector_db.add_texts(
    ["减肥就是要少吃多练", "在减脂期间吃东西很重要,清淡少油控制卡路里摄入并运动起来", "跑步是很好的运动哦"]
)

input_text = "如何科学减肥"

# result = vector_db.similarity_search(input_text, 2)
# context = "["
# for doc in result:
#     context += doc.page_content
# context += "]"

# chain = prompt_template | model | StrOutputParser()
# print(chain.invoke({"context":context, "input":input_text}))

def format_func(docs):
    if not docs:
        return "无"
    ret = "["
    for doc in docs:
        ret += doc.page_content
    ret += "]"
    return ret

retriever = vector_db.as_retriever(search_kwargs={"k":2})
chain = (
    {"input":RunnablePassthrough(), "context": retriever|format_func} | prompt_template | model |StrOutputParser()
)
print(chain.invoke(input_text))