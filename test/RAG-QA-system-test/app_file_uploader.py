import streamlit
from knowledge_base import KnowledgeBaseService
import time

if "data_base_service" not in streamlit.session_state:
    streamlit.session_state["data_base_service"] = KnowledgeBaseService()

streamlit.title("Knowlege Data Upadate")
# 文件上传窗
upload_file = streamlit.file_uploader(
    "Upload TXT",
    type=['txt'],
    accept_multiple_files=False,
)

if upload_file is not None:
    file_name = upload_file.name
    file_type = upload_file.type
    file_size = upload_file.size / 1024
    streamlit.subheader(f'File Name: {file_name}')
    streamlit.write(f'File type: {file_type} ;   File Size: {file_size:.2f} KB')
    text = upload_file.getvalue().decode("utf-8")

    with streamlit.spinner("Loading..."):
        time.sleep(1)
        ret = streamlit.session_state["data_base_service"].upload_str(text, file_name)
        streamlit.write(ret)
