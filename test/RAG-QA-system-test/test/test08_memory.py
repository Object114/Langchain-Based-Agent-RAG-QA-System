from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
#短期存储，临时存储
memory = {}

def get_history(session_id):
    if session_id not in memory:
        memory[session_id] = InMemoryChatMessageHistory()
    return memory[session_id]

model = ChatTongyi(model="qwen3-max")
# prompt = PromptTemplate.from_template(
#     "请根据会话的历史信息来回答对应的问题。对话历史：{chat_history}, 用户提问：{input}"
# )
prompt = ChatPromptTemplate(
    [
        ("system", "请根据以下会话的历史信息回应用户问题，对话历史："),
        MessagesPlaceholder("chat_history"),
        ("human", "请回答问题：{input}")
    ]
)
str_parser = StrOutputParser()

base_chain = prompt | model | str_parser

conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

session_config = {
    "configurable":{
        "session_id":"01"
    }
}
print(conversation_chain.invoke({"input":"小明有2只猫"}, session_config))
print(conversation_chain.invoke({"input":"小红有3只狗"}, session_config))
print(conversation_chain.invoke({"input":"总共有几只狗"}, session_config))

