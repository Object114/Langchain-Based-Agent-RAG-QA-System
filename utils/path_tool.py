"""
提供统一的绝对路径
"""

import os

def get_project_root()->str:
    utils_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(utils_path)

def get_abs_path(relative_path:str) -> str:
    return os.path.join(get_project_root(), relative_path)
