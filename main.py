import uuid
import logging
from fastapi import FastAPI, BackgroundTasks, HTTPException
from core.schemas import JiraWebhookPayload, TaskRequest
from core.firestore import check_if_processed, mark_ticket_processed

from google.genai import types
from agents.coordinator import coordinator_runner, session_service, APP_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------
# FastAPI App & Endpoints
# ---------------------------------------------------------
app = FastAPI(title="Google-ADK Task Management API")

async def process_jira_runner(payload: JiraWebhookPayload):
    """
    Background worker executing the ADK Runner session asynchronously.
    """
    try:
        logger.info(f"Background ADK Runner Session started for {payload.issue_key}")
        
        # 1. Create a unique session per webhook execution
        user_id = "system_webhook"
        session_id = f"{payload.issue_key}_{uuid.uuid4().hex[:8]}"
        await session_service.create_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
        
        # 2. Build model prompt
        session_prompt = f"Process Jira Ticket: {payload.issue_key}. Event: {payload.webhookEvent}"
        new_message = types.Content(role='user', parts=[types.Part(text=session_prompt)])

        # 3. Stream Async Events
        final_answer = ""
        async for event in coordinator_runner.run_async(user_id=user_id, session_id=session_id, new_message=new_message):
            if event.is_final_response() and event.content:
                final_answer = event.content.parts[0].text.strip()
                logger.info(f"\n🟢 FINAL ANSWER\n{final_answer}\n")
                
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
    return {"message": "Ticket accepted and ADK async runner started", "status": "processing"}

@app.post("/api/agent/task")
async def agent_task(payload: TaskRequest):
    """Synchronous Task Endpoint."""
    try:
        user_id = "api_user"
        session_id = f"task_{uuid.uuid4().hex[:8]}"
        await session_service.create_session(app_name=APP_NAME, user_id=user_id, session_id=session_id)
        
        new_message = types.Content(role='user', parts=[types.Part(text=payload.prompt)])

        final_answer = ""
        async for event in coordinator_runner.run_async(user_id=user_id, session_id=session_id, new_message=new_message):
            if event.is_final_response() and event.content:
                final_answer = event.content.parts[0].text.strip()
                
        return {"result": final_answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
