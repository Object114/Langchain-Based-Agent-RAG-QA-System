from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from typing import Callable
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from langchain.agents import AgentState
from langgraph.runtime import Runtime
from utils.logger_handler import logger
from utils.prompt_loader import load_system_prompts, load_report_prompts

@wrap_tool_call
def tool_monitor(
    request: ToolCallRequest,
    handler: Callable[[ToolCallRequest], ToolMessage | Command],
) -> ToolMessage | Command:
    logger.info(f"[工具调用] 执行工具: {request.tool_call['name']}  传入参数: {request.tool_call['args']}")
    try:
        res = handler(request)
        logger.info(f"[工具调用] {request.tool_call['name']}调用成功")
        # report提示词切换转换
        if request.tool_call['name'] == "fill_context_for_report":
            request.runtime.context["report"] = True
        return res
    except Exception as e:
        logger.error(f"[工具调用] {request.tool_call['name']}调用失败，返回{str(e)}")
        raise e

@before_model
def log_before_model(
    state: AgentState,
    runtime: Runtime
):
    logger.info(f"[before model]即将调用模型， 带有{len(state['messages'])}条消息")
    logger.debug(f"[before model] {type(state['messages'][-1]).__name__}>>{state['messages'][-1].content.strip()}")
    return None

@dynamic_prompt # 在调用提示词模板之前会被调用
def report_prompt_switch(
    request: ModelRequest
):
    is_report = request.runtime.context.get("report", False)
    if is_report:
        return load_report_prompts()
    else:
        return load_system_prompts()
    