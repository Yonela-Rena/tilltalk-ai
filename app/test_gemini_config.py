import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)

api_key = os.getenv("GEMINI_API_KEY")

print(f".env location: {ENV_FILE}")
print(f".env exists: {ENV_FILE.exists()}")

if api_key:
    print("Gemini API key loaded successfully.")
else:
    print("Gemini API key was not found.")