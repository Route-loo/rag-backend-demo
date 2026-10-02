import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)


def generate_answer(query: str, context: str) -> str:
    prompt = f"""
    请基于下面给出的参考资料回答用户问题，如果资料里没有答案，就如实说「根据现有资料无法回答该问题」，不要编造内容。

    【参考资料】
    {context}

    【用户问题】
    {query}
    """
    response = client.chat.completions.create(
        model=os.getenv("LLM_MODEL"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content
