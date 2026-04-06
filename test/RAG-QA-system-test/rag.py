from vector_retrieve import VectorRetrieve
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda
from history_store import get_history

class RagService(object):
    def __init__(self):
        self.retriever = VectorRetrieve().get_retriever()
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", "请以我提供的参考信息, 简洁地回答用户的问题。参考资料: {context}"),
                ("system", "另外与用户的对话历史记录如下:"),
                MessagesPlaceholder("history"),
                ("user", "请回答用户提问: {input}")
            ]
        )
        self.model = ChatTongyi(model="qwen3-max-2026-01-23")
        self.chain = self.__get_chain()
    
    def __get_chain(self):
        def format_document(docs):
            if not docs:
                return "无参考资料"
            ret = ""
            for doc in docs:
                ret += doc.page_content
            return ret
        
        def format_for_input(dic):
            return dic["input"]
        
        def format_for_history(dic):
            return dic["history"]

        chain = (
            {
                "input": RunnableLambda(format_for_input),
                "context": RunnableLambda(format_for_input) | self.retriever | format_document,
                "history": RunnableLambda(format_for_history)
            } | self.prompt_template | self.model | StrOutputParser()
        )
        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history"
        )

        return conversation_chain
    
if __name__ == '__main__':
    session_config = {
        "configurable":{
            "session_id":"01"
        }
    }
    answer = RagService().chain.invoke({"input": "我的上一个提问是什么，再为我简单扩展一下"}, session_config)
    print(answer)
