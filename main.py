import logging
from fastapi import FastAPI, BackgroundTasks, HTTPException
from core.schemas import JiraWebhookPayload, TaskRequest
from core.firestore import check_if_processed, mark_ticket_processed
from agents.coordinator import coordinator_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# FastAPI App & Endpoints
# ---------------------------------------------------------
app = FastAPI(title="Google-ADK Task Management API")

def process_jira_runner(payload: JiraWebhookPayload):
    """
    Background worker executing the ADK Runner session.
    """
    try:
        logger.info(f"Background ADK Runner Session started for {payload.issue_key}")
        
        session_prompt = f"Process Jira Ticket: {payload.issue_key}. Event: {payload.webhookEvent}"
        response = coordinator_agent.invoke(session_prompt)
        
        logger.info(f"ADK runner session finished for {payload.issue_key}.")
        mark_ticket_processed(payload.issue_key, "completed")
        
    except Exception as e:
        logger.error(f"ADK Runner Session failed for {payload.issue_key}: {e}", exc_info=True)
        mark_ticket_processed(payload.issue_key, "failed")

@app.post("/api/webhooks/jira")
async def jira_webhook(payload: JiraWebhookPayload, background_tasks: BackgroundTasks):
    """Webhook Endpoint returning 200 OK immediately."""
    if check_if_processed(payload.issue_key):
        logger.info(f"Ticket {payload.issue_key} already processed. Skipping workflow.")
        return {"message": "Ticket already processed", "status": "skipped"}
    
    background_tasks.add_task(process_jira_runner, payload)
    return {"message": "Ticket accepted and ADK runner started", "status": "processing"}

@app.post("/api/agent/task")
async def agent_task(payload: TaskRequest):
    """Synchronous Task Endpoint."""
    try:
        response = coordinator_agent.invoke(payload.prompt)
        return {"result": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
