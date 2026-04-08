from typing import Optional
from pydantic import BaseModel, Field

class JiraWebhookPayload(BaseModel):
    issue_id: str
    issue_key: str
    webhookEvent: str
    summary: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

class TaskRequest(BaseModel):
    prompt: str
