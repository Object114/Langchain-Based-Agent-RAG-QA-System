import streamlit
from agent.React_agent import ReactAgent
import time

streamlit.title("扫地机器人-智能客服")
streamlit.divider()

if "agent" not in streamlit.session_state:
    streamlit.session_state["agent"] = ReactAgent()

if "messages" not in streamlit.session_state:
    streamlit.session_state["messages"] = [{"role":"assistant", "content":"你好，请问有什么可以帮到你的？"}]

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
        answer_stream = streamlit.session_state["agent"].execute_stream(user_message)
        # 将流式输出片段捕捉到列表中缓存起来
        def capture(generator, cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                for char in chunk:
                    time.sleep(0.01)
                    yield char
        streamlit.chat_message("assistant").write_stream(capture(answer_stream, assistant_message))

        # 添加历史消息记录
        streamlit.session_state["messages"].append({
            "role":"assistant",
            "content":assistant_message[-1]
        })
        streamlit.rerun()
