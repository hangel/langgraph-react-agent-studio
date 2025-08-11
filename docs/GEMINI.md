# Project Overview

This is the LangGraph React Agent Studio, a powerful and extensible full-stack AI agent platform. It is designed to facilitate the creation and interaction with multiple specialized AI agents, featuring real-time streaming of agent thought processes and responses.

**Key Technologies:**
*   **Backend**: Python, FastAPI, LangGraph, LangChain, Google Gemini API, `langchain-mcp-adapters`.
*   **Frontend**: React, TypeScript, Vite, Tailwind CSS, Radix UI.
*   **Infrastructure**: Docker, Docker Compose, PostgreSQL (for state persistence and task queuing), Redis (for pub/sub streaming).
*   **Tooling**: Model Context Protocol (MCP) for external tool integration (Filesystem, Brave Search).

## Building and Running

### Prerequisites
*   Node.js 18+ and npm
*   Python 3.8+
*   Gemini API Key

### Local Development Setup

1.  **Configure Environment Variables:**
    ```bash
    cd backend
    cp .env.example .env
    # Edit .env to set GEMINI_API_KEY and optional MCP/LangSmith keys
    ```

2.  **Install Dependencies:**
    *   **Backend:**
        ```bash
        cd backend && uv sync
        ```
    *   **Frontend:**
        ```bash
        cd frontend && npm install
        ```
    *   **Global MCP Servers (optional, for local MCP tool usage):**
        ```bash
        npm install -g @modelcontextprotocol/server-filesystem @modelcontextprotocol/server-brave-search
        ```

3.  **Launch Development Servers:**
    From the project root directory:
    ```bash
    make dev
    # This runs both frontend (http://localhost:5173/app) and backend (http://localhost:2024) concurrently.
    # Alternatively, run them separately:
    # make dev-frontend
    # make dev-backend
    ```

### Docker Deployment

1.  **Build the Docker Image:**
    From the project root directory:
    ```bash
    docker build -t langgraph-agent-studio -f Dockerfile .
    ```

2.  **Run with Docker Compose:**
    From the project root directory (ensure `GEMINI_API_KEY` and `LANGSMITH_API_KEY` are set in your shell environment or `.env` file):
    ```bash
    GEMINI_API_KEY=<your_gemini_api_key> LANGSMITH_API_KEY=<your_langsmith_api_key> docker-compose up
    ```
    Access the application at `http://localhost:8123/app/` (API at `http://localhost:8123`).

## Development Conventions

*   **Code Structure**: The project is organized into `backend/` (Python FastAPI/LangGraph) and `frontend/` (React/TypeScript) directories, promoting clear separation of concerns.
*   **Agent Orchestration**: LangGraph's `StateGraph` is used extensively in the backend (`backend/src/agent/`) to define and manage the flow of specialized AI agents.
*   **Type Safety**: TypeScript is used in the frontend, and Python type hints are encouraged in the backend, enforced by `mypy`.
*   **Code Formatting & Linting**:
    *   **Python**: `ruff` is configured for linting and formatting (see `backend/pyproject.toml`).
    *   **JavaScript/TypeScript**: `eslint` is used for linting (see `frontend/package.json`).
*   **UI Components**: Frontend UI is built using Radix UI primitives and styled with Tailwind CSS, ensuring consistency and accessibility.
*   **Documentation**: Comprehensive architectural and extension documentation is available in the `docs/` directory, providing guidelines for contributing and extending the platform.
