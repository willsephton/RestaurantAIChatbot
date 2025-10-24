import streamlit as st

def init_session_state():
    # ! Initialize session state variables.
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

    if "conversation_mode" not in st.session_state:
        st.session_state.conversation_mode = None

    if "pending_booking" not in st.session_state:
        st.session_state.pending_booking = {}

    if "pending_order" not in st.session_state:
        st.session_state.pending_order = {}
