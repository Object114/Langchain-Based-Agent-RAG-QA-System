from langchain.agents import create_agent
from utils.config_handler import agent_config
from model.factory import chat_model
from utils.prompt_loader import load_system_prompts
from agent.tools.agent_tools import rag_summarize, get_weather, get_user_location, get_user_id, get_current_month, fetch_user_data, fill_context_for_report
from agent.tools.middle_ware import tool_monitor, log_before_model, report_prompt_switch

class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompts(),
            tools=[rag_summarize, get_weather, get_user_location, get_user_id, get_current_month, fetch_user_data, fill_context_for_report],
            middleware=[tool_monitor, log_before_model, report_prompt_switch]        
        )

    def execute_stream(self, query: str):
        for chunk in self.agent.stream(
                                        {
                                            "messages":[
                                                {"role": "user", "content": query}
                                            ]
                                        },
                                        stream_mode="values",
                                        context={"report": False}
                                    ):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                yield latest_message.content.strip() + "\n"

if __name__ == '__main__':
    agent = ReactAgent()
    for chunk in agent.execute_stream("扫地机器人在我所在的城市和今天的天气下，应该如何保养？"):
        print(chunk, end="", flush=True)
