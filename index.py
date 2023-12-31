import streamlit as st
from chat import chatbot
import time


def hello():
    with st.chat_message("assistant"):
        st.write("Hello 👋")


def chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("say something"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            response, sources, texts = chatbot(prompt)
            for event in response.events():
                full_response += event.data
                message_placeholder.markdown(full_response + " ")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            for i in range(len(sources)):
                expander_text = 'file: {}, page: {}'.format(sources[i][0], int(sources[i][1]))
                with st.expander(expander_text):
                    st.markdown(texts[i])


if __name__ == '__main__':
    hello()
    chat()

# D:\Desktop\pythonSRT\venv\Scripts\streamlit.exe run index.py
