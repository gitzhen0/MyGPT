## Intro

* Personalized GPT, for Easy Markdown Export

### Problem List
* 无法上网
* 无法图片
* token 记忆问题, 无法总结
  * 如果我用网页版 gpt, 一次聊天, 虽然 token 上线就那么高, 但似乎, gpt 能总提炼总结, 但我现在这个的话, 他似乎只是机械的把聊天记录发回给 api, 一旦聊天记录超过 token 上线, 是不是就....

### Sample config.py

* put under MyGPT/app

```config.py
OPENAI_API_KEY = ""

DEFAULT_OPENAI_CONFIG = {
    "model": "gpt-4.1",
    "temperature": 1.0,
    "max_tokens": 6000,
    # "top_p": 1.0,
    # "presence_penalty": 1.0,
    # "frequency_penalty": 0.3,
    # "stop": ["你：", "ChatGPT："],  # 可选
    # "logit_bias": {},
    # "user": "my_app_user_123"     # 可选
}

MARKDOWN_SAVE_PATH = "/Users/Bob/Desktop"

SYSTEM_PROMPT = ""

```


