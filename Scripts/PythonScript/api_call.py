from openai import OpenAI
import sys
import json


# TODO: REMOVE api_key before committing!
client = OpenAI(api_key = "", base_url = "https://api.deepseek.com")

def process_text(input_text: str):
    prompt = f"""
Please split the following text into chapters.

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
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are an assistant that organizes study materials."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1024,
        temperature=0.7,
        stream=False, 
        response_format={"type": "json_object"}
    )
    content = response.choices[0].message.content
    return content

if __name__ == "__main__":
    # 从命令行读取文本
    input_text = sys.stdin.read()
    result = process_text(input_text)
    # 输出给 C#
    print(result)