import os

import requests
import streamlit as st

from dotenv import load_dotenv


# Load environment variables
load_dotenv()

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)


# ----------------------------------
# Page Configuration
# ----------------------------------

st.set_page_config(
    page_title="GoAified HR/IT Helpdesk",
    page_icon="🤖",
    layout="centered"
)


# ----------------------------------
# Application Header
# ----------------------------------

st.title("🤖 GoAified HR/IT Helpdesk")

st.caption(
    "Your AI-powered assistant for HR policies, "
    "IT support and employee information."
)


# ----------------------------------
# Sidebar
# ----------------------------------

with st.sidebar:

    st.header("Helpdesk")

    st.write("Ask questions about:")

    st.markdown("""
    - HR policies
    - Annual and sick leave
    - Work from home
    - IT security
    - Employee leave balances
    """)

    st.divider()

    st.subheader("Backend Status")

    try:
        health_response = requests.get(
            f"{API_BASE_URL}/health",
            timeout=5
        )

        if health_response.ok:
            st.success("API Connected")
        else:
            st.error("API Unavailable")

    except requests.RequestException:
        st.error("Cannot connect to FastAPI")

    st.caption(f"API: {API_BASE_URL}")

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ----------------------------------
# Chat History
# ----------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message.get("status") == "blocked":
            st.caption("Request blocked by security guardrails.")


# ----------------------------------
# Chat Input
# ----------------------------------

question = st.chat_input(
    "Ask your HR or IT question..."
)


if question:

    # Display employee question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Call FastAPI backend
    with st.chat_message("assistant"):

        with st.spinner("GoAified AI is thinking..."):

            try:

                response = requests.post(
                    f"{API_BASE_URL}/api/chat",
                    json={
                        "question": question
                    },
                    timeout=180
                )

                response.raise_for_status()

                data = response.json()

                answer = data.get(
                    "answer",
                    "No response received."
                )

                status = data.get(
                    "status",
                    "success"
                )

                st.markdown(answer)

                if status == "blocked":
                    st.caption(
                        "Request blocked by security guardrails."
                    )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "status": status
                })

            except requests.Timeout:

                answer = (
                    "The request took too long. "
                    "Please try again."
                )

                st.error(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except requests.RequestException:

                answer = (
                    "Unable to connect to the helpdesk backend. "
                    "Please ensure the FastAPI server is running."
                )

                st.error(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })