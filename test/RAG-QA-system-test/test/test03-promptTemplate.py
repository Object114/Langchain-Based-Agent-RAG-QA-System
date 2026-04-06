from langchain_core.prompts import PromptTemplate
from langchain_community.llms.tongyi import Tongyi

prompt_template = PromptTemplate.from_template(
    "My neigborhood's last name is{last_name}, and born a {gender}, please give a name, answer briefly."
)


model = Tongyi(model="qwen-max")
# print(model.invoke(input=prompt_template.format(last_name="Smith", gender="girl")))

# 执行链条示例
chain = prompt_template | model
res = chain.invoke(input={"last_name":"Smith", "gender":"boy"})
print(res)