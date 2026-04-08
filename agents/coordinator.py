import uuid
from google.adk.agents import Agent
from agents.workers.jira import jira_analyst
from agents.workers.notion import notion_architect
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

# Primary Coordinator acts as the central router, utilizing sub-agents directly as callable tools
coordinator_agent = Agent(
    name="primary_coordinator",
    instruction="""You are the Primary Task Coordinator. 
    When an issue is received, use the jira_analyst sub-agent to fetch context. 
    Then, pass the analyzed context into the notion_architect sub-agent to generate a Notion page.
    Synthesize their responses and return the result.""",
    sub_agents=[
        jira_analyst,
        notion_architect
    ]
)

# Setup Session Service
APP_NAME = "nexus-agent-coordinator"
USER_ID = str(uuid.uuid4())
SESSION_ID = str(uuid.uuid4())

session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
# Setup Agent Runner
coordinator_runner = Runner(
    agent=coordinator_agent,
    app_name=APP_NAME,
    session_service=session_service,
)
