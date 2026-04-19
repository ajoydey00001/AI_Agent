# AI_Agent Workspace

This repository is a multi-project workspace for learning and building AI agents.

It contains:

1. A tabular data chatbot project (Q&A + RAG over SQL, CSV, XLSX).
2. A travel-agent project (OpenAI Agents SDK examples, FastAPI API, Streamlit UI).
3. Notebook-based learning modules for RAG, tools, memory, and image/audio demos.

The goal of this README is to help a new developer get productive quickly.

## Table of Contents

1. [Repository Overview](#repository-overview)
2. [Tech Stack](#tech-stack)
3. [Prerequisites](#prerequisites)
4. [Quick Start for New Developers](#quick-start-for-new-developers)
5. [Project 1: Agent-Database-Interaction](#project-1-agent-database-interaction)
6. [Project 2: Travel_Agent](#project-2-travel_agent)
7. [Notebooks and Learning Modules](#notebooks-and-learning-modules)
8. [Environment Variables](#environment-variables)
9. [Troubleshooting](#troubleshooting)
10. [Recommended Onboarding Path](#recommended-onboarding-path)

## Repository Overview

Top-level folders:

- `Agent-Database-Interaction/`: Gradio app for LLM , SQL Q&A and RAG over tabular data.
- `Travel_Agent/`: OpenAI Agents SDK examples with FastAPI and Streamlit interfaces.
- `RAG/`: RAG learning notebooks.
- `Memory/`: memory/vector DB learning notebooks.
- `tools/`: tool-use learning notebooks.
- `image_geration/`: image generation and speech notebooks.

## Tech Stack

Main technologies used across the workspace:

- Python 3.10+
- OpenAI-compatible LLM APIs (OpenAI/GitHub Models/Azure OpenAI)
- LangChain and LangChain Community
- Gradio
- SQLite + SQLAlchemy
- ChromaDB (vector database)
- OpenAI Agents SDK (`openai-agents`)
- FastAPI + Uvicorn
- Streamlit
- Jupyter notebooks for exploration

## Prerequisites

Install these before running projects:

1. Python 3.10 or newer
2. Git
3. SQLite CLI (recommended)
4. A valid API key and endpoint for an OpenAI-compatible model provider

### Windows Notes

- Create and use a virtual environment for each project.
- Install SQLite (optional but recommended):

```powershell
winget install --id=SQLite.sqlite --source=winget
```

## Quick Start for New Developers

If you are new, start from here.

### 1) Clone and open

```bash
git clone <your-repo-url>
cd AI_Agent
```

### 2) Pick one project first

- For data chatbot: go to `Agent-Database-Interaction/`
- For agent orchestration demos: go to `Travel_Agent/`

### 3) Create venv and install dependencies

Example for Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Repeat inside each project folder, because each project has its own `requirements.txt`.

### 4) Configure environment variables

Create a `.env` file in the project folder (details in [Environment Variables](#environment-variables)).

---

## Project 1: Agent-Database-Interaction

Path: `Agent-Database-Interaction/`

### What It Does

This project provides a Gradio chatbot UI that supports:

1. Q&A with a stored SQL database.
2. Q&A with SQL databases generated from CSV/XLSX files.
3. RAG over CSV/XLSX data using ChromaDB embeddings.
4. Upload-and-chat workflow for user-provided CSV/XLSX files.

### Important Files

- `src/app.py`: Gradio application entry point.
- `src/utils/chatbot.py`: chat routing logic for SQL Q&A and RAG.
- `src/utils/load_config.py`: loads YAML and environment configuration.
- `configs/app_config.yml`: paths, prompts, RAG settings.
- `src/prepare_csv_xlsx_sqlitedb.py`: build SQLite DB from stored tabular files.
- `src/prepare_csv_xlsx_vectordb.py`: build Chroma vectors from tabular files.
- `src/utils/upload_file.py`: pipeline for uploaded files.
- `data/`: input data, SQL files, generated DBs, Chroma persistence.

### Setup

From `Agent-Database-Interaction/`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `.env` in `Agent-Database-Interaction/` with your provider values.

### Prepare Data (Choose One or More)

#### A) Build SQL database from `.sql`

1. Put SQL file into `data/sql/` (for example: `Chinook_Sqlite.sql`).
2. Run:

```bash
sqlite3 data/sqldb.db
.read data/sql/Chinook_Sqlite.sql
```

#### B) Build SQL database from CSV/XLSX in `data/csv_xlsx`

```bash
python src/prepare_csv_xlsx_sqlitedb.py
```

This creates `data/csv_xlsx_sqldb.db`.

#### C) Build Chroma vector database from files in `data/for_upload`

```bash
python src/prepare_csv_xlsx_vectordb.py
```

This writes vectors to `data/chroma/`.

### Run the Gradio App

```bash
python src/app.py
```

Open the local URL shown in terminal.

### How to Use the UI

1. Choose `App functionality`:
	- `Chat` for asking questions
	- `Process files` for uploading CSV/XLSX
2. Choose `Chat type`:
	- `Q&A with stored SQL-DB`
	- `Q&A with stored CSV/XLSX SQL-DB`
	- `RAG with stored CSV/XLSX ChromaDB`
	- `Q&A with Uploaded CSV/XLSX SQL-DB`
3. Enter question and submit.

### Notes

- Use read-only databases for safety.
- Keep data schema simple and clean for better query generation.
- The `explore/` folder has notebooks for debugging and understanding internals.

---

## Project 2: Travel_Agent

Path: `Travel_Agent/`

### What It Does

This project demonstrates a progression of agent capabilities:

1. Basic agent response (`v1_basic_agent.py`)
2. Structured outputs with Pydantic (`v2_structured_output.py`)
3. Tool calls (`v3_tool_calls.py`)
4. Agent handoffs to specialists (`v4_handoffs.py`)
5. Guardrails and user context (`v5_guardrails_and_contexts.py`)
6. Streamlit conversational UI (`v6_streamlit_agent.py`)

It also includes a production-style API wrapper:

- `fastapi_travel_agent.py` (FastAPI REST service)
- `test_fastapi_agent.py` (API test client)

### Setup

From `Travel_Agent/`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Create `.env` in `Travel_Agent/`:

```env
BASE_URL="https://models.github.ai/inference/v1"
API_KEY="<your_api_key>"
MODEL_NAME="openai/gpt-4.1-nano"
```

### Run Individual Examples

```bash
python v1_basic_agent.py
python v2_structured_output.py
python v3_tool_calls.py
python v4_handoffs.py
python v5_guardrails_and_contexts.py
```

### Run Streamlit App

```bash
streamlit run v6_streamlit_agent.py
```

### Run FastAPI Server

Option 1:

```bash
python fastapi_travel_agent.py
```

Option 2:

```bash
uvicorn fastapi_travel_agent:app --host 0.0.0.0 --port 8000 --reload
```

### Test FastAPI Endpoints

```bash
python test_fastapi_agent.py
```

### Docker (Optional)

From `Travel_Agent/`:

```bash
docker-compose up --build
```

Service will be available on `http://localhost:8000`.

---

## Notebooks and Learning Modules

Use these folders for experimentation and learning:

- `Agent-Database-Interaction/explore/`: SQL connection tests, query chain tests, tabular DB experiments.
- `RAG/`: RAG fundamentals and chatbot examples.
- `Memory/`: vector database and memory concepts.
- `tools/`: agent tool integration examples.
- `image_geration/`: image generation and speech notebooks.

Suggested approach:

1. Run product code first (`src/app.py` or `fastapi_travel_agent.py`).
2. Use notebooks to inspect behavior and test ideas.

## Environment Variables

Different projects read different environment variables.

### Agent-Database-Interaction (from `load_config.py` + configs)

Required values typically include:

- `OPENAI_API_KEY`
- `OPENAI_API_BASE`
- `OPENAI_API_VERSION`
- `gpt_deployment_name`
- `embed_deployment_name`

### Travel_Agent

- `BASE_URL`
- `API_KEY`
- `MODEL_NAME`

Keep `.env` files local and never commit secrets.

## Troubleshooting

### 1) Import errors

- Ensure virtual environment is activated.
- Reinstall dependencies:

```bash
pip install -r requirements.txt
```

### 2) SQLite not found

- Install SQLite CLI or verify path with:

```bash
sqlite3 --version
```

### 3) API authentication/model errors

- Verify `.env` values and model availability.
- Confirm endpoint supports selected model name.

### 4) Chroma/vector issues

- Ensure `chromadb` installed.
- Verify `persist_directory` in `configs/app_config.yml`.

### 5) FastAPI server not reachable

- Check server logs.
- Verify port `8000` is free.
- Try: `http://localhost:8000/health`

## Recommended Onboarding Path

For a new team member, follow this order:

1. Read this root README.
2. Run `Agent-Database-Interaction/src/app.py` and complete one SQL and one RAG query.
3. Run `Travel_Agent/v1` to `v4` to understand agent evolution.
4. Run `Travel_Agent/fastapi_travel_agent.py` and test endpoints.
5. Explore relevant notebooks for deeper understanding.

## Security and Good Practices

- Never hardcode API keys or tokens in notebooks/scripts.
- Keep databases read-only when enabling LLM-generated SQL.
- Validate uploaded files before processing in production.
- Add tests for mission-critical paths before deployment.

## License

See subproject repositories and source files for license details.

