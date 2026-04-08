import logging
from fastapi import FastAPI, BackgroundTasks, HTTPException
from core.schemas import JiraWebhookPayload, TaskRequest
from core.firestore import check_if_processed, mark_ticket_processed

from google.genai import types
from agents.coordinator import coordinator_runner, USER_ID, SESSION_ID

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
        new_message = types.Content(role='user', parts=[types.Part(text=session_prompt)])

        events = coordinator_runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=new_message)
        for event in events:
            print(f"\nDEBUG EVENT: {event}\n")
            if event.is_final_response() and event.content:
                final_answer = event.content.parts[0].text.strip()
                print("\n🟢 FINAL ANSWER\n", final_answer, "\n")
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
        new_message = types.Content(role='user', parts=[types.Part(text=payload.prompt)])

        events = coordinator_runner.run(user_id=USER_ID, session_id=SESSION_ID,new_message=new_message)
        for event in events:
            print(f"\nDEBUG EVENT: {event}\n")
            if event.is_final_response() and event.content:
                final_answer = event.content.parts[0].text.strip()
                print("\n🟢 FINAL ANSWER\n", final_answer, "\n")
        return {"result": final_answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
