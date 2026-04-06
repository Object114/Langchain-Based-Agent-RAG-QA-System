from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

model = ChatTongyi(model="qwen3-max")

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

first_prompt = PromptTemplate.from_template(
    "我的邻居姓：{last_name}, 生了一个{gender}, 请帮我起一个名字, 仅回复名字"
)

second_prompt = PromptTemplate.from_template(
    "姓名: {name}, 请解析这个名字, 简短回答"
)

my_func = RunnableLambda(lambda msg : {"name":msg.content})

# chain = first_prompt | model | my_func | second_prompt | model | str_parser
chain = first_prompt | model | (lambda msg : {"name":msg.content}) | second_prompt | model | str_parser

print(chain.invoke({"last_name":"刘", "gender":"女儿"}))