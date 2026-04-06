import streamlit
from rag import RagService
import json

try:
    with open("config.json", 'r', encoding="utf-8") as f:
        config = json.load(f)
except: FileExistsError

streamlit.title("智能客服")
streamlit.divider()

if "messages" not in streamlit.session_state:
    streamlit.session_state["messages"] = [{"role":"assistant", "content":"你好，请问有什么可以帮到你的？"}]

if "RagService" not in streamlit.session_state:
    streamlit.session_state["RagService"] = RagService()

for message in streamlit.session_state["messages"]:
    streamlit.chat_message(message["role"]).write(message["content"])

user_message = streamlit.chat_input()

if user_message is not None:
    streamlit.chat_message("user").write(user_message)
    # 添加历史消息记录
    streamlit.session_state["messages"].append({
        "role":"user",
        "content":user_message
    })
    
    assistant_message = []
    with streamlit.spinner("思考中......"):
        answer_stream = streamlit.session_state["RagService"].chain.stream(
            {"input":user_message},
            config["session_config"]
        )
        # 将流式输出片段捕捉到列表中缓存起来
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk
        streamlit.chat_message("assistant").write_stream(capture(answer_stream, assistant_message))

        # 添加历史消息记录
        streamlit.session_state["messages"].append({
            "role":"assistant",
            "content":"".join(assistant_message)
        })
