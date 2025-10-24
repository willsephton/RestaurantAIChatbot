import pandas as pd
from datetime import datetime
from utils.helpers import respond
import streamlit as st

def place_order():
    st.session_state.conversation_mode = "ordering"
    st.session_state.pending_order = {}
    try:
        df = pd.read_csv("restaurant_data/menu.csv")
        menu_text = ""
        for category in df["category"].unique():
            menu_text += f"\n**{category}**:\n"
            for _, row in df[df["category"] == category].iterrows():
                menu_text += f"- {row['item_name']} ({row['price']})\n"
        respond("Here’s our menu:\n" + menu_text + "\nWhat would you like to order?")
    except:
        respond("Couldn't load the menu.")

def handle_order_flow(user_input):
    name = st.session_state.user_name or "Guest"
    order_item = user_input.strip().lower()

    try:
        df = pd.read_csv("restaurant_data/menu.csv")
        df["item_name_lower"] = df["item_name"].str.lower()

        if order_item not in df["item_name_lower"].values:
            respond(f"Sorry, we don't have '{user_input}' on the menu. Please choose a valid item.")
            return

        item = df[df["item_name_lower"] == order_item].iloc[0]
        order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_order = pd.DataFrame([{
            "name": name,
            "order_item": item["item_name"],
            "category": item["category"],
            "price": item["price"],
            "order_time": order_time,
            "status": "Being prepared",
        }])

        try:
            existing = pd.read_csv("restaurant_data/orders.csv")
            updated = pd.concat([existing, new_order], ignore_index=True)
        except FileNotFoundError:
            updated = new_order

        updated.to_csv("restaurant_data/orders.csv", index=False)
        respond(f"Order confirmed for {item['item_name']}! It will be prepared shortly.")
        st.session_state.conversation_mode = None
        st.session_state.pending_order = {}
    except:
        respond("Sorry, there was an issue placing your order.")

def view_order():
    name = st.session_state.user_name
    if not name:
        respond("I don’t know your name yet. What’s your name?")
        return

    try:
        df = pd.read_csv("restaurant_data/orders.csv")
        user_orders = df[df["name"].str.lower() == name.lower()]
        if user_orders.empty:
            respond(f"No orders found for {name}.")
        else:
            orders_list = "\n".join(
                [f"- {row['order_item']} ({row['category']}, {row['price']}) — {row['status']}" for _, row in user_orders.iterrows()]
            )
            respond(f"Here are your orders, {name}:\n{orders_list}")
    except FileNotFoundError:
        respond("No orders found yet.")
