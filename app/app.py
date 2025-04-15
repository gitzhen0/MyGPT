# app.py
import streamlit as st
from openai import OpenAI
from config import OPENAI_API_KEY, DEFAULT_OPENAI_CONFIG, SYSTEM_PROMPT
from utils import save_markdown_by_date

# 初始化 OpenAI 客户端
client = OpenAI(api_key=OPENAI_API_KEY)

# 页面配置
st.set_page_config(page_title="ChatGPT Web", layout="wide")

# 初始化聊天记录
if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# 顶部区域：标题 + 保存按钮
col1, col2 = st.columns([5, 1])
with col1:
    st.title("💬 ChatGPT Web 客户端")
with col2:
    if st.button("🗂 保存聊天记录到桌面"):
        saved_path = save_markdown_by_date(st.session_state.history[1:])  # 跳过 system
        st.success(f"保存成功：{saved_path}")

# 用户输入
user_input = st.chat_input("请输入你的问题...")

if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    with st.spinner("正在思考..."):
        response = client.chat.completions.create(
            messages=st.session_state.history,
            **DEFAULT_OPENAI_CONFIG
        )
        reply = response.choices[0].message.content
        st.session_state.history.append({"role": "assistant", "content": reply})

# 显示聊天记录
for msg in st.session_state.history[1:]:  # 跳过 system
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])