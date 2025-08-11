---
runme:
  document:
    relativePath: base_architecture.md
  session:
    id: 01K2DKBXC998YHWFGGQKD7EQQF
    updated: 2025-08-11 17:19:19-05:00
---

# Base Architecture

The LangGraph React Agent Studio is a full-stack AI agent platform designed for extensibility and real-time interaction. It leverages a modern, scalable architecture that separates concerns across several layers.

## Overall System Diagram

![Architecture Overview](../../architecture.png)

## Architecture Layers

The platform is composed of the following key architectural layers:

1. **Frontend Layer**:

   * **Technology**: Built with
      * React,
      * TypeScript,
      * Tailwind CSS, and
      * Radix UI.

   * __Purpose____**: Provides a _rich, interactive user interface_ for interacting with AI agents. It _handles real-time streaming of agent responses and activity timelines_.
   * **Key Components**:
      * `App.tsx` (main application logic, state management, LangGraph stream integration),
      * `ChatMessagesView.tsx` (displays conversation),
      * `InputForm.tsx` (user input),
      * `ActivityTimeline.tsx` (agent thought process visualization), and
      * a suite of reusable UI components (`ui/`).

2. **Backend Layer**:

   * **Technology**: Developed using
      * Python
      * FastAPI
      * LangGraph
   * **Purpose**: Hosts the AI agents, manages their execution, and provides
      * `REST` and
      * `WebSocket`
      endpoints for communication with the frontend. It also serves the `static frontend assets` in production.
   * **Key Components**:
      * `**app.py**`: The main FastAPI application, responsible for mounting the frontend and handling API routes.
      * `**langgraph-api**` (base image): Provides the core LangGraph API functionalities.
      * Agent-specific graphs (e.g.,

         * `chatbot_graph.py`,
         * `deep_researcher.py`,
         * `math_agent.py`,
         * `mcp_agent.py`):
         Define the logic and flow for each specialized AI agent using __LangGraph's `StateGraph`__.

   * `state.py`: Defines the `TypedDict` classes that represent the state of different agents, managing how information is passed between nodes.
   * `tools_and_schemas.py`: Contains Pydantic models for defining tool inputs/outputs and other structured data used by agents.

3. **Infrastructure Layer**:

   * `**Redis**`: Used as a pub-sub broker to enable real-time streaming of output from background agent runs to the frontend.
   * `**PostgreSQL**`: Serves as the primary data store for persisting agent state, threads, runs, and managing the background task queue with "exactly once" semantics. It also stores assistants.

4. **MCP (Model Context Protocol) Layer**:

   * **Purpose**: Integrates external tools and services with the AI agents using the Model Context Protocol.
   * **Key Components**:

      * `@modelcontextprotocol/server-filesystem`: Enables agents to interact with the filesystem (read/write files, directory operations) in a sandboxed environment.
      * `@modelcontextprotocol/server-brave-search`: Provides web search capabilities for agents, including search result processing and citation tracking.
      * `langchain-mcp-adapters`: Python library facilitating the integration of MCP servers with LangChain tools.

5. **External Services**:
   * __LLM AI Providers__: Primarily Google Gemini (configured via `GEMINI_API_KEY`).
   * __Monitoring__: LangSmith (optional, configured via `LANGSMITH_API_KEY`) for observability and tracing of agent runs.
   * **Third-party API Integrations**: Any other external APIs that agents might interact with via custom tools.

## Deployment Overview

The application is designed for Dockerized deployment.

* **Development**: `make dev` command starts the frontend (Vite dev server) and backend (FastAPI dev server) separately.
* **Production (Docker Compose)**:
   * The `Dockerfile` builds the React frontend and then incorporates it into the backend image.
   * `docker-compose.yml` orchestrates the `langgraph-redis`, `langgraph-postgres`, and `langgraph-api` services.
   * The `langgraph-api` service serves the static frontend assets and exposes the backend API.
   * Environment variables (e.g., `GEMINI_API_KEY`, `REDIS_URI`, `POSTGRES_URI`) are used for configuration.
