from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool

@tool(description="天气查询，传入城市名字，返回字符串信息")
def get_weather(name:str):
    return f"城市{name}的天气是大雨"

agent = create_agent(
    model = ChatTongyi(model="qwen3-max-2026-01-23"),
    tools = [get_weather],
    system_prompt="你是一个聊天助手，回答问题时请输出工具调用的过程，",
)

# res = agent.invoke(
#     {
#         "messages":[
#             {"role": "user", "content": "明天北京的天气怎么样？"}
#         ]
#     }
# )
# print(res)

# 流式输出
for chunk in agent.stream(
    {
        "messages":[
            {"role": "user", "content": "明天北京的天气怎么样？"}
        ]
    },
    stream_mode="values"
):
    latest_message = chunk["messages"][-1]
    if latest_message.content:
        print(type(latest_message).__name__, latest_message.content)
    try:
        if latest_message.tool_calls:
            print(f"工具调用：{[use_tool["name"] for use_tool in latest_message.tool_calls]}")
    except: pass
