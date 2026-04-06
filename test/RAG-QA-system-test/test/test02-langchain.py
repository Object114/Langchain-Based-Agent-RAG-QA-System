from langchain_community.llms.tongyi import Tongyi
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_community.embeddings import DashScopeEmbeddings

### LLM
# model = Tongyi(model="qwen-max")
# res = model.invoke(input="你是谁，简短回答")
# print(res)

# # 流式输出
# res = model.stream(input="你是谁")
# for chunk in res:
#     print(chunk, end="", flush=True)

### caht model
# model = ChatTongyi(model="qwen3-max-2026-01-23")
# messages = [
#     SystemMessage(content="你是一个诗人"),
#     HumanMessage(content="写一个三行俳句"),
#     AIMessage(conten="")
# ]
# messages 简写
# messages = [
#     ("system", "你是一个诗人"),
#     ("human", "写一个三行俳句"),
#     ("ai", "")
# ]
# res = model.invoke(input=messages)
# print(res.content)

# embedding 模型
model = DashScopeEmbeddings()
print(model.embed_query("Hello world"))
print(model.embed_documents(["Hello world", "你是谁", "你好"]))