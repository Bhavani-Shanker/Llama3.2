import requests
import json
import streamlit as st

url = "https://llama32-n85yrsvpztvqdwctqsg8q5.streamlit.app/"


headers = {
    'Content-Type': 'application/json'
}

if "history" not in st.session_state:
    st.session_state.history = []


def generate_response(prompt):
    st.session_state.history.append(prompt)
    final_prompt = "\n".join(st.session_state.history)

    data = {
        "model": "llama3.2",
        "prompt": final_prompt,
        "stream": False
    }

    
    response = requests.post(url, headers=headers, data=json.dumps(data))

    
    if response.status_code == 200:
        data = response.json()
        actual_response = data['response']
        return actual_response
    else:
        st.error(f"Error: {response.text}")
        return None


st.set_page_config(page_title="LLaMA 3.2 Chat Interface", layout="wide")


st.title("💬 LLama 3.2 Chat Interface")

# Introduction
st.markdown("""
This application allows you to interact with the **LLaMA model**. 
Simply enter your prompt below and click the button to receive a response.
""")

prompt = st.text_area("Enter your Prompt:", height=100)

# Button to submit the prompt
if st.button("Generate Response"):
    if prompt:
        
        response = generate_response(prompt)
        
        
        if response:
            st.success("Response:")
            st.markdown(f"> {response}")
    else:
        st.error("Please enter a prompt.")

st.sidebar.title("Conversation History")
if st.session_state.history:
    for i, message in enumerate(st.session_state.history):
        st.sidebar.markdown(f"{i + 1}. **User:** {message}")

if st.sidebar.button("Clear History"):
    st.session_state.history.clear()
    st.sidebar.success("Conversation history cleared.")
