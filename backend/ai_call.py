from openai import OpenAI
import sys
import json
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY", "")
base_url = os.getenv("BASE_URL", "https://api.deepseek.com")

client = OpenAI(api_key=api_key, base_url=base_url)


def build_prompt(input_text: str) -> str:
    prompt = f"""
Please split the following text into chapters.
You can rearrange the format and/or add explanations if needed.

For each chapter provide:
- Title
- Detailed Content

Return in JSON format like:

[
  {{
    "Title": "...",
    "Content": "..."
  }}
]

Text:
{input_text}
"""
    return prompt


def process_text(prompt: str) -> str | None:
    response = client.chat.completions.create(
        model="deepseek-reasoner",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that organizes study materials.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=64000,
        temperature=0.7,
        stream=False,
        response_format={"type": "json_object"},
    )
    result = response.choices[0].message.content
    return result


if __name__ == "__main__":
    input_text = sys.stdin.read()
    result = process_text(build_prompt(input_text))
    print(result)
