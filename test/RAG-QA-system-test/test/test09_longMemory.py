import os
import json
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.chat_history import BaseChatMessageHistory
from typing import Sequence
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate, MessagesPlaceholder, ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory


class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id, memory_path):
        # super().__init__()
        self.session_id = session_id
        self.memory_path = memory_path
        self.file_path = os.path.join(self.memory_path, self.session_id)
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        all_message = self.messages
        all_message.extend(messages)
        new_messages = [message_to_dict(message) for message in all_message]
        with open(self.file_path, 'w', encoding="utf-8") as f:
            json.dump(new_messages, f)
    
    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path, 'r', encoding="utf-8") as f:
                return messages_from_dict(json.load(f))
        except FileNotFoundError:
            return []
        
    def clear(self) -> None:
        with open(self.file_path, 'w', encoding="utf-8") as f:
            json.dump([], f)


def get_history(session_id):
    return FileChatMessageHistory(session_id, './chat_history')

model = ChatTongyi(model="qwen3-max-2026-01-23")
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
print(conversation_chain.invoke({"input":"总共提到了几只宠物"}, session_config))
