# config.py

"""
Holds global configuration variables and helper methods
to load environment variables or default settings.
"""

import os
from dotenv import load_dotenv
load_dotenv()


DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/climb")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
