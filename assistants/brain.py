"""
GPT wrapper – always answers in Hebrew.
"""

import openai

class AssistantBrain:
    def __init__(self, api_key: str):
        openai.api_key = api_key

    def chat(self, prompt: str) -> str:
        res = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "אתה עוזר אישי שעונה תמיד בעברית תקנית."},
                {"role": "user", "content": prompt},
            ],
        )
        return res.choices[0].message.content.strip()
