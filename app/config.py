import os
from dotenv import load_dotenv

load_dotenv()

class ConfigurationError(Exception):
    pass


def validate_config():
    required_keys = ["GROQ_API_KEY", "TAVILY_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        raise ConfigurationError(f"Missing required environment variables: {', '.join(missing_keys)}")


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")