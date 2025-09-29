import streamlit as st
import requests
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="Food Delivery Chatbot",
    page_icon="🍔",
    layout="centered",
)

# --- UI Elements ---
st.title("🍔 Food Delivery Chatbot")
st.write("Ask me anything about our menu, delivery, or promotions!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input and API Interaction ---
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Call the Flask API ---
    api_url = "https://food-delivery-chatbot.onrender.com/chat"
    headers = {"Content-Type": "application/json"}
    data = {"message": prompt}

    try:
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        bot_response = response.json().get("response", "Sorry, something went wrong.")

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(bot_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the chatbot API. Please make sure the Flask server is running. Error: {e}")

