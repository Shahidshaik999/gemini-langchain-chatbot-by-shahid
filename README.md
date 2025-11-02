# Gemini LangChain Chatbot — Setup & Troubleshooting

> A complete step-by-step README to reproduce the Gemini + LangChain local chatbot that Shahid built. This file documents every command, exact package versions, and the fixes for the issues encountered so future users won't get stuck.

---

## 🚀 Project summary

This project is a simple terminal-based chatbot that uses **Google Gemini** models via the **google-generativeai** SDK and **LangChain** integration (`langchain-google-genai`). It includes multi-turn chat memory and is configured to run under **Python 3.12**.

This README lists the exact environment, installation commands, model names that worked, and detailed troubleshooting steps for each error encountered during setup.

---

## ✅ Prerequisites

* Windows (instructions assume PowerShell)
* Admin access recommended for Python installation
* A Google account with access to the **Generative Language API** and an API key
* Git (for pushing to GitHub)

---

## 🧾 Exact versions used (stable tested set)

Use these versions to avoid compatibility errors encountered during development:

```
Python: 3.12.x (tested with 3.12)
Packages:
  google-generativeai==0.8.3
  langchain-google-genai==1.0.1
  langchain==0.1.20
  langchain-core==0.1.53
  langgraph==0.0.49
  python-dotenv==1.0.1
```

> Note: Some `langchain` newer releases (>=1.0) removed `pydantic_v1` internals and broke `langchain-google-genai` compatibility. The versions above are the verified working combination.

---

## 1) Install Python 3.12 (if not installed)

1. Download from [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Run the installer and **check `Add python.exe to PATH`** and `Install for all users`.
3. Verify in a *new* PowerShell window:

```powershell
py -3.12 --version
```

---

## 2) Create a project folder and virtual environment (recommended)

Open PowerShell and run:

```powershell
cd "C:\Users\<your-user>\OneDrive\Desktop"
mkdir python_project1
cd python_project1
py -3.12 -m venv .venv
.\.venv\Scripts\activate
```

After activation your prompt shows `(.venv)`.

---

## 3) Install the required packages (exact commands)

Use the interpreter for Python 3.12 so `pip` and `python` target the same environment:

```powershell
py -3.12 -m pip install --upgrade pip
py -3.12 -m pip install google-generativeai==0.8.3 langchain-google-genai==1.0.1 python-dotenv==1.0.1
# If you need langchain/langgraph older compatible versions:
py -3.12 -m pip install "langchain==0.1.20" "langchain-core==0.1.53" "langgraph==0.0.49"
```

> If you already have other versions installed that cause conflicts, uninstall them first:

```powershell
py -3.12 -m pip uninstall -y langchain langchain-core langchain-google-genai langgraph google-generativeai
```

---

## 4) Create `.env` (store your Gemini API key)

Make a `.env` file in the project root (do not commit real keys to public repos):

```
GOOGLE_API_KEY=AIzaSyYourRealKeyHere
```

**Important:** no quotes, no extra spaces, key must be the Generative Language API key.

---

## 5) `main.py` (final working script)

Add `main.py` to the project with this content (multi-turn memory):

```python
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

def main():
    model = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash", temperature=0.7)

    print("Welcome! I am your Gemini AI assistant 🤖")
    print("Ask me anything... (type 'quit' to exit)\n")

    chat_history = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        chat_history.append(HumanMessage(content=user_input))

        try:
            response = model.invoke(chat_history)
            print("Assistant:", response.content, "\n")
            chat_history.append(AIMessage(content=response.content))
        except Exception as e:
            print("Error:", e)
            break

if __name__ == "__main__":
    main()
```

---

## 6) Run your chatbot

From project folder (activate `.venv` if used):

```powershell
py -3.12 main.py
```

Type messages; use `quit` to exit.

---

## Troubleshooting — common errors and fixes

### 1) `ModuleNotFoundError: No module named 'langchain_google_genai'`

* Cause: package not installed in the interpreter you're running.
* Fix: `py -3.12 -m pip install langchain-google-genai==1.0.1`
* If still failing, run pip install using the explicit Python path:
  `"C:\Users\...\Python312\python.exe" -m pip install langchain-google-genai`

### 2) `ModuleNotFoundError` for `langchain_core.pydantic_v1` or similar

* Cause: langchain version mismatch (new LangChain removed pydantic_v1).
* Fix: install `langchain==0.1.20` and `langchain-core==0.1.53`.

### 3) `404 model ... not found for API version v1beta`

* Cause: SDK calling v1beta endpoint while model lives on v1.
* Fix: install `google-generativeai==0.8.3` and `langchain-google-genai==1.0.1` (they use v1); use model names like `models/gemini-2.5-flash`.

### 4) `API key not valid. Please pass a valid API key.`

* Cause A: Wrong key type (not a Generative Language API key)
* Cause B: Generative Language API not enabled for the project
* Fix:

  1. Create an API key via Google Cloud / Maker Suite (Makersuite or Cloud Console); copy exact value.
  2. Make sure Generative Language API / Vertex AI is enabled in the project.
  3. Put it in `.env` as `GOOGLE_API_KEY=AIza...` (no quotes/spaces).
  4. Test with the quick script below to list models (see next section).

### 5) `NotImplementedError` when using `create_react_agent` (langgraph)

* Cause: `ChatGoogleGenerativeAI` does not implement `.bind_tools()` required by LangGraph's prebuilt ReAct agent.
* Fix: Do not use `create_react_agent(model, tools)` with Gemini. Instead either:

  * Use direct `model.invoke(messages)` loop (recommended). Or
  * Build a custom runnable sequence/prompt chain that simulates ReAct manually.

---

## Quick API key + models check (sanity script)

Create `check_models.py` with:

```python
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

for m in genai.list_models():
    print(m.name)
```

Run:

```powershell
py -3.12 check_models.py
```

If you see model names like `models/gemini-2.5-flash` and `models/gemini-2.5-pro`, your key and SDK are correct.

---

## .gitignore (recommended)

```
.venv/
__pycache__/
.env
*.pyc
.DS_Store
```

---

## Final tips & notes (lessons learned)

* Always run `pip` with the same Python interpreter you will run the code with (`py -3.12 -m pip ...`).
* When a package reports missing internals (`pydantic_v1`), don't try to hack imports — match compatible versions instead.
* Avoid `langgraph` prebuilt agents with Gemini until tooling catches up — use direct invocation or build custom pipelines.
* Keep a short `health-check` script (`check_models.py`) in the repo so future users can verify their key and available models immediately.

---

## Example `README` commit message

```
chore: add README with setup, tested package versions, and troubleshooting
```

---

## Contact / Credit

Created by: **Shaik Shahid** — B.Tech CSE (AI & ML)

---

*License: MIT — adapt as needed.*
