# utils.py
import os
from datetime import datetime
from config import MARKDOWN_SAVE_PATH

def history_to_markdown(history):
    md = ""
    for msg in history:
        if msg["role"] == "user":
            md += "## 我\n" + msg["content"].strip() + "\n\n"
        elif msg["role"] == "assistant":
            md += "## ChatGPT\n" + msg["content"].strip() + "\n\n"
    return md

def save_markdown_by_date(history, base_path=MARKDOWN_SAVE_PATH):
    today = datetime.now().strftime("%Y-%-m-%-d")
    time_str = datetime.now().strftime("%H-%M-%S")

    dir_path = os.path.join(base_path, today)
    os.makedirs(dir_path, exist_ok=True)

    file_path = os.path.join(dir_path, f"chat_{time_str}.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(history_to_markdown(history))

    return file_path