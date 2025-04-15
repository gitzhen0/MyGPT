# app.py
import streamlit as st
import markdown
from openai import OpenAI
from config import OPENAI_API_KEY, DEFAULT_OPENAI_CONFIG, SYSTEM_PROMPT
from utils import save_markdown_by_date

client = OpenAI(api_key=OPENAI_API_KEY)
st.set_page_config(page_title="ChatGPT Web", layout="wide")

# 💄 样式：字体 + 气泡 + 代码块 + 消除气泡高度异常
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
    code, pre {
        background-color: #1e1e1e !important;
        color: #d4d4d4;
        padding: 10px;
        border-radius: 8px;
        font-family: Menlo, Consolas, monospace;
        font-size: 13px;
        overflow-x: auto;
        display: block;
    }
    /* 🧼 去除 p 的 margin 避免 bubble 空行 */
    .chat-bubble p,
    .chat-bubble h1,
    .chat-bubble h2,
    .chat-bubble h3,
    .chat-bubble h4,
    .chat-bubble ul,
    .chat-bubble ol {
        margin-top: 0.2em;
        margin-bottom: 0.2em;
    }
    .chat-bubble ol,
    .chat-bubble ul {
        padding-left: 1em;
        margin: 0;
    }
    .chat-bubble li {
        margin: 0.1em 0;
        padding: 0;
    }
    </style>
""", unsafe_allow_html=True)

# 🛠️ 修复 Markdown 标题不渲染的问题
def fix_markdown(content: str) -> str:
    if content.strip().startswith("#"):
        return "\n" + content
    return content

# ✅ 渲染聊天气泡（markdown 转 html 包在 bubble 中）
def render_bubble(role, content):
    bubble_class = "user" if role == "user" else "assistant"
    fixed = fix_markdown(content)
    md_html = markdown.markdown(fixed, extensions=["fenced_code", "codehilite"])
    html_block = f"<div class='chat-bubble {bubble_class}'>{md_html}</div>"
    st.markdown(html_block, unsafe_allow_html=True)

# 初始化聊天记录
if "history" not in st.session_state:
    st.session_state.history = [{"role": "system", "content": SYSTEM_PROMPT}]

# 顶部区域
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("### ChatGPT Web 客户端")
with col2:
    if st.button("🗂 保存聊天记录"):
        path = save_markdown_by_date(st.session_state.history[1:])
        st.success("保存成功")

# 用户输入
user_input = st.chat_input("请输入你的问题...")

# 用户消息立即显示
if user_input:
    st.session_state.history.append({"role": "user", "content": user_input})
    st.rerun()

# ✅ 渲染聊天记录（跳过 system）
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.history[1:]:
    role = msg.get("role")
    if role in ("user", "assistant"):
        render_bubble(role, msg.get("content", ""))
st.markdown("</div>", unsafe_allow_html=True)

# ✅ GPT 回复
if len(st.session_state.history) >= 2 and st.session_state.history[-1]["role"] == "user":
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            messages=st.session_state.history,
            **DEFAULT_OPENAI_CONFIG
        )
        reply = response.choices[0].message.content
        st.session_state.history.append({"role": "assistant", "content": reply})
        st.rerun()