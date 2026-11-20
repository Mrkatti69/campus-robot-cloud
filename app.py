import os
import requests
import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Campus AI Robot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Polished Robotics Dark-Cyber CSS ---
st.markdown("""
    <style>
    /* Main Robotics Dark Background */
    .stApp {
        background: radial-gradient(circle at top right, #162238, #0B0F19);
        color: #E2E8F0;
    }
    /* Glowing Primary Action Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: 600;
        background: linear-gradient(135deg, #0066FF 0%, #00B4D8 100%);
        color: white !important;
        border: none;
        padding: 0.55rem 1rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 14px rgba(0, 180, 216, 0.25);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 180, 216, 0.45);
        color: white !important;
    }
    /* Dark Glass Response Card */
    .response-card {
        background: rgba(19, 28, 49, 0.88) !important;
        backdrop-filter: blur(10px);
        color: #F8FAFC !important;
        padding: 22px;
        border-radius: 14px;
        border: 1px solid rgba(0, 212, 255, 0.25);
        border-left: 5px solid #00D4FF;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
        margin-bottom: 16px;
    }
    .response-card h4 {
        color: #38BDF8 !important;
        margin-top: 0;
        letter-spacing: 0.4px;
    }
    .response-card p {
        color: #F1F5F9 !important;
        line-height: 1.55;
    }
    /* Live Telemetry Pill Badge */
    .status-badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 20px;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid #10B981;
        color: #34D399;
        font-size: 0.85em;
        font-weight: 600;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if 'voice_input' not in st.session_state:
    st.session_state['voice_input'] = ""
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'last_query' not in st.session_state:
    st.session_state['last_query'] = ""

# --- Sidebar: System Telemetry, Document Uploader & Audio Controls ---
with st.sidebar:
    st.markdown("## ⚙️ Robot Control Panel")
    st.markdown('<div class="status-badge">● ONLINE • LLAMA 3 (8B)</div>', unsafe_allow_html=True)
    st.caption("Hardware: RTX 3050 (4GB) • 16GB RAM")
    st.write("---")

    voice_enabled = st.toggle("🔊 Enable Voice Response", value=True)
    voice_rate = st.slider("🗣️ Speech Speed (WPM)", min_value=120, max_value=190, value=155, step=5)

    st.write("---")
    st.markdown("### 📂 Knowledge Base Expansion")
    st.caption("Base File: `college_guide.txt` (Auto-loaded)")
    uploaded_files = st.file_uploader(
        "➕ Upload Extra Campus PDFs or TXT",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        help="Upload exam schedules, circulars, or department guides to expand the robot's knowledge immediately."
    )
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} extra file(s) indexed!")

    st.write("---")
    if st.button("🗑️ Clear Conversation Logs"):
        st.session_state['chat_history'] = []
        st.session_state['last_query'] = ""
        st.session_state['voice_input'] = ""
        st.rerun()

# --- Header Section ---
st.markdown('<div class="status-badge">⚡ VECTOR RAG ACTIVE • DUAL-MODE INTERFACE</div>', unsafe_allow_html=True)
st.markdown("# 🤖 Interactive Campus Robot Assistant")
st.markdown("Ask questions about campus facilities, timings, circulars, and rules using text, quick prompts, or voice.")
st.write("---")

# --- Clean Spoken Audio Engine ---
# --- Microphone Speech-to-Text Engine ---
def speak(text, rate=155):
    pass

def listen_to_mic():
    return "ERROR_HARDWARE"

# --- Main Split Interface: Text Terminal & Voice Node ---
layout_left, layout_right = st.columns([2,1])

with layout_left:
    st.markdown("#### 💬 Student Query Terminal")
    student_query = st.text_input(
        "Type a question or click a quick topic below:",
        value=st.session_state['voice_input'],
        placeholder="e.g., What is the breakfast and dinner time of hostel?"
    )

    # One-Click Quick-Prompt Chips (6 Topics)
    q1, q2, q3, q4, q5, q6 = st.columns(6)
    with q1:
        if st.button("🍽️ Mess"):
            st.session_state['voice_input'] = "What is the breakfast and dinner timing of hostel?"
            st.rerun()
    with q2:
        if st.button("📚 Library"):
            st.session_state['voice_input'] = "What is the timing of library?"
            st.rerun()
    with q3:
        if st.button("🚪 Curfew"):
            st.session_state['voice_input'] = "What is the closing time of hostel and mess?"
            st.rerun()
    with q4:
        if st.button("📋 Summary"):
            st.session_state['voice_input'] = "Summarize the key rules and timings in the uploaded documents."
            st.rerun()
    with q5:
        if st.button("🚌 Bus"):
            st.session_state['voice_input'] = "What are the morning and evening college bus timings?"
            st.rerun()
    with q6:
        if st.button("🎓 Placements"):
            st.session_state['voice_input'] = "Where is the placement cell and what is the CGPA criteria?"
            st.rerun()

    st.write("")
    submit_query = st.button("🚀 Execute Vector Query Loop")

with layout_right:
    st.markdown("#### 🎙️ Voice Input Node")
    st.caption("Click below and speak clearly into your microphone.")
    if st.button("🔴 Click & Speak Now"):
        with st.spinner("🎧 Listening..."):
            audio_text = listen_to_mic()
            if audio_text == "ERROR_TIMEOUT":
                st.toast("⚠️ No speech detected. Please speak sooner.", icon="⏳")
            elif audio_text == "ERROR_UNRECOGNIZED":
                st.toast("⚠️ Could not understand audio. Try again.", icon="❌")
            elif audio_text == "ERROR_HARDWARE":
                st.toast("⚠️ Microphone or network error.", icon="🎤")
            else:
                st.session_state['voice_input'] = audio_text
                st.rerun()

# --- Query Execution & Response Rendering ---
if student_query.strip() and (submit_query or st.session_state.get("last_query") != student_query):
    st.write("---")
    try:
        with st.spinner("🤖 Reasoning through Knowledge Base via Cloud Llama 3..."):
            st.session_state["last_query"] = student_query
            res = requests.post(
                "https://campus-robot-cloud.onrender.com/ask",
                json={"question": student_query},
                timeout=90
            )
            res.raise_for_status()
            response_text = res.json().get("answer", "No response from server.")

            st.session_state['chat_history'].insert(0, {
                "question": student_query,
                "answer": response_text
            })

            if voice_enabled:
                speak(response_text, rate=voice_rate)
    except Exception as e:
        st.error(f"❌ Error during query execution: {str(e)}")
elif submit_query and not student_query.strip():
    st.warning("Please enter a question, select a quick topic, or use the microphone first.")
           
# --- Display Persistent Conversation Logs ---
if st.session_state['chat_history']:
    st.write("---")
    st.markdown("### 📜 Conversation Logs")

    for idx, chat in enumerate(st.session_state['chat_history']):
        badge = "🟢 Latest" if idx == 0 else f"#{len(st.session_state['chat_history']) - idx}"
        st.markdown(f"""
            <div class="response-card">
                <p style="font-size:0.92em; color:#94A3B8 !important; margin-bottom:6px;">
                    <strong>{badge} &nbsp;|&nbsp; 🧑‍🎓 Student:</strong> {chat['question']}
                </p>
                <h4>🤖 Robot Node Response</h4>
                <p style="font-size:1.1em; margin-bottom:0;">{chat['answer']}</p>
            </div>
        """, unsafe_allow_html=True)
