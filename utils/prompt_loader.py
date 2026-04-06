"""
提示词加载工具
"""

from utils.config_handler import prompt_config
from utils.path_tool import get_abs_path
from utils.logger_handler import logger

def load_system_prompts():
    try:
        system_prompt_path = get_abs_path(prompt_config["main_prompt_path"])
    except KeyError as e:
        logger.error(f"prompt.yml中没有配置项main_prompt_path")
        raise e
    
    try:
        return open(system_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"系统提示词解析出错.{str(e)}")
        raise e
    
def load_rag_prompts():
    try:
        rag_prompt_path = get_abs_path(prompt_config["rag_summarize_prompt_path"])
    except KeyError as e:
        logger.error(f"prompt.yml中没有配置项rag_summarize_prompt_path")
        raise e
    
    try:
        return open(rag_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"rag总结提示词解析出错.{str(e)}")
        raise e
    
def load_report_prompts():
    try:
        report_prompt_path = get_abs_path(prompt_config["report_prompt_path"])
    except KeyError as e:
        logger.error(f"prompt.yml中没有配置项report_prompt_path")
        raise e
    
    try:
        return open(report_prompt_path, "r", encoding="utf-8").read()
    except Exception as e:
        logger.error(f"报告提示词解析出错.{str(e)}")
        raise e
    
if __name__ == '__main__':
    print(load_report_prompts())