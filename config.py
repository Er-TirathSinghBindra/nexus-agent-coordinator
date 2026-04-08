import os
from dotenv import load_dotenv

# Optionally load .env payload here
load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")

# MCP Configurations
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "mock_jira_token")
JIRA_USER = os.getenv("JIRA_USER", "mock_user_email")
NOTION_API_KEY = os.getenv("NOTION_API_KEY", "mock_notion_key")

DEFAULT_MODEL = os.getenv("MODEL", "gemini-2.5-flash")
