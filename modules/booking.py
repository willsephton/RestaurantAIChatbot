import pandas as pd
from datetime import datetime
from utils.helpers import respond
import streamlit as st

def book_table():
    st.session_state.conversation_mode = "booking"
    st.session_state.pending_booking = {}
    respond("Sure! I can help you book a table. How many people will be in your party?")

def handle_booking_flow(user_input):
    booking = st.session_state.pending_booking

    if "number_of_people" not in booking:
        try:
            booking["number_of_people"] = int(user_input)
            respond("Got it! What time would you like to book for? (e.g., 7:00 PM)")
        except ValueError:
            respond("Please enter a valid number for the number of people.")
        return

    if "time" not in booking:
        booking["time"] = user_input.strip()
        name = st.session_state.user_name or "Guest"

        new_booking = pd.DataFrame([{
            "name": name,
            "number_of_people": booking["number_of_people"],
            "time": booking["time"],
        }])

        try:
            existing = pd.read_csv("restaurant_data/bookings.csv")
            updated = pd.concat([existing, new_booking], ignore_index=True)
        except FileNotFoundError:
            updated = new_booking

        updated.to_csv("restaurant_data/bookings.csv", index=False)
        respond(f"Booking confirmed for {name} at {booking['time']} for {booking['number_of_people']} people!")
        st.session_state.conversation_mode = None
        st.session_state.pending_booking = {}

def view_bookings():
    name = st.session_state.user_name
    if not name:
        respond("I don’t know your name yet. What’s your name?")
        return

    try:
        df = pd.read_csv("restaurant_data/bookings.csv")
        user_bookings = df[df["name"].str.lower() == name.lower()]
        if user_bookings.empty:
            respond(f"No bookings found for {name}.")
        else:
            bookings_list = "\n".join(
                [f"- {row['number_of_people']} people at {row['time']}" for _, row in user_bookings.iterrows()]
            )
            respond(f"Here are your bookings, {name}:\n{bookings_list}")
    except FileNotFoundError:
        respond("No bookings found yet.")
