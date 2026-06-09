import streamlit as st
import pandas as pd
import sqlite3
from auth import create_user
from qa_engine import get_response
import sqlite3

def run_query(query, params=(), fetch=False, fetchall=False):
    conn = sqlite3.connect("users.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute(query, params)

    result = None

    if fetch:
        result = cursor.fetchone()
    elif fetchall:
        result = cursor.fetchall()

    conn.commit()
    conn.close()

    return result

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

if "page" not in st.session_state:
    st.session_state.page = "chat"

if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None   
# ==================================================
# CALCULATED ANALYTICS
# ==================================================

tokens_used = sum(
    len((msg.get("content") or "").split())
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




# ==================================================
# LEFT PANEL
# ==================================================



# ==========================================
# SESSION STATE
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ==========================================
# LOGIN FUNCTION
# ==========================================

def login_user(email, password):

    user = run_query(
        """
        SELECT * FROM users
        WHERE email=? AND password=?
        """,
        (email, password),
        fetch=True
    )

    return user
# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp{
background-color:#202123;
color:white;
}

.main{
padding-top:80px;
}

.login-box{
background:#2A2B32;
padding:30px;
border-radius:15px;
}

.big-title{
text-align:center;
font-size:42px;
font-weight:bold;
margin-bottom:10px;
}

.sub-title{
text-align:center;
color:#B0B0B0;
margin-bottom:30px;
}

.stButton > button{
width:100%;
height:45px;
border-radius:10px;
background:#10A37F;
color:white;
font-weight:bold;
border:none;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# MAIN APP
# ==========================================

def show_chatgpt():

    if st.button(
        "Logout",
        key="logout_btn"
    ):
        st.session_state.logged_in = False
        st.rerun()

# ==========================================
# AUTH PAGE
# ==========================================
import sqlite3

def get_user_id(email):

    result = run_query(
        "SELECT id FROM users WHERE email=?",
        (email,),
        fetch=True
    )

    if result:
        return result[0]

    return None

def profile_exists(email):

    user_id = get_user_id(email)

    profile = run_query(
        "SELECT * FROM profiles WHERE user_id=?",
        (user_id,),
        fetch=True
    )

    return profile
def show_onboarding():

    st.title("👋 Welcome")
    st.subheader("Complete your profile")

    full_name = st.text_input("Full Name")
    phone_number = st.text_input("Phone Number")
    college = st.text_input("College")

    if st.button("Continue", key="onboarding_ml_btn"):

        user_id = get_user_id(st.session_state.user_email)

        run_query(
            """
            INSERT INTO profiles
            (user_id, full_name, phone_number, college)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, full_name, phone_number, college)
        )

        st.success("Profile saved successfully!")
        st.rerun()
def get_user_chats(email):

    user_id = get_user_id(email)

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, title
        FROM chats
        WHERE user_id=?
        ORDER BY id DESC
        """,
        (user_id,)
    )

    chats = cursor.fetchall()

    conn.close()

    return chats        


def show_auth():

    st.markdown(
        """
        <div class='big-title'>
        🤖 ChatGPT
        </div>

        <div class='sub-title'>
        Log in to continue
        </div>
        """,
        unsafe_allow_html=True
    )

    login_tab, signup_tab = st.tabs(
        ["Login", "Create Account"]
    )

    # ==================================
    # LOGIN
    # ==================================

    with login_tab:

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Continue",
            key="login_btn"
        ):

            user = login_user(
                email,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user_email = email
                if "page" not in st.session_state:
                    st.session_state.page = "chat"

                st.rerun()

            else:

                st.error(
                    "Invalid email or password"
                )

    # ==================================
    # SIGNUP
    # ==================================

    with signup_tab:

        email = st.text_input(
            "Email",
            key="signup_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        if st.button(
            "Create Account",
            key="signup_btn"
        ):

            success = create_user(
                email,
                password
            )

            if success:

                st.success(
                    "Account created successfully!"
                )

            else:

                st.error(
                    "Email already exists"
                )

# ==========================================
# APP FLOW
# ==========================================

# ==============================
# APP FLOW (CLEAN VERSION)
# ==============================

# 1. AUTH CHECK
if not st.session_state.logged_in:
    show_auth()
    st.stop()

# 2. PROFILE CHECK (only once)
profile = profile_exists(st.session_state.user_email)

if not profile:
    show_onboarding()
    st.stop()


# ==============================
# PROFILE FUNCTIONS (CLEAN)
# ==============================

def get_profile(email):

    user_id = get_user_id(email)

    return run_query(
        """
        SELECT full_name, phone_number, college
        FROM profiles
        WHERE user_id=?
        """,
        (user_id,),
        fetch=True
    )


def update_profile(email, full_name, phone, college):

    user_id = get_user_id(email)

    run_query(
        """
        UPDATE profiles
        SET full_name=?,
            phone_number=?,
            college=?
        WHERE user_id=?
        """,
        (full_name, phone, college, user_id)
    )


def show_profile():

    st.title("👤 Profile")

    profile = get_profile(st.session_state.user_email)

    if not profile:
        st.warning("No profile found")
        return

    full_name = st.text_input("Full Name", value=profile[0])
    phone = st.text_input("Phone Number", value=profile[1])
    college = st.text_input("College", value=profile[2])

    if st.button("Save Changes", key="save_profile"):

        update_profile(
            st.session_state.user_email,
            full_name,
            phone,
            college
        )

        st.success("Profile Updated Successfully")
        st.rerun()


# ==============================
# CHAT MESSAGES LOADER
# ==============================

def load_messages(chat_id):

    return run_query(
        """
        SELECT role, content
        FROM messages
        WHERE chat_id=?
        """,
        (chat_id,),
        fetchall=True
    )
        

left, center, right = st.columns([1.2, 6, 1.5])

# =========================
# LEFT PANEL
# =========================
with left:

    st.markdown("## 🤖 ChatGPT")

    # NEW CHAT
    if st.button("➕ New Chat", key="new_chat_btn"):

        user_id = get_user_id(st.session_state.user_email)

        run_query(
            "INSERT INTO chats (user_id, title) VALUES (?, ?)",
            (user_id, "Chat")
        )

        chat_id = run_query(
            "SELECT last_insert_rowid()",
            fetch=True
        )[0]

        st.session_state.current_chat_id = chat_id
        st.session_state.messages = []

        st.rerun()

    st.text_input(
        "Search Chats",
        placeholder="🔍 Search Chats",
        label_visibility="collapsed",
        key="search_chats"
    )

    st.divider()

    if st.button("💬 Chat", key="chat_btn"):
        st.session_state.page = "chat"

    if st.button("👤 Profile", key="profile_btn"):
        st.session_state.page = "profile"

    st.divider()

    st.markdown("### 📅 Recent Chats")

    chats = get_user_chats(st.session_state.user_email)

    for chat_id, title in chats:
        if st.button(title, key=f"chat_{chat_id}"):

            st.session_state.current_chat_id = chat_id
            data = load_messages(chat_id)

            st.session_state.messages = [
             {"role": r, "content": c or ""}
             for r, c in data
            ]

            st.rerun()

    st.divider()


# =========================
# CENTER PANEL
# =========================
with center:

    if st.session_state.page == "profile":
        show_profile()

    else:

        st.markdown("""
        <div class='chat-title'>ChatGPT</div>
        <div class='chat-subtitle'>Your AI Workspace</div>
        """, unsafe_allow_html=True)

        # suggestions
        if len(st.session_state.messages) == 0:
            c1, c2 = st.columns(2)

            with c1:
                st.button("🧠 Explain ML", key="ml_btn")
                st.button("📄 Summarize PDF", key="pdf_btn")

            with c2:
                st.button("💻 Generate Code", key="code_btn")
                st.button("🎯 Interview Questions", key="interview_btn")

        # chat history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # input
        prompt = st.chat_input("Ask anything...")

        if prompt and prompt.strip():

            if st.session_state.current_chat_id is None:
                st.error("Please create a new chat first.")
                st.stop()

            # save user msg
            run_query(
                "INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)",
                (st.session_state.current_chat_id, "user", prompt)
            )

            # AI response
            response = get_response(prompt)

            # save assistant msg
            run_query(
                "INSERT INTO messages (chat_id, role, content) VALUES (?, ?, ?)",
                (st.session_state.current_chat_id, "assistant", response)
            )

            # update UI
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": response})

            st.rerun()


# =========================
# RIGHT PANEL
# =========================
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