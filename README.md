# Langchain-Based-Agent-RAG-QA-System
# 基于LangChain构建的 Agent + RAG 智能客服问答系统

---

一个融合 **Agent + RAG** 架构的智能问答系统的学习项目，能够基于知识库文档进行高质量问答，支持多工具调用以及自动报告生成。

## 项目结构
```
Langchain-Based-Agent-RAG-QA-System/
├── agent/
│ ├── react_agent.py # Agent核心逻辑
│ ├── tools/ # Agent可调用的工具定义
│ └── middleware.py # 中间件（用于流程控制、日志记录）
│
├── config/
│ ├── agent.yml # Agent配置
│ ├── chroma.yml # 向量数据库Chroma相关配置（路径、参数等）
│ ├── prompts.yml # Prompt配置（统一管理提示词路径）
│ └── rag.yml # RAG参数配置
│
├── data/ # 知识库数据目录（支持txt和pdf格式文件）
│
├── model/
│ └── factory.py # 模型工厂（统一创建 LLM 和 Embedding 实例）
│
├── prompts/
│ # Prompt 提示词模板目录（系统提示词 / RAG / 报告生成三种提示词）
│
├── rag/
│ ├── rag_service.py # RAG服务层（封装检索 + 生成的完整流程）
│ └── vector_store.py # 向量库构建与加载（文档切分 + embedding + 存储）
│
├── utils/
│ ├── config_handler.py # 配置文件加载工具
│ ├── file_handler.py # 文件读取与处理工具
│ ├── logger_handler.py # 日志管理工具
│ ├── path_tool.py # 路径处理工具
│ └── prompt_loader.py # 提示词加载工具
│
├── app.py # 项目主入口（启动可视化网页）
├── requirements.txt
└── README.md
```

## 使用流程
### 1. 安装依赖
```
pip install -r requirements.txt
```

### 2. 配置阿里云百炼平台api
```
export DASHSCOPE_API_KEY="your_api_key"
```

### 3. 将外部知识库文档放在`data/`目录下，目录中的文件转换为向量并存储到向量数据库：
```
python -m rag.vector_store
```

### 4. 启动可视化界面
```
streamlit run app.py
```

## 自定义配置文件
在`config/`下有四个yml文件，可以自定义使用的模型名字、数据库存储路径、RAG分片大小等配置。项目提供丰富的日志保存功能，运行后默认存放在`logs/`目录下。

## 🤝Tips:
本项目仅供学习和交流，希望能够对你有帮助
