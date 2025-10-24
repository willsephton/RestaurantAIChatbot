import random
import pandas as pd
from utils.helpers import respond
import streamlit as st

def greeting():
    greetings = [
        "How can I assist you today?",
        "How may I help you?",
        "What can I do for you today?",
        "How can I assist you?",
        "How can I help?",
    ]
    if st.session_state.user_name:
        respond(f"Hello {st.session_state.user_name}! {random.choice(greetings)}")
    else:
        respond("Hello! What is your name?")

def chatbot_status():
    status = [
        "I'm doing great!",
        "I'm functioning smoothly, how about you?",
        "I'm here and ready to assist!",
        "I'm doing well! How can I help you today?",
        "I'm all set, how can I assist you today?",
    ]
    respond(random.choice(status))

def capabilities():
    caps = [
        "I can help you make a reservation or place an order.",
        "I can remember your name for a more personalized chat.",
        "I can answer questions about our menu, specials, and opening hours.",
        "I can engage in small talk to make our chat more fun!",
    ]
    header = (
        f"Hello {st.session_state.user_name}! Here are some things I can do:"
        if st.session_state.user_name
        else "Here are some things I can do:"
    )
    respond(header + "\n" + "\n".join([f"- {msg}" for msg in caps]))

def get_name():
    if st.session_state.user_name:
        respond(f"Your name is {st.session_state.user_name}.")
    else:
        respond("I don't know your name yet. What is your name?")

def update_name(new_name):
    st.session_state.user_name = new_name
    respond(f"Nice to meet you, {st.session_state.user_name}!")

def restaurant_hours():
    try:
        df = pd.read_csv("restaurant_data/restaurant_hours.csv")
        hours = "\n".join([f"{row['day']}: {row['opening_hour']} - {row['closing_hour']}" for _, row in df.iterrows()])
        respond("Here are our opening hours:\n" + hours)
    except:
        respond("Couldn't load restaurant hours.")

def restaurant_location():
    respond("Our restaurant is located at 123 Pasta Street, Food City.")

def show_menu():
    try:
        df = pd.read_csv("restaurant_data/menu.csv")
        menu_str = ""
        for category in df["category"].unique():
            menu_str += f"\n**{category}**:\n"
            subset = df[df["category"] == category]
            for _, row in subset.iterrows():
                menu_str += f"- {row['item_name']} for {row['price']}\n"
        respond("Here’s the menu:\n" + menu_str)
    except:
        respond("Couldn't load the menu.")

def todays_specials():
    try:
        df = pd.read_csv("restaurant_data/specials.csv")
        special = df.sample(1).iloc[0]
        respond(
            f"Today's special is **{special['dish_name']}**!\n{special['description']}\nPrice: {special['price']}"
        )
    except:
        respond("Couldn't load today's specials.")
