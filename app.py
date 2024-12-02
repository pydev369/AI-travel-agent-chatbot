import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate

# Streamlit app setup
st.title("Travel Assistant Chatbot 🌍")
st.sidebar.title("Travel Assistant Options")
st.sidebar.markdown("Select your preferences to chat about destinations.")

# Input options for destinations
destinations = st.sidebar.multiselect("Select Destinations", ["Egypt", "Europe"], default=["Egypt", "Europe"])

# Simulate a chatbot conversation
chat_history = st.session_state.get("chat_history", [])

if "chatbot" not in st.session_state:
    # Initialize LangChain ChatOpenAI model
    st.session_state.chatbot = ChatOpenAI(temperature=0.7)

# Display chat messages
st.markdown("## Chat Conversation")
for message in chat_history:
    if message['role'] == 'user':
        st.markdown(f"**You**: {message['content']}")
    elif message['role'] == 'assistant':
        st.markdown(f"**Travel Assistant**: {message['content']}")

# Input field for user to ask questions
user_input = st.text_input("Your question about the destinations:", "")

if st.button("Send") and user_input:
    # Append user's message to chat history
    chat_history.append({"role": "user", "content": user_input})
    
    # Create context for destinations
    context = f"User is comparing travel options for {', '.join(destinations)}."
    system_prompt = SystemMessagePromptTemplate.from_template(context)
    
    # Human message
    human_message = HumanMessagePromptTemplate.from_template(user_input)
    
    # Run the chatbot
    response = st.session_state.chatbot.invoke(
        [system_prompt.format_message(), human_message.format_message()]
    )
    
    # Append AI's response to chat history
    chat_history.append({"role": "assistant", "content": response.content})
    st.session_state.chat_history = chat_history

# Clear chat history
if st.sidebar.button("Reset Chat"):
    st.session_state.chat_history = []

# Footer
st.markdown("---")
st.markdown("**Powered by Streamlit & LangChain** 🚀")
