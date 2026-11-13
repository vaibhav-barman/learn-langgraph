from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph, add_messages

load_dotenv()

llm = ChatGoogleGenerativeAI(model='gemini-3.5-flash-lite')

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):

    # take user query from state
    messages = state['messages']

    # send it to llm
    response = llm.invoke(messages)

    # response stored to state
    return {'messages': [response]}

# Checkpointer
checkpointer = InMemorySaver()
graph = StateGraph(ChatState)

# Nodes
graph.add_node('chat_node', chat_node)

# Edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)