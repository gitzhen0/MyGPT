
* Personalized GPT, for Easy Markdown Export

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


