from langchain_core.chat_history import BaseChatMessageHistory
from typing import Sequence
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
import json, os

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
