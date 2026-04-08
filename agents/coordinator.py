from google.adk.agents import Agent
from agents.workers.jira import jira_analyst
from agents.workers.notion import notion_architect

# Primary Coordinator acts as the central router, utilizing sub-agents directly as callable tools
coordinator_agent = Agent(
    name="primary_coordinator",
    instruction="""You are the Primary Task Coordinator. 
    When an issue is received, use the jira_analyst tool to fetch context. 
    Then, pass the analyzed context into the notion_architect tool to generate a Notion page.
    Synthesize their responses and return the result.""",
    tools=[
        jira_analyst,
        notion_architect
    ]
)
