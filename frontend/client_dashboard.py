import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh
import os

# Allows working both in docker-compose & locally
# BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8501")
BACKEND_URL = os.getenv("BACKEND_URL", "http://192.168.49.2:30799")



st.set_page_config(page_title="Salon AI Assistant 💇‍♀️", page_icon="💬")
st.title("💇‍♀️ Salon AI Receptionist Chat")

# --- Session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_id" not in st.session_state:
    st.session_state.user_id = "user_001"
user_id = st.session_state.user_id

# --- Auto-refresh every 5 seconds ---
st_autorefresh(interval=20000, key="client_refresh")

# --- Check for supervisor updates ---
try:
    check_resp = requests.get(f"{BACKEND_URL}/check_updates/{user_id}")
    if check_resp.status_code == 200:
        data = check_resp.json()
        if data.get("status") == "resolved_from_supervisor":
            ai_reply = f"✅ Supervisor confirmed: {data['answer']}"
            if ("assistant", ai_reply) not in st.session_state.chat_history:
                st.session_state.chat_history.append(("assistant", ai_reply))
except Exception as e:
    st.warning(f"⚠️ Could not check for updates: {e}")

# --- User chat input ---
user_input = st.chat_input("Ask me anything about the salon...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    payload = {"user_id": user_id, "message": user_input}

    try:
        response = requests.post(f"{BACKEND_URL}/query", json=payload)
        data = response.json()

        if data["status"] == "answered":
            ai_reply = data["answer"]
        elif data["status"] == "escalated":
            ai_reply = "🤖 I’m not sure. I’ll confirm with my supervisor."
        elif data["status"] == "resolved_from_supervisor":
            ai_reply = f"✅ Supervisor confirmed: {data['answer']}"
        else:
            ai_reply = "⚠️ Unexpected response."
    except Exception as e:
        ai_reply = f"❌ Error: {e}"

    ai_reply = ai_reply.replace("\\n", "\n").strip()
    st.session_state.chat_history.append(("assistant", ai_reply))

# --- Display chat history ---
for role, msg in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("user"):
            st.markdown(msg)
    else:
        with st.chat_message("assistant"):
            st.markdown(
                f"""
                <div style='background-color:#262730; padding:12px; border-radius:10px; color:white; line-height:1.6;'>
                    {msg.replace('\n', '<br>')}
                </div>
                """,
                unsafe_allow_html=True,
            )
