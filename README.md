<div align="center">

# 🕸️ Learn LangGraph

**A hands-on journey into building agentic AI systems with LangGraph**

![Python](https://img.shields.io/badge/Python-3.14+-3776AB?logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1.2+-1C3C3C?logo=langchain&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1.5+-1C3C3C?logo=langchain&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-LLM-4285F4?logo=google&logoColor=white)
![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37626?logo=jupyter&logoColor=white)

</div>

---

## 📖 Overview

This repository is a practice workspace for **Agentic AI using LangGraph**. It covers the topics below, starting with graph fundamentals and ending with advanced RAG and full agentic projects. Each topic is a notebook or script, so you can run and modify the examples directly.

---

## 🧰 Tech Stack

| Layer | Tools |
| --- | --- |
| Language | Python 3.14 |
| Orchestration | LangGraph, LangChain |
| LLM Provider | Google Gemini (`langchain-google-genai`) |
| Config | `python-dotenv` |
| Packaging | `uv` |
| Environment | Jupyter Notebooks |

---

## 🗺️ Roadmap

Status key: ✅ done · 🚧 in progress · ⬜ planned

### 🧠 Part 1 · Foundations

| # | Topic | Status |
| --- | --- | :---: |
| 01 | Generative AI vs Agentic AI | ⬜ |
| 02 | What is Agentic AI? | ⬜ |
| 03 | LangChain vs LangGraph | ⬜ |
| 04 | LangGraph Core Concepts | ⬜ |

### 🔀 Part 2 · Workflows

| # | Topic | Notebook | Status |
| --- | --- | --- | :---: |
| 05 | Sequential Workflows | [`1_bmi_workflow.ipynb`](1_bmi_workflow.ipynb) | ✅ |
| 06 | Parallel Workflows | – | ⬜ |
| 07 | Conditional Workflows | – | ⬜ |
| 08 | Iterative Workflows | – | ⬜ |

### 💬 Part 3 · Chatbots & Persistence

| # | Topic | Status |
| --- | --- | :---: |
| 09 | Building a Chatbot with LangGraph | ⬜ |
| 10 | Persistence & Time Travel | ⬜ |
| 11 | Chatbot UI with Streamlit | ⬜ |
| 12 | Streaming | ⬜ |
| 13 | Resume Chat Feature (ChatGPT-style) | ⬜ |
| 14 | LangGraph + SQLite (Database Integration) | ⬜ |

### 🔭 Part 4 · Observability

| # | Topic | Status |
| --- | --- | :---: |
| 15 | LangSmith Crash Course | ⬜ |
| 16 | Observability in LangGraph (LangSmith Integration) | ⬜ |

### 🛠️ Part 5 · Tools, MCP & RAG

| # | Topic | Status |
| --- | --- | :---: |
| 17 | Tools in LangGraph | ⬜ |
| 18 | MCP Client using LangGraph | ⬜ |
| 19 | RAG using LangGraph | ⬜ |

### 🧑‍💻 Part 6 · Advanced Patterns

| # | Topic | Status |
| --- | --- | :---: |
| 20 | Human-in-the-Loop (HITL) | ⬜ |
| 21 | Subgraphs | ⬜ |

### 🧠 Part 7 · Memory

| # | Topic | Status |
| --- | --- | :---: |
| 22 | How LLMs Remember (Memory Fundamentals) | ⬜ |
| 23 | Short-Term Memory | ⬜ |
| 24 | Long-Term Memory | ⬜ |

### 🚀 Part 8 · Projects & Advanced RAG

| # | Topic | Status |
| --- | --- | :---: |
| 25 | Blog Writing Agent (Plans → Researches → Writes) | ⬜ |
| 26 | Corrective RAG (CRAG) | ⬜ |
| 27 | Self-RAG | ⬜ |

---

## 📂 Project Structure

```text
learn-langgraph/
├── 1_bmi_workflow.ipynb   # Sequential workflow: BMI calculator
├── src/                   # Python package source
├── pyproject.toml         # Project metadata & dependencies
├── uv.lock                # Locked dependency versions
├── .python-version        # Pinned Python version
└── README.md
```

---

## ⚙️ Getting Started

### Prerequisites

- Python **3.14+**
- [`uv`](https://docs.astral.sh/uv/) package manager
- A Google Gemini API key

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/vaibhav-barman/learn-langgraph.git
cd learn-langgraph

# 2. Install dependencies
uv sync

# 3. Configure environment variables
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# 4. Launch Jupyter and open a notebook
uv run jupyter notebook
```

---

## 💡 Quick Example

A minimal LangGraph workflow, taken from [`1_bmi_workflow.ipynb`](1_bmi_workflow.ipynb):

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class BMIState(TypedDict):
    weight_kg: float
    height_m: float
    bmi: float

def calculate_bmi(state: BMIState) -> BMIState:
    state["bmi"] = round(state["weight_kg"] / (state["height_m"] ** 2), 2)
    return state

graph = StateGraph(BMIState)
graph.add_node("calculate_bmi", calculate_bmi)
graph.add_edge(START, "calculate_bmi")
graph.add_edge("calculate_bmi", END)

workflow = graph.compile()
workflow.invoke({"weight_kg": 82, "height_m": 1.78})
# {'weight_kg': 82, 'height_m': 1.78, 'bmi': 25.88}
```

---

## 🧩 Core Concepts at a Glance

| Concept | Description |
| --- | --- |
| **State** | Shared data structure passed between nodes |
| **Node** | A function that reads and updates the state |
| **Edge** | A connection that defines execution flow |
| **Conditional Edge** | Routes to different nodes based on the state |
| **Checkpointer** | Persists state for memory and time travel |
| **Subgraph** | A graph nested inside another graph |

---

<div align="center">

⭐ Built while learning agentic AI with LangGraph

</div>
