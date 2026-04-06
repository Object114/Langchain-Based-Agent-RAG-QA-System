from langchain.agents import create_agent, AgentState
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool
from langchain.agents.middleware import before_agent, after_agent, before_model, after_model, wrap_model_call, wrap_tool_call
from langgraph.runtime import Runtime

@tool(description="天气查询，传入城市名字，返回字符串信息")
def get_weather(name:str):
    return f"城市{name}的天气是大雨"

# agent执行前
@before_agent
def log_before_agent(state, runtime):
    print(f"[before agent] agent 启动, 附带{len(state["messages"])}条消息")

# agent执行后
@after_agent
def log_after_agent(state, runtime):
    print(f"[after agent] agent 结束, 附带{len(state["messages"])}条消息")

# model执行前
@before_model
def log_before_model(state, runtime):
    print(f"[before model] model 启动, 附带{len(state["messages"])}条消息")

# model执行后
@after_model
def log_after_model(state, runtime):
    print(f"[after model] model 结束, 附带{len(state["messages"])}条消息")

# 模型执行中
@wrap_model_call
def model_call_hook(request, handler):
    print("模型调用中")
    return handler(request)

# tool执行中
@wrap_tool_call
def monitor_tool(request, handler):
    print(f"工具执行：{request.tool_call['name']}")
    print(f'工具传入参数：{request.tool_call['args']}')
    return handler(request)

agent = create_agent(
    model = ChatTongyi(model="qwen3-max-2026-01-23"),
    tools = [get_weather],
    middleware=[log_before_agent, log_before_model, log_after_agent, log_after_model, model_call_hook, monitor_tool],
    system_prompt="你是一个聊天助手，回答问题时请输出工具调用的过程，",
)

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
