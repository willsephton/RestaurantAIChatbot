import streamlit as st

def respond(message: str):
    # ! Add a bot message to chat history.
    st.session_state.chat_history.append(("bot", message))

def show_chat(chat_placeholder):
    # ! Render all chat messages.
    chat_placeholder.empty()
    with chat_placeholder.container():
        for sender, message in st.session_state.chat_history:
            if sender == "user":
                st.chat_message("user").markdown(message)
            else:
                st.chat_message("assistant").markdown(message)
