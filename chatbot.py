import streamlit as st
from models.intent_model import load_model
from utils.session_state import init_session_state
from utils.helpers import respond, show_chat
from modules.basic_intents import *
from modules.booking import *
from modules.ordering import *
import re

st.set_page_config(page_title="🍝 Pasta la Vista Chatbot", layout="centered", initial_sidebar_state="collapsed")

with st.sidebar:
    st.title("🍝 About Pasta la Vista")
    st.markdown("""
    ### Your AI Restaurant Assistant
    
    Welcome to **Pasta la Vista Chatbot** — your friendly restaurant companion!  
    Here's what I can do for you:
    
    - 🍽️ Show the full restaurant menu  
    - ⭐ Tell you today's specials  
    - 📅 Help you **book a table**  
    - 🧾 Let you **place and view orders**  
    - 🕒 Share our opening hours and location  
    - 💬 Engage in small talk to make your visit more enjoyable  
    
    ---
    🧠 **Tip:**  
    Just type something like:
    - “Show me the menu”
    - “Book a table for 2 at 7 PM”
    - “My name is Will”
    - “What’s the special today?”
    """)


# ! Initialize
init_session_state()
model = load_model()

st.title("🍝 Pasta la Vista Chatbot")
st.caption("Your friendly restaurant assistant")

chat_placeholder = st.empty()

# ! Initial greeting
if not st.session_state.chat_history:
    respond("Hello! Welcome to Pasta la Vista 🍝")
    if st.session_state.user_name:
        respond(f"How can I assist you today, {st.session_state.user_name}?")
    else:
        respond("What’s your name?")

show_chat(chat_placeholder)
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    if st.session_state.conversation_mode == "booking":
        handle_booking_flow(user_input)
        show_chat(chat_placeholder)
        st.stop()

    elif st.session_state.conversation_mode == "ordering":
        handle_order_flow(user_input)
        show_chat(chat_placeholder)
        st.stop()
    
    if not st.session_state.user_name:
        # Match phrases like "my name is Will", "I'm Will", or "I am Will"
        name_match = re.search(r"(?:my name is|i am|i'm)\s+([A-Za-z]+)", user_input, re.IGNORECASE)
        if name_match:
            name = name_match.group(1).capitalize()
            update_name(name)
            show_chat(chat_placeholder)
            st.stop()

        # If user types just one word (likely their name)
        elif len(user_input.split()) == 1 and user_input.isalpha():
            name = user_input.capitalize()
            update_name(name)
            show_chat(chat_placeholder)
            st.stop()

    intent = model.predict([user_input])[0]

    intent_to_function = {
        "greeting": greeting,
        "chatbot_status": chatbot_status,
        "capabilities": capabilities,
        "get_name": get_name,
        "update_name": lambda: update_name(user_input.split()[-1]),
        "restaurant_hours": restaurant_hours,
        "restaurant_location": restaurant_location,
        "show_menu": show_menu,
        "todays_specials": todays_specials,
        "book_table": book_table,
        "view_bookings": view_bookings,
        "place_order": place_order,
        "view_order": view_order,
    }

    if intent in intent_to_function:
        intent_to_function[intent]()
    else:
        respond("I'm not sure how to answer that. Could you rephrase or ask another question?")

    show_chat(chat_placeholder)
