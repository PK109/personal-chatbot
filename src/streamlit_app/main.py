import streamlit as st
from utils.prompts import classification_prompt
from utils.llm_setup import llm, structured_llm
from utils.session_state import init_session_state


init_session_state()

st.title("Project Portfolio Chatbot")
st.write("This is a chat app using Streamlit and LangChain.\nYou can ask questions in your language about Przemek and his experience.")
with st.expander("Disclaimer", expanded=False):
    with open("./docs/disclaimer.txt", "r") as f:
        st.write(f.read())

# Display chat messages from history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input(placeholder=st.session_state.placeholder, key="chat_input", max_chars=500):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = classification_prompt.invoke({"input": prompt})
    classification = structured_llm.invoke(prompt)
    prompt_category = classification.model_dump()['category']
    if prompt_category == "followup question":
        prompt_category = st.session_state.last_category
    st.session_state.last_category = prompt_category

    # Display assistant response in chat message container
    if prompt_category == "other":
        messages = []
        messages.extend(st.session_state.project_intro)
        messages.extend(st.session_state.personal_intro)
        messages.extend(st.session_state.messages)

    elif prompt_category in ["about Me", "experience"]:
        messages = []
        messages.extend(st.session_state.personal_intro)
        messages.extend(st.session_state.messages)

    elif prompt_category in ["programming", "projects", "development"]:
        messages = []
        messages.extend(st.session_state.project_intro)
        messages.extend(st.session_state.messages)

    else:
        messages = []
        messages.extend(st.session_state.messages)       
    
    with st.chat_message("assistant"):
        stream = llm.stream(messages)
        response = st.write_stream(stream)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})