import streamlit as st
from langchain_core.messages import HumanMessage

from langgraph_backend import chatbot

# streamlit session_state -> dict
CONFIG = {'configurable': {'thread_id': 'thread-1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


user_input = st.chat_input('Type here')

# Loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

if user_input:

    # add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('human'):
        st.text(user_input)

    
    with st.chat_message('ai'):
        ai_message = st.write_stream(
            message_chunk.text for message_chunk, metadata in chatbot.stream({
                'messages': [HumanMessage(content=user_input)]
                }, 
                config = {'configurable': {'thread_id': 'thread-1'}},
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})