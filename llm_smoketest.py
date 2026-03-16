from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
assert api_key, "OPENAI_API_KEY is not set"

client = OpenAI(api_key=api_key)

resp = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "Say 'hello from ops triage agent' in one short sentence."}],
)

print(resp.choices[0].message.content)
