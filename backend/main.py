from fastapi import FastAPI
from pydantic import BaseModel
from ollama_client import generate_answer
from knowledge_base import add_document, query_context
import uvicorn

app = FastAPI(title="Salon AI Receptionist", version="1.2")

pending_requests = {}
resolved_requests = {}
user_updates = {}  
request_counter = 1


class QueryRequest(BaseModel):
    user_id: str
    message: str


class SupervisorResponse(BaseModel):
    request_id: int
    answer: str


@app.post("/query")
def handle_query(req: QueryRequest):
    global request_counter, pending_requests, resolved_requests, user_updates

    user_query = req.message

    if req.user_id in user_updates:
        update = user_updates.pop(req.user_id)
        return {
            "status": "resolved_from_supervisor",
            "message": "Supervisor provided a final answer.",
            "answer": update["answer"],
        }

    ai_answer = generate_answer(user_query)

    unsure_keywords = ["supervisor", "manager", "confirm with", "ask my boss", "check with"]
    if any(keyword in ai_answer.lower() for keyword in unsure_keywords):
        pending_requests[request_counter] = {
            "user_id": req.user_id,
            "question": user_query,
            "status": "pending",
        }
        request_counter += 1
        return {
            "status": "escalated",
            "message": "🤖 I'm not sure — I’ll confirm with my supervisor.",
        }

    return {"status": "answered", "answer": ai_answer}


@app.post("/supervisor/respond")
def supervisor_respond(res: SupervisorResponse):
    """Supervisor provides an answer; it's refined via LLM and stored for user delivery."""
    global pending_requests, user_updates

    req_id = res.request_id
    if req_id not in pending_requests:
        return {"error": "Invalid request ID."}

    pending = pending_requests[req_id]
    user_id = pending["user_id"]
    pending["status"] = "resolved"
    pending["raw_answer"] = res.answer

    refinement_prompt = f"""
    Refine the following supervisor's response into a professional, friendly, and natural salon chatbot message.

    Question: {pending['question']}
    Supervisor's Answer: {res.answer}

    Return only the polished response.
    """
    refined_answer = generate_answer(refinement_prompt).strip()


    pending["answer"] = refined_answer


    add_document(f"Q: {pending['question']} A: {refined_answer}")

    user_updates[user_id] = {
        "status": "resolved_from_supervisor",
        "question": pending["question"],
        "answer": refined_answer,
    }

    return {
        "status": "updated",
        "message": "Refined answer added to knowledge base and queued for client.",
        "refined_answer": refined_answer,
    }


@app.get("/check_updates/{user_id}")
def check_updates(user_id: str):
    """Client polls this endpoint to receive supervisor’s refined reply."""
    global user_updates

    if user_id in user_updates:
        update = user_updates.pop(user_id)
        return update

    return {"status": "no_update"}


@app.get("/pending")
def view_pending():
    return {
        k: v for k, v in pending_requests.items() if v.get("status") == "pending"
    }


@app.delete("/pending/{request_id}")
def delete_pending(request_id: int):
    global pending_requests

    if request_id not in pending_requests:
        return {"error": "Request not found."}

    del pending_requests[request_id]
    return {"status": "deleted", "message": f"Request {request_id} deleted successfully."}


@app.get("/knowledge")
def view_knowledge():
    return query_context("salon")


@app.post("/refine")
def refine_text(req: dict):
    prompt = req.get("prompt", "")
    refined = generate_answer(
        f"Polish this text for a friendly salon receptionist chatbot:\n\n{prompt}"
    )
    return {"refined_answer": refined.strip()}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

