import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

r = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "List 6 comma-separated keywords for how people use the clown face emoji. Output only the list."}],
    temperature=0.7,
    max_tokens=200,
)

print(r.choices[0].message)
print("\nfinish_reason:", r.choices[0].finish_reason)
print("usage:", r.usage)