# app.py
import streamlit as st
import html
from openai import OpenAI
from config import OPENAI_API_KEY, DEFAULT_OPENAI_CONFIG, SYSTEM_PROMPT
from utils import save_markdown_by_date

client = OpenAI(api_key=OPENAI_API_KEY)
st.set_page_config(page_title="ChatGPT Web", layout="wide")

# 💄 样式（无头像，自定义气泡 + ChatGPT 风格字体）
st.markdown("""
    <style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", "PingFang SC", "Microsoft YaHei", "Arial", sans-serif;
        background-color: #f7f7f8;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        padding: 20px 32px;
    }
    .chat-bubble {
        padding: 12px 18px;
        border-radius: 16px;
        margin: 6px 0;
        width: fit-content;
        max-width: 80%;
        font-size: 15px;
        line-height: 1.6;
        white-space: pre-wrap;
        word-break: break-word;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .user {
        background-color: #e5e5ea;
        align-self: flex-end;
        margin-left: auto;
        color: #000;
    }
    .assistant {
        background-color: #ffffff;
        align-self: flex-start;
        margin-right: auto;
        color: #000;
    }
    </style>
""", unsafe_allow_html=True)

# 初始化聊天记录
if "history" not in st.session_state:
    st.session_state.history = [{"role": "system", "content": SYSTEM_PROMPT}]

# 顶部标题和导出按钮
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("### ChatGPT Web 客户端")
with col2:
    if st.button("🗂 保存聊天记录"):
        path = save_markdown_by_date(st.session_state.history[1:])
        st.success(f"保存成功：{path}")

# 用户输入
user_input = st.chat_input("请输入你的问题...")

# ✅ 用户发言立即追加并刷新页面
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    st.rerun()

# ✅ 渲染所有消息（无 Streamlit 头像）
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.history[1:]:
    role = msg["role"]
    bubble_class = "user" if role == "user" else "assistant"
    safe_content = html.escape(msg["content"])
    st.markdown(
        f"<div class='chat-bubble {bubble_class}'>{safe_content}</div>",
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)

# ✅ 自动回复 GPT，追加后刷新
if len(st.session_state.history) >= 2 and st.session_state.history[-1]["role"] == "user":
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            messages=st.session_state.history,
            **DEFAULT_OPENAI_CONFIG
        )
        reply = response.choices[0].message.content
        st.session_state.history.append({"role": "assistant", "content": reply})
        st.rerun()