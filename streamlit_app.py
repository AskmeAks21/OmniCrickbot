import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app
st.title("Ak's Cricket Info Repository")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an AI assistant specializing in cricket and its history. "
                                      "You should only provide information related to cricket, including players, matches, records, and historical events. "
                                      "Do not answer any questions unrelated to cricket. If a user asks about another topic, politely redirect them."}
    ]

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Collect user input
user_input = st.chat_input("Ask me anything about cricket...")

# Function to get a response from OpenAI with context restrictions
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages + [{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Process and display response if there's input
if user_input:
    # Append user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant's response
    assistant_response = get_response(user_input)

    # Check if the response is unrelated (Negative Prompting)
    if "I'm here to talk about cricket" in assistant_response or "I can only provide information on cricket" in assistant_response:
        assistant_response = "I specialize in cricket and its history. Please ask me about cricket-related topics."

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response)
