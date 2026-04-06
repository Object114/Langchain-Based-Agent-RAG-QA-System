from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi

model = ChatTongyi(model="qwen3-max")
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个诗人"),
        MessagesPlaceholder("history"),
        ("human", "请再来一首唐诗")
    ]
)

history_chat = [
    ("human", ""),
    ("ai", ""),
    ("human", ""),
    ("ai", "")
]

prompt_text = chat_prompt_template.invoke({"history": history_chat})
print(model.invoke(prompt_text).content)
