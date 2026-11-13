import uuid

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from langgraph_tool_backend import chatbot, retrieve_all_threads


# =========================== Utilities ===========================
def generate_thread_id():
    return uuid.uuid4()

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get("messages", [])

def get_thread_title(thread_id, max_len=30):
    """Title a thread by its first user message; None if the thread has no messages yet."""
    for msg in load_conversation(thread_id):
        if isinstance(msg, HumanMessage):
            title = msg.text.strip()
            if not title:
                continue
            return title if len(title) <= max_len else title[:max_len] + "..."
    return None

# ======================= Session Initialization ===================
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

add_thread(st.session_state["thread_id"])

# ============================ Sidebar ============================
st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()

st.sidebar.header("My Conversations")
for thread_id in st.session_state["chat_threads"][::-1]:
    title = get_thread_title(thread_id)
    if title is None:
        # empty thread: don't list it until it has a first message
        continue
    # key keeps buttons unique even when two threads start with the same message
    if st.sidebar.button(title, key=str(thread_id)):
        st.session_state["thread_id"] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []
        for msg in messages:
            # skip ToolMessages and AI messages that only contain tool calls
            if isinstance(msg, HumanMessage):
                role = "user"
            elif isinstance(msg, AIMessage) and msg.text.strip():
                role = "assistant"
            else:
                continue
            temp_messages.append({"role": role, "content": msg.text})
        st.session_state["message_history"] = temp_messages

# ============================ Main UI ============================

# Render history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Type here")

if user_input:
    # Show user's message
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
    }

    # Assistant streaming block
    with st.chat_message("assistant"):
        # Use a mutable holder so the generator can set/modify it
        status_holder = {"box": None}

        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                # Lazily create & update the SAME status container when any tool runs
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"🔧 Using `{tool_name}` …", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"🔧 Using `{tool_name}` …",
                            state="running",
                            expanded=True,
                        )

                # Stream ONLY assistant text tokens. Use .text (always a str): .content can be
                # a list for Gemini, and st.write_stream renders non-strings (e.g. []) as JSON.
                if isinstance(message_chunk, AIMessage) and message_chunk.text:
                    yield message_chunk.text

        ai_message = st.write_stream(ai_only_stream())

        # Finalize only if a tool was actually used
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool finished", state="complete", expanded=False
            )

    # Save assistant message
    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )

    # first exchange in this thread: rerun so it shows up in the sidebar right away
    if len(st.session_state["message_history"]) == 2:
        st.rerun()