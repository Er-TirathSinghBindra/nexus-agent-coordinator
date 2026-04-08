from google.adk.agents import Agent
from tools.external import get_jira_mcp_tool
from config import DEFAULT_MODEL

jira_analyst = Agent(
    name="jira_analyst",
    model=DEFAULT_MODEL,
    instruction="You are a Jira task analyst. You pull ticket dimensions and classify them using the provided Jira MCP tool.",
    tools=[get_jira_mcp_tool()]  # Bound the active Jira MCP server capability
)
