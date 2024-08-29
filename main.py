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
            st.markdown(f"<div style='background-color: #dfefff; color: black; padding: 8px; border-radius: 5px; margin-bottom: 5px;'>**User**: {user_input}</div>", unsafe_allow_html=True)
            st.markdown("<div style='background-color: #f4f4f4; color: black; padding: 8px; border-radius: 5px; margin-bottom: 5px;'>**Bot**: ...</div>", unsafe_allow_html=True)

        with st.spinner("Generating response..."):
            response = llm.stream(user_input, stop=['<|eot_id|>'])
            full_response = "".join(response)
            response_placeholder.empty()  
            st.session_state['conversation_history'].append(f"Bot: {full_response}")

st.markdown("### Conversation History")
for message in st.session_state['conversation_history']:
    if message.startswith("User:"):
        st.markdown(f"<div style='background-color: #8caaee; color: black; padding: 8px; border-radius: 5px; margin-bottom: 5px;'>{message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background-color: #303446; color: white; padding: 8px; border-radius: 5px; margin-bottom: 5px;'>{message}</div>", unsafe_allow_html=True)

st.text_input("Enter your prompt:", value=st.session_state.user_input, key="user_input")

st.button("Generate", on_click=generate_response)

st.empty()