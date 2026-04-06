from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_community.llms.tongyi import Tongyi

model = Tongyi(model="qwen-max")
example_template = PromptTemplate.from_template("单词：{word}, 反义词：{antonym}")

example_data = [
    {"word": "大", "antonym":"小"},
    {"word": "上", "antonym":"下"}
]

fewshot_tempalte = FewShotPromptTemplate(
    example_prompt=example_template,
    examples=example_data,
    prefix="有以下反义词示例：",
    suffix="基于以上示例, 告诉我{input_word}的反义词, 简单回答",
    input_variables=["input_word"] # 声明要前缀或后缀中所需要注入的变量名
)

fewshot_prompt = fewshot_tempalte.invoke(input={"input_word":"开心"}).to_string() # invoke得到PromptValue类对象
# print(fewshot_prompt)
print(model.invoke(fewshot_prompt))