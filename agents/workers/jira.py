from google.adk.agents import Agent
from tools.external import get_jira_mcp_tool

jira_analyst = Agent(
    name="jira_analyst",
    instruction="You are a Jira task analyst. You pull ticket dimensions and classify them using the provided Jira MCP tool.",
    tools=[get_jira_mcp_tool()]  # Bound the active Jira MCP server capability
)
