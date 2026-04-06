from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate

model = ChatTongyi(model="qwen3-max")

# prompt_template = PromptTemplate.from_template(
#     "My neigborhood's last name is{last_name}, and born a {gender}, please give a name, answer briefly."
# )

# # aimessage转字符串
# parser = StrOutputParser()
# chain = prompt_template | model | parser | model

# res = chain.invoke({"last_name":"Brayn", "gender":"boy"})
# print(res.content)

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

first_prompt = PromptTemplate.from_template(
    "我的邻居姓：{last_name}, 生了一个{gender}, 请帮我起一个名字, 简单回复。并且将回复封装在json格式中, 其中key是name, 所起的名字就是value"
)

second_prompt = PromptTemplate.from_template(
    "姓名: {name}, 请解析这个名字, 简短回答"
)

chain = first_prompt | model | json_parser | second_prompt | model | str_parser
print(chain.invoke({"last_name":"陈", "gender":"女儿"}))