import streamlit as st
import random
import streamlit as st
from st_files_connection import FilesConnection
import streamlit as st
import os

def init_session_state():
    # Create connection object and retrieve file contents.
    # Specify input format is a txt and to cache the result for 600 seconds.
    try:
        conn = st.connection('gcs', type=FilesConnection, ttl=600)
    except Exception as e:
        st.error(f"Error connecting to GCS: {e}")
        st.write("Using local files instead.")
        conn = None
    BUCKET_URL = os.getenv('BUCKET_URL') 
    if BUCKET_URL is None:
        raise EnvironmentError("Missing required environment variable: BUCKET_URL")

    if "project_intro" not in st.session_state:
        st.session_state.project_intro = []
        if conn is not None:
            files = conn.fs.ls(f'gs://{BUCKET_URL}/project_intro')
            for file in files:
                file_name = file.split("/")[-1].split(".")[0]
                if conn.fs.isfile(file):
                    content=conn.read(file, input_format='text', ttl=600)
                    content = f"File: {file_name}\n" + content
                    # st.write(f"File {file_name} loaded with: \n\t{content[:50]}...")
                    st.session_state.project_intro.append({'role': 'system', "content": content})
        else:
            # in case of failure to read files from GCS, use local files
            st.session_state.project_intro.append({'role': 'system', "content": "Here is a information about main projects developed by Przemysław Kuta. There were also minor ones, that are not described here."})
            for fname in ["./docs/e-commerce-workflow.txt", "./docs/data_streaming.txt", "./docs/zoho_api.txt", "./docs/links.txt"]:
                with open(fname, "r") as f:
                    # st.write(f"File {fname} loaded with: \n\t{f.read()[:50]}...")
                    st.session_state.project_intro.append({'role': 'system', "content": f.read()})
    
    if "personal_intro" not in st.session_state:
        st.session_state.personal_intro = []
        if conn is not None:
            files = conn.fs.ls(f'gs://{BUCKET_URL}/personal_intro')
            for file in files:
                file_name = file.split("/")[-1].split(".")[0]
                if conn.fs.isfile(file):
                    content=conn.read(file, input_format='text', ttl=600)
                    content = f"File: {file_name}\n" + content
                    # st.write(f"File {file_name} loaded with: \n\t{content[:50]}...")
                    st.session_state.personal_intro.append({'role': 'system', "content": content})
        # in case of failure to read files from GCS, use local files
        else:
            st.session_state.personal_intro.append({'role': 'system', "content": "Here is a brief information about Przemysław Kuta."})
            st.session_state.personal_intro.append({'role': 'system', "content": "Here is a brief information about Przemysław Kuta."})
            for fname in ["./docs/linkedin_summary.txt", "./docs/skillset_summary.txt"]:
                with open(fname, "r") as f:
                    # st.write(f"File {fname} loaded with: \n\t{f.read()[:50]}...")
                    st.session_state.personal_intro.append({'role': 'system', "content": f.read()})
    
    if "messages" not in st.session_state:
        init_message = "Hello! I am a personal assistant of Przemysław Kuta.\nFeel free to ask me about him, his experience or project portfolio!"
        system_message = "Be concise in your answers. Highly rely on the information provided in the documents. Try to respond in user's language. If you don't know the answer, say that you don't know."
        st.session_state.messages = []
        st.session_state.messages.append({"role": "system", "content": system_message})
        st.session_state.messages.append({"role": "assistant", "content": init_message})
    
    if "placeholder" not in st.session_state:
        content = ""
        if conn is not None:
            file = f'gs://{BUCKET_URL}/general/faq.txt'
            if conn.fs.isfile(file):
                content=conn.read(file, input_format='text', ttl=600)
        else:
            with open("./docs/faq.txt", "r") as f:
                content = f.read()
        lines = content.split("\n")
        st.session_state.placeholder = random.choice(lines)