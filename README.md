# AI Agent in Python

A command-line AI Agent that connects to LLMs via OpenRouter and executes local functions dynamically.

> **Curriculum Note:** This project was built as a guided project in the [Boot.dev](https://www.boot.dev) Backend Developer Path, focusing on LLM tool-calling (function calling), API integration, and safe local execution.

---

## What It Does

The agent runs a conversational loop (capped at 20 turns) that accepts a user prompt from the command line, forwards it to an LLM, and allows the model to invoke local Python tools to inspect files, write content, and execute code before returning a final answer.

### Available Tools / Functions
- `get_files_info(directory)`: Scans a directory and returns file names and sizes.
- `get_file_content(file_path)`: Reads and returns the content of a local file safely.
- `write_file(file_path, content)`: Writes content to a target file.
- `run_python_file(file_path)`: Executes a local Python script in a subprocess and captures output.

---

## Technical Details

- **Language:** Python 3.13 (`uv` package manager)
- **Dependencies:** `openai` (v2.44+), `python-dotenv`
- **API Provider:** OpenRouter (`openrouter/free` or specified model)
- **Features:**
  - Dynamic tool-calling with JSON schema definitions
  - Token tracking (calculates and logs prompt tokens and completion tokens)
  - Execution safeguards (prevents infinite LLM loops by enforcing a 20-step ceiling)
  - Verbose flag (`--verbose`) for inspecting tool arguments and function outputs in real-time
  - Unit test coverage for tool functions (`test_get_file_content.py`, `test_get_files_info.py`, `test_run_python_file.py`, `test_write_file.py`)

---

## How to Run

### 1. Prerequisites & Environment
Clone the repository and set up your virtual environment using `uv`:

```bash
uv sync
```

Create a `.env` file with your OpenRouter API key:
```env
OPENROUTER_API_KEY=your_key_here
```

### 2. Usage
Run the agent with a prompt:
```bash
python main.py "List the files in calculator/ and run its tests"
```

Run with verbose logging to see tool invocations:
```bash
python main.py "What does lorem.txt say?" --verbose
```

### 3. Running Tests
```bash
python -m unittest discover .
```
