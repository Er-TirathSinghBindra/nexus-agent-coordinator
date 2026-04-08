import os
from config import JIRA_API_TOKEN, NOTION_API_KEY
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, StdioServerParameters

def get_jira_mcp_tool():
    """Initializes the Jira MCP Tool server binding via npx STDIO."""
    # We must copy the user environment so npx has access to PATH and Node binaries
    env = os.environ.copy()
    env["JIRA_API_TOKEN"] = JIRA_API_TOKEN
    env["JIRA_DOMAIN"] = os.getenv("JIRA_DOMAIN", "mock.atlassian.net")
    env["JIRA_USER"] = os.getenv("JIRA_USER", "mock@example.com")
    
    return MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "@modelcontextprotocol/server-atlassian"],
                env=env
            ),
            timeout=30.0
        )
    )

def get_notion_mcp_tool():
    """
    Initializes the Notion MCP Tool server binding via npx STDIO.
    Uses headless open-source server for API token support.
    """
    env = os.environ.copy()
    env["NOTION_API_KEY"] = NOTION_API_KEY
    
    return MCPToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParameters(
                command="npx",
                args=["-y", "@modelcontextprotocol/server-notion"],
                env=env
            ),
            timeout=30.0
        )
    )
