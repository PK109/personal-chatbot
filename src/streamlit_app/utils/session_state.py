import streamlit as st
import random

def init_session_state():
    if "last_category" not in st.session_state:
        st.session_state.last_category = ""

    if "project_intro" not in st.session_state:
        st.session_state.project_intro = []
        st.session_state.project_intro.append({'role': 'system', "content": "Here is a information about main projects developed by Przemysław Kuta. There were also minor ones, that are not described here."})
        for fname in ["./docs/e-commerce-workflow.txt", "./docs/data_streaming.txt", "./docs/zoho_api.txt", "./docs/links.txt"]:
            with open(fname, "r") as f:
                st.session_state.project_intro.append({'role': 'system', "content": f.read()})
    
    if "personal_intro" not in st.session_state:
        st.session_state.personal_intro = []
        st.session_state.personal_intro.append({'role': 'system', "content": "Here is a brief information about Przemysław Kuta."})
        for fname in ["./docs/linkedin_summary.txt", "./docs/skillset_summary.txt"]:
            with open(fname, "r") as f:
                st.session_state.personal_intro.append({'role': 'system', "content": f.read()})
    
    if "messages" not in st.session_state:
        init_message = "Hello! I am a personal assistant of Przemysław Kuta.\nFeel free to ask me about him, his experience or project portfolio!"
        system_message = "Be concise in your answers. Highly rely on the information provided in the documents. Try to respond in user's language. If you don't know the answer, say that you don't know."
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": init_message})
        st.session_state.messages.append({"role": "system", "content": system_message})
    
    if "placeholder" not in st.session_state:
        with open("./docs/faq.txt", "r") as f:
            text = f.read()
            lines = text.split("\n")
        st.session_state.placeholder = random.choice(lines)