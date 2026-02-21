import streamlit as st
from langgraph.graph import StateGraph
from langchain_openai import ChatOpenAI

# 1. THE UI CONFIGURATION
# We set up the browser window title and header.
st.set_page_config(page_title="Agentic Architect Cockpit")
st.title("Autonomous Worker Interface")

# 2. SESSION MEMORY
# Streamlit reruns the script on every interaction.
# We store the agent's history in st.session_state so it persists.
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. THE ENGINE CONNECTION
# We pull in the logic graph defined in previous modules.
# We use the evergreen placeholder to keep the code up to date.
llm = ChatOpenAI(model="<LATEST_FAST_MODEL>", temperature=0)

# Displaying previous chat history to the user.
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. CAPTURING USER INPUT
if prompt := st.chat_input("Command your digital fleet..."):
    # Add the user message to the local memory.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Triggering the LangGraph reasoning engine.
    with st.chat_message("assistant"):
        # We invoke the agent and stream the response to the UI.
        # This keeps the browser from looking frozen during heavy thinking.
        response = llm.invoke(st.session_state.messages)
        st.markdown(response.content)
        
    # Save the assistant's reply to the session.
    st.session_state.messages.append({"role": "assistant", "content": response.content})
