import os
from config import JIRA_API_TOKEN, NOTION_API_KEY

# Assuming standard google-adk tools implementation for MCP
try:
    from google.adk.tools import McpTool
except ImportError:
    # Safe mock definition matching expected ADK kwargs if the library version varies
    class McpTool:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

def get_jira_mcp_tool():
    """Initializes the Jira MCP Tool server binding."""
    return McpTool(
        name="Jira_MCP_Server",
        # We specify standard NodeJS MCP execution via typical npx commands
        server_command="npx",
        server_args=["-y", "@modelcontextprotocol/server-atlassian"],
        # Provide securely isolated config keys
        env={
            "JIRA_API_TOKEN": JIRA_API_TOKEN,
            "JIRA_DOMAIN": os.getenv("JIRA_DOMAIN", "mock.atlassian.net"),
            "JIRA_USER": os.getenv("JIRA_USER", "mock@example.com")
        }
    )

def get_notion_mcp_tool():
    """
    Initializes the Notion MCP Tool server binding.
    As per Notion docs, the hosted https://mcp.notion.com/mcp requires human-in-the-loop OAuth.
    For our headless Cloud Run background worker, we must use the open-source server 
    that supports the NOTION_API_KEY bearer token.
    """
    return McpTool(
        name="Notion_MCP_Server",
        # Using the headless open-source notion MCP for API token support
        server_command="npx",
        server_args=["-y", "@modelcontextprotocol/server-notion"],
        env={
            "NOTION_API_KEY": NOTION_API_KEY
        }
    )
