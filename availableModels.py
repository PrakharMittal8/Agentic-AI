# list_models.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # <-- loads .env into environment

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)

models = client.models.list()
for m in models.data:
    print(m.id)