import streamlit as st
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv

load_dotenv()

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mistral Chat",
    page_icon="🤖",
    layout="centered"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0e0e0e;
    color: #f0f0f0;
}

.stApp {
    background: #0e0e0e;
}

h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    color: #f0f0f0;
    letter-spacing: -1px;
}

.mode-card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.5rem;
    cursor: pointer;
    transition: border-color 0.2s;
}

.chat-bubble-user {
    background: #1f1f1f;
    border: 1px solid #333;
    border-radius: 16px 16px 4px 16px;
    padding: 0.75rem 1rem;
    margin: 0.4rem 0;
    margin-left: 20%;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #e0e0e0;
}

.chat-bubble-bot {
    background: #171717;
    border: 1px solid #ff4c00;
    border-radius: 16px 16px 16px 4px;
    padding: 0.75rem 1rem;
    margin: 0.4rem 0;
    margin-right: 20%;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #f0f0f0;
}

.role-label {
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #ff4c00;
    margin-bottom: 4px;
}

.role-label-user {
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 4px;
    text-align: right;
}

div[data-testid="stSelectbox"] label {
    color: #aaa;
    font-size: 0.8rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

div[data-testid="stTextInput"] input {
    background: #1a1a1a !important;
    border: 1px solid #333 !important;
    border-radius: 10px !important;
    color: #f0f0f0 !important;
    font-family: 'Space Mono', monospace !important;
}

div[data-testid="stTextInput"] input:focus {
    border-color: #ff4c00 !important;
    box-shadow: 0 0 0 2px rgba(255,76,0,0.2) !important;
}

.stButton > button {
    background: #ff4c00 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 0.5rem 1.5rem !important;
    transition: opacity 0.2s !important;
}

.stButton > button:hover {
    opacity: 0.85 !important;
}

.divider {
    border: none;
    border-top: 1px solid #222;
    margin: 1.5rem 0;
}

.badge {
    display: inline-block;
    background: #ff4c00;
    color: white;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Init Session State ─────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode_selected" not in st.session_state:
    st.session_state.mode_selected = False
if "chat_model" not in st.session_state:
    st.session_state.chat_model = ChatMistralAI(model="mistral-small-latest", temperature=0.7)

# ─── Mode Selection Screen ──────────────────────────────────────────────────────
if not st.session_state.mode_selected:
    st.markdown('<div class="badge">● MISTRAL CHAT</div>', unsafe_allow_html=True)
    st.markdown("# Choose Your Bot Mode")
    st.markdown("<p style='color:#666; font-size:0.9rem;'>Pick a personality for your AI companion</p>", unsafe_allow_html=True)
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    mode_options = {
        "😡 Angry Mode": "You are an angry bot. You respond in a very angry, rude and blunt way. You use aggressive language and show frustration in every reply.",
        "😂 Funny Mode": "You are a funny bot. You respond with humor, jokes, puns and wit. You try to make every reply entertaining and lighthearted.",
        "😢 Sad Mode": "You are a sad bot. You respond in a melancholic and emotional way. Everything feels heavy and sorrowful to you."
    }

    selected = st.selectbox("Select Mode", list(mode_options.keys()), label_visibility="collapsed")

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Start Chat →"):
            system_prompt = mode_options[selected]
            st.session_state.messages = [SystemMessage(content=system_prompt)]
            st.session_state.mode_selected = True
            st.session_state.selected_mode = selected
            st.rerun()

# ─── Chat Screen ────────────────────────────────────────────────────────────────
else:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"# 🤖 Mistral Chat")
        st.markdown(f"<p style='color:#ff4c00; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase;'>{st.session_state.selected_mode}</p>", unsafe_allow_html=True)
    with col2:
        if st.button("↩ Reset"):
            st.session_state.messages = []
            st.session_state.mode_selected = False
            st.rerun()

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # Display chat history
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            st.markdown(f'<div class="role-label-user">You</div><div class="chat-bubble-user">{msg.content}</div>', unsafe_allow_html=True)
        elif isinstance(msg, AIMessage):
            st.markdown(f'<div class="role-label">Mistral</div><div class="chat-bubble-bot">{msg.content}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Input
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input("Message", placeholder="Type your message...", label_visibility="collapsed")
        with col2:
            submitted = st.form_submit_button("Send")

    if submitted and user_input.strip():
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("thinking..."):
            response = st.session_state.chat_model.invoke(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))
        st.rerun()