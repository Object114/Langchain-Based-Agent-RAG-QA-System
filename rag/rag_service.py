"""
根据用户提问，搜索参考资料，将检索出来的信息提供给模型，让模型总结回复
"""
from rag.vector_store import VectorStore
from utils.prompt_loader import load_rag_prompts
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

class RagSummarizeService:
    def __init__(self):
        self.retriever = VectorStore().get_retriever()
        self.prompt_template = PromptTemplate.from_template(load_rag_prompts())
        self.model = chat_model
        self.chain = self.__get_chain()

    def __get_chain(self):
        return self.prompt_template | self.model | StrOutputParser()
    
    # def retrieve_docs(self, query: str) -> list[Document]:
    #     return self.retriever.invoke(query)
    
    def retrieve_and_summarize(self, query: str) -> str:
        docs:list[Document] = self.retriever.invoke(query)
        context = ""
        for i, doc in enumerate(docs):
            context += f"参考资料[{i}]: {doc.page_content}"

        return self.chain.invoke(
            {
                "input": query,
                "context": context
            }
        )

if __name__ == "__main__":
    res = RagSummarizeService().retrieve_and_summarize("129平方米大小的房子适合什么样的扫地机器人？")
    print(res)
