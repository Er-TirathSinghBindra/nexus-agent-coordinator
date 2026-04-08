import logging
from google.cloud import firestore

logger = logging.getLogger(__name__)

try:
    db = firestore.Client()
except Exception as e:
    logger.warning(f"Could not initialize Firestore Client: {e}")
    db = None

def check_if_processed(ticket_id: str) -> bool:
    """Checks if a ticket_id exists in the database to prevent infinite loops."""
    if not db:
        logger.warning("Firestore client not initialized, skipping check.")
        return False
    doc_ref = db.collection('processed_jira_tickets').document(ticket_id)
    return doc_ref.get().exists

def mark_ticket_processed(ticket_id: str, status: str):
    """Marks ticket_id workflow execution bounded status."""
    if not db:
        return
    doc_ref = db.collection('processed_jira_tickets').document(ticket_id)
    doc_ref.set({
        'processed_at': firestore.SERVER_TIMESTAMP,
        'status': status
    })
