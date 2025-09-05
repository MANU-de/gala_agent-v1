import streamlit as st
import os
from dotenv import load_dotenv
from alfred_agent import AlfredAgent
import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# Load environment variables (especially for GEMINI_API_KEY)
load_dotenv()

# --- Initialize AlfredAgent ---
# Only initialize Alfred once using st.session_state
if 'alfred_agent' not in st.session_state:
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        st.error("GEMINI_API_KEY environment variable not set. Please set it in your .env file.")
        st.stop() # Stop the app if API key is missing
    
    st.session_state.alfred_agent = AlfredAgent(gemini_api_key=gemini_api_key)
    st.session_state.messages = [] # Initialize chat history
    st.session_state.messages.append({"role": "assistant", "content": "Greetings! I am Alfred, your humble gala host. How may I assist you this splendid evening?"})

alfred = st.session_state.alfred_agent

st.set_page_config(page_title="Alfred the Gala Host", page_icon="🎩")

st.title("🎩 Alfred the Gala Host")
st.markdown("Ask Alfred anything about the gala, its esteemed guests, or even the weather!")

# --- Display Chat Messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Alfred is thinking..."):
            try:
                # Call Alfred's run method
                response = alfred.run(prompt)
                st.markdown(response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                error_message = f"An error occurred while Alfred was processing your request: {e}"
                st.error(error_message)
                st.session_state.messages.append({"role": "assistant", "content": error_message})

# Optional: Add a sidebar for more info or settings
with st.sidebar:
    st.header("About Alfred")
    st.info(
        "Alfred is an AI agent powered by Agentic RAG, designed to assist with gala management. "
        "He uses an LLM (Gemini 2.5 Flash), a custom knowledge base, and external tools to answer your questions intelligently."
    )
    st.write("Project by [Manuela Schrittwieser/GitHub Profile Link]")