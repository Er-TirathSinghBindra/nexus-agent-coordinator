from google.adk.agents import Agent
from tools.external import get_notion_mcp_tool

notion_architect = Agent(
    name="Notion Architect",
    instructions="You are a Notion architect. You format analyzed data into structured pages using the connected Notion MCP tool.",
    tools=[get_notion_mcp_tool()]  # Bound the active Notion MCP server capability
)
