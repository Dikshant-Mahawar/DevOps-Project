import streamlit as st
import requests
from streamlit_autorefresh import st_autorefresh

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Supervisor Dashboard", layout="wide")
st.title("💼 Salon AI Supervisor Dashboard")

# Auto-refresh every 20 seconds
st_autorefresh(interval=20000, key="supervisor_refresh")

# --- View Pending Requests ---
st.header("🕐 Pending Help Requests")

try:
    resp = requests.get(f"{API_URL}/pending")
    pending = resp.json()
except Exception as e:
    st.error(f"⚠️ Could not fetch pending requests: {e}")
    st.stop()

if not pending:
    st.success("✅ No pending requests.")
else:
    if isinstance(pending, dict):
        pending_items = pending.items()
    elif isinstance(pending, list):
        pending_items = enumerate(pending, start=1)
    else:
        pending_items = []

    for req_id, req in pending_items:
        with st.container():
            st.subheader(f"🟡 Request #{req_id}")
            st.write(f"👤 **User ID:** {req.get('user_id', 'N/A')}")
            st.write(f"💬 **Question:** {req.get('question', 'N/A')}")

            answer = st.text_area(f"✍️ Your Answer for Request #{req_id}", key=f"answer_{req_id}")

            col1, col2, col3 = st.columns([1, 1, 1])

            # ✨ Preview LLM refinement
            with col1:
                if st.button(f"✨ Preview Refined #{req_id}", key=f"preview_{req_id}"):
                    if not answer.strip():
                        st.warning("Please write an answer first.")
                    else:
                        try:
                            refine_payload = {
                                "prompt": f"Refine this for a polite, concise, and professional salon assistant reply:\n\n{answer}"
                            }
                            refine_resp = requests.post(f"{API_URL}/refine", json=refine_payload)
                            if refine_resp.status_code == 200:
                                refined = refine_resp.json().get("refined_answer", "").strip()
                                st.session_state[f"refined_{req_id}"] = refined
                                st.markdown(
                                    f"""
                                    <div style='background-color:#262730; padding:12px; border-radius:10px; color:white; line-height:1.6;'>
                                        {refined.replace('\n', '<br>')}
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                            else:
                                st.error("Refinement failed.")
                        except Exception as e:
                            st.error(f"Error refining answer: {e}")

            # ✅ Submit answer (refined version if available)
            with col2:
                if st.button(f"✅ Submit Answer #{req_id}", key=f"submit_{req_id}"):
                    final_answer = st.session_state.get(f"refined_{req_id}", answer)
                    if not final_answer.strip():
                        st.warning("Please provide or preview an answer first.")
                    else:
                        res = requests.post(
                            f"{API_URL}/supervisor/respond",
                            json={"request_id": int(req_id), "answer": final_answer},
                        )
                        if res.status_code == 200:
                            st.success("💾 Answer submitted, refined, and knowledge base updated!")
                            st.balloons()
                        else:
                            st.error(f"⚠️ Failed to submit: {res.text}")

            # 🗑️ Delete request
            with col3:
                if st.button(f"🗑️ Delete Request #{req_id}", key=f"delete_{req_id}"):
                    del_res = requests.delete(f"{API_URL}/delete_request/{req_id}")
                    if del_res.status_code == 200:
                        st.warning(f"🗑️ Request #{req_id} deleted.")
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete request.")

# --- Knowledge Base Preview ---
st.header("📘 Knowledge Base Preview")

try:
    kb_resp = requests.get(f"{API_URL}/knowledge")
    if kb_resp.status_code == 200:
        kb_entries = kb_resp.json()
        if kb_entries:
            for entry in kb_entries:
                st.markdown(f"- {entry}")
        else:
            st.info("No entries found in the knowledge base.")
    else:
        st.error("⚠️ Could not fetch knowledge base.")
except Exception as e:
    st.error(f"Error fetching KB: {e}")
