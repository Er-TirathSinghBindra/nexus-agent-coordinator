from nexus_agent_coordinator.agents.coordinator import root_agent, APP_NAME
from google.adk.apps.app import App

app = App(
    name=APP_NAME,
    root_agent=root_agent,
)