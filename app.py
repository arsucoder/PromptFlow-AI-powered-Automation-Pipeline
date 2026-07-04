import streamlit as st
import requests

# -----------------------------
# Page Configuration
# -----------------------------
st.title("🤝 Your Personal Assistant")

st.subheader("What can your personal assistant do?")

st.markdown("""
1. Answer questions on various topics.
2. Arrange calendar events and meetings.
3. Read your emails, send replies, and summarize them.
4. Manage your tasks and to-do lists.
5. Take quick notes for you.
6. Track your expenses and budgeting.
""")

st.subheader("💬 Chat with your assistant")

# -----------------------------
# Chat History
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# User Input
# -----------------------------
user_message = st.chat_input("Ask me anything...")

if user_message:

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_message)

    st.session_state.messages.append(
        {"role": "user", "content": user_message}
    )

    try:
        # Send request to n8n webhook
        response = requests.post(
            "https://clerical-absurd-legume.ngrok-free.dev/webhook/effeef99-a431-43d3-be9e-1a51c9113c74",
            json={"message": user_message},
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        # Extract assistant response
        if isinstance(result, list) and len(result) > 0:
            ai_response = result[0].get(
                "output",
                "No response received from the assistant."
            )

        elif isinstance(result, dict):
            ai_response = result.get(
                "output",
                "No response received from the assistant."
            )

        else:
            ai_response = "Unexpected response received."

    except requests.exceptions.RequestException:
        ai_response = "❌ Unable to connect to the assistant. Please try again."

    except ValueError:
        ai_response = "❌ The assistant returned an invalid response."

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(ai_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_response}
    )
