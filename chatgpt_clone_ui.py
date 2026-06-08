import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ChatGPT ",
    page_icon="🤖",
    layout="wide"
)

# ==================================================
# SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "timeline" not in st.session_state:
    st.session_state.timeline = []

# ==================================================
# CALCULATED ANALYTICS
# ==================================================

tokens_used = sum(
    len(msg["content"].split())
    for msg in st.session_state.messages
)

chat_depth = len(st.session_state.messages)

confidence = min(75 + chat_depth, 99)

productivity = min(60 + chat_depth * 2, 100)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.block-container{
    padding-top:1.5rem;
    padding-bottom:0rem;
    padding-left:1rem;
    padding-right:1rem;
}

.stApp{
    background:linear-gradient(
        135deg,
        #0B1020,
        #111827,
        #0F172A
    );
}

[data-testid="stSidebar"]{
    background:#0F172A;
}

.stButton > button{
    width:100%;
    height:52px;
    border-radius:12px;
    background:#1E293B;
    color:white;
    border:none;
}

.stButton > button:hover{
    background:#2563EB;
}

.metric-card{
    background:#1E293B;
    padding:8px;
    border-radius:12px;
    text-align:center;
}

.chat-title{
    text-align:center;
    font-size:42px;
    font-weight:bold;
    margin-bottom:0px;
}

.chat-subtitle{
    text-align:center;
    color:#94A3B8;
    margin-top:0px;
    margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)
# ==================================================
# LAYOUT
# ==================================================

left, center, right = st.columns([1.2,6,1.5])

# ==================================================
# LEFT PANEL
# ==================================================


with left:

    st.markdown("##  ChatGPT ")

    st.button("➕ New Chat", key="new_chat")

    st.text_input(
        "Search",
        placeholder="🔍 Search Chats",
        label_visibility="collapsed"
    )

    st.divider()

    menu_items = [
        "📚 Library",
        "📁 Projects",
        "⚡ Apps",
        "💻 Codex",
        "🖼 Images"
    ]

    for item in menu_items:
        st.markdown(item)

    st.divider()

    st.markdown("### 📅 Recent")

    if len(st.session_state.timeline) == 0:
        st.caption("No chats yet")
    else:
        for chat in st.session_state.timeline[-2:]:
            st.caption(f"🕒 {chat}")

    st.divider()

    st.button("⚙ Settings", key="settings")    
with center:

    st.markdown("""
    <div class='chat-title'>
     ChatGPT 
    </div>

    <div class='chat-subtitle'>
    Your AI Workspace
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.button("🧠 Explain ML", key="ml")
        st.button("📄 Summarize PDF", key="pdf")

    with c2:
        st.button("💻 Generate Code", key="code")
        st.button("🎯 Interview Questions", key="interview")

    st.markdown("<br>", unsafe_allow_html=True)

    for msg in st.session_state.messages:

        if msg["role"] == "user":
            st.info(msg["content"])
        else:
            st.success(msg["content"])

    prompt = st.text_input(
        "Chat Input",
        placeholder="Ask anything...",
        label_visibility="collapsed"
    )

    if prompt:

        st.session_state.messages.append(
            {
                "role":"user",
                "content":prompt
            }
        )

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":"This is a demo AI response."
            }
        )

        st.session_state.timeline.append(prompt[:25])

        st.rerun()

# ==================================================
# RIGHT PANEL
# ==================================================
with right:

    st.markdown("## 🚀 AI Dashboard")

    a, b = st.columns(2)

    with a:
        st.metric("Conf", f"{confidence}%")
        st.metric("Tokens", tokens_used)

    with b:
        st.metric("Depth", chat_depth)
        st.metric("Prod", f"{productivity}%")

    st.markdown("### 🧠 Topic")
    st.info("Machine Learning")

    st.markdown("### 📈 Progress")
    st.progress(80)

    st.markdown("### 💡 Insight")
    st.success("Learning-focused session")

    st.rerun()
