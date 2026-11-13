import uuid

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from langgraph_tool_backend import chatbot, retrieve_all_threads


# ******************************* Utility functions **********************************
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversation(thread_id):
    return chatbot.get_state(config={'configurable': {'thread_id': thread_id}}).values.get('messages', [])

def get_thread_title(thread_id, max_len=30):
    for msg in load_conversation(thread_id):
        if isinstance(msg, HumanMessage):
            title = msg.text.strip()
            return title if len(title) <= max_len else title[:max_len] + '...'
    return None

# ******************************* Session Setup **********************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])

# ******************************* Sidebar UI **********************************
st.sidebar.title('Langgraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.header('My Conversations')
for thread_id in st.session_state['chat_threads'][::-1]:
    title = get_thread_title(thread_id)
    if title is None:
        # empty thread, don't list it until it has a first message
        continue
    if st.sidebar.button(title, key=str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []
        for msg in messages:
            # skip ToolMessages and AI messages that only contain tool calls
            if isinstance(msg, HumanMessage):
                role = 'human'
            elif isinstance(msg, AIMessage) and msg.text.strip():
                role = 'ai'
            else:
                continue
            temp_messages.append({'role': role, 'content': msg.text})

        st.session_state['message_history'] = temp_messages

# ******************************* Main UI **********************************
# Loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:

    # add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('human'):
        st.text(user_input)

    # CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {
            "thread_id": st.session_state["thread_id"]
        },
        "run_name": "chat_turn",
    }
    
    with st.chat_message('ai'):
        ai_message = st.write_stream(
            message_chunk.text for message_chunk, metadata in chatbot.stream({
                'messages': [HumanMessage(content=user_input)]
                }, 
                config = CONFIG,
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

    # first exchange in this thread: rerun so it shows up in the sidebar right away
    if len(st.session_state['message_history']) == 2:
        st.rerun()