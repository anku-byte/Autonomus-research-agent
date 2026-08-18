from openai import OpenAI  # type: ignore[reportMissingImports]
from app.config import GROQ_API_KEY, GROQ_MODEL

# Groq provides an OpenAI-compatible client endpoint
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

def get_completion(prompt: str, model: str = GROQ_MODEL) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful research assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content