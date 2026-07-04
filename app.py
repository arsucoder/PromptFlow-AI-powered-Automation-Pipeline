import streamlit as st
import requests

# create the title for the page
st.title("🤝 Your Personal Assistant")

# add subheader
st.subheader("What can your personal assistant do?")

# create a list of what your assistant can do
st.markdown("""
1. Answer questions on various topics.
2. Arrange Calendar events and meetings.
3. Read your emails and send replies, can even summarize them for you.
4. Manage your tasks and to-do lists.
5. Take quick notes for you.
6. Track your expenses and budgeting.
""")

# add chats subheader
st.subheader("💬 Chat with your assistant")

# create a session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# show the messages in chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# create a chat input box
user_message = st.chat_input()

# if user sends a message
if user_message:

    with st.chat_message("user"):
        st.markdown(user_message)

    st.session_state.messages.append(
        {"role": "user", "content": user_message}
    )

    # Send request to n8n
    response = requests.post(
        "https://clerical-absurd-legume.ngrok-free.dev/webhook/effeef99-a431-43d3-be9e-1a51c9113c74",
        json={"message": user_message}
    )

    st.write("Status Code:", response.status_code)
    st.write("Response Text:", response.text)

    try:
        result = response.json()
        st.write("JSON Response:", result)

        # Handle different response formats
        if isinstance(result, list):
            ai_response = result[0]["output"]

        elif isinstance(result, dict):
            ai_response = result.get("output", str(result))

        else:
            ai_response = str(result)

    except Exception as e:
        st.error(f"JSON Error: {e}")
        st.stop()

    with st.chat_message("assistant"):
        st.markdown(ai_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_response}
    )
