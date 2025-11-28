from tinydb import TinyDB, Query

db = TinyDB("./data/help_requests.json")

def add_help_request(user_id, question):
    """Add a new pending help request."""
    req_id = len(db) + 1
    db.insert({
        "id": req_id,
        "user_id": user_id,
        "question": question,
        "status": "pending",
        "answer": None
    })
    return req_id

def update_help_request(req_id, answer):
    """Mark request as resolved and save answer."""
    Request = Query()
    db.update({"status": "resolved", "answer": answer}, Request.id == req_id)

def get_pending():
    """Return all pending help requests."""
    Request = Query()
    return db.search(Request.status == "pending")

def get_all():
    """Return all requests (resolved + pending)."""
    return db.all()
