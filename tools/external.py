import os
import base64
from config import JIRA_API_TOKEN, NOTION_API_KEY, JIRA_USER
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams, StdioServerParameters
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams 

def get_jira_mcp_tool():
    """Initializes the Jira MCP Tool server binding via npx STDIO."""
    # We must copy the user environment so npx has access to PATH and Node binaries
    token = f"{JIRA_USER}:{JIRA_API_TOKEN}"
    base64_token = base64.b64encode(token.encode()).decode()
    
    return MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url="https://mcp.atlassian.com/v1/mcp",
            headers={    
                "Authorization": f"Basic {base64_token}"
            },
            timeout=30.0,          
            sse_read_timeout=300.0
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
