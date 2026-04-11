import os
from openai import OpenAI
from dotenv import load_dotenv
# Load environment variables from .env
load_dotenv()
# Read configuration
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")
MODEL = os.getenv("OPENAI_MODEL")
# Create client connection
client = OpenAI(
   api_key=API_KEY,
   base_url=BASE_URL
)