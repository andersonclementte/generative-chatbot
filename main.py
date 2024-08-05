import streamlit as st
from langchain_community.llms import Ollama

llm = Ollama(model="llama3.1")

st.title("Chatbot")

if 'conversation_history' not in st.session_state:
    st.session_state['conversation_history'] = []
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ""

def generate_response():
    user_input = st.session_state.user_input
    if user_input:
        st.session_state['conversation_history'].append(f"User: {user_input}")
        st.session_state.user_input = ""

        response_placeholder = st.empty()
        with response_placeholder.container():
            st.write(f"User: {user_input}")
            st.write("Bot: ...")

        with st.spinner("Generating response..."):
            response = llm.stream(user_input, stop=['<|eot_id|>'])
            full_response = "".join(response) 
            response_placeholder.empty()  # Clear the placeholder
            st.session_state['conversation_history'].append(f"Bot: {full_response}")

for message in st.session_state['conversation_history']:
    st.markdown(f"{message}")

user_input = st.text_area("Enter your prompt:", value=st.session_state.user_input, key="user_input")

if st.button("Generate", on_click=generate_response):
    pass

st.empty()
