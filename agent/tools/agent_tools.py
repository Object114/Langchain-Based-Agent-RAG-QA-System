"""
agent使用的工具
"""
from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService
import os, csv, random
from utils.config_handler import agent_config
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

rag = RagSummarizeService()
user_data = {}

@tool(description="从向量数据库中检索参考资料并总结")
def rag_summarize(query: str) -> str:
    return rag.retrieve_and_summarize(query)

@tool(description="获取指定城市的天气，并以字符串形式返回")
def get_weather(city: str) -> str:
    return f"城市{city}天气位晴天，气温26度"

@tool(description="获取当前用户所在城市的名称，以字符串形式返回")
def get_user_location() -> str:
    return random.choice(["北京", "上海", "广州"])

@tool(description="获取当前月份，并以字符串形式返回")
def get_current_month() -> str:
    return random.choice(["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
             "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12", ])

@tool(description="获取用户的ID，以字符串形式返回")
def get_user_id() -> str:
    return random.choice(["1001", "1002", "1003", "1004", "1005", "1006", "1007", "1008", "1009", "1010"])

def generate_user_data():
    if not user_data:
        data_path = get_abs_path(agent_config["user_data_path"])
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"用户数据文件{data_path}不存在")
        with open(data_path, 'r', encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                arr = line.strip().split(",")
                user_id = arr[0].replace('"', "")
                feature = arr[1].replace('"', "")
                efficiency = arr[2].replace('"', "")
                consumble = arr[3].replace('"', "")
                comparison = arr[4].replace('"', "")
                time = arr[5].replace('"', "")

                if user_id not in user_data:
                    user_data[user_id] = {}
                user_data[user_id][time] = {
                    "feature": feature,
                    "efficiency": efficiency,
                    "consumble": consumble,
                    "comparison": comparison
                }

@tool(description="从外部系统中获取指定用户在指定月份中的使用记录，以字符串形式返回")
def fetch_user_data(user_id: str, time: str) -> str:
    generate_user_data()
    try:
        return user_data[user_id][time]
    except KeyError:
        logger.warning(f"[fetch_user_data]未能检索到指定用户数据: ID:{user_id} 时间:{time}")
        return ""
    
@tool(description="调用后触发中间件，自动为报告生成的场景切换上下文信息")
def fill_context_for_report():
    return "fill_context_for_report()已调用"
