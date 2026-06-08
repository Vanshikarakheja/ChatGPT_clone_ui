import streamlit as st

st.set_page_config(
    page_title="ChatGPT Clone",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.stApp {
    background-color: #212121;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #171717;
}

.chat-container {
    max-width: 800px;
    margin: auto;
}

.user-msg {
    background: #2f2f2f;
    padding: 12px;
    border-radius: 12px;
    margin: 10px 0;
}

.assistant-msg {
    background: #303030;
    padding: 12px;
    border-radius: 12px;
    margin: 10px 0;
}

.big-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    margin-top: 40px;
}

.subtitle {
    text-align: center;
    color: #bbbbbb;
    margin-bottom: 30px;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("ChatGPT")

    st.button("➕ New Chat")

    st.divider()

    st.subheader("Recent Chats")

    st.button("Machine Learning")
    st.button("Python Project")
    st.button("Interview Prep")
    st.button("Data Analysis")

    st.divider()

    st.subheader("Tools")

    st.button("📄 PDF Assistant")
    st.button("🐍 Python Helper")
    st.button("📊 Data Analyst")
    st.button("🎓 Study Assistant")

# -----------------------------
# Main Screen
# -----------------------------

if len(st.session_state.messages) == 0:

    st.markdown(
        '<div class="big-title">ChatGPT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">How can I help you today?</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧠 Explain Machine Learning"):
            st.session_state.prompt = "Explain Machine Learning"

        if st.button("📄 Summarize a PDF"):
            st.session_state.prompt = "Summarize a PDF"

    with col2:
        if st.button("💻 Generate Python Code"):
            st.session_state.prompt = "Generate Python Code"

        if st.button("🎯 Interview Questions"):
            st.session_state.prompt = "Interview Questions"

# -----------------------------
# Chat History
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat Input
# -----------------------------
prompt = st.text_input("Message ChatGPT")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    fake_response = f"""
I received your message:

**{prompt}**

This is a sample AI response used for demonstrating the UI.

You can replace this later with OpenAI, Groq, or any backend model.
"""

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": fake_response
        }
    )

    st.rerun()