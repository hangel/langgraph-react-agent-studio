# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Frontend (React/Vite)
- `cd frontend && npm run dev` - Start frontend development server (port 5173)
- `cd frontend && npm run build` - Build frontend for production
- `cd frontend && npm run lint` - Run ESLint for frontend code

### Backend (Python/LangGraph)
- `cd backend && langgraph dev` - Start backend development server (port 2024)
- `cd backend && ruff check` - Run linting (configured in pyproject.toml)
- `cd backend && ruff format` - Format Python code

### Full Stack Development
- `make dev` - Start both frontend and backend servers concurrently
- `make dev-frontend` - Start only frontend
- `make dev-backend` - Start only backend

### Docker Deployment
- `docker build -t langgraph-agent-studio -f Dockerfile .` - Build production image
- `GEMINI_API_KEY=<key> docker-compose up` - Run with Docker Compose

### Testing
- `cd backend && pytest` - Run backend tests

## Architecture Overview

This is a full-stack AI agent platform with React frontend and LangGraph-powered Python backend.

### Key Components

**Frontend (`frontend/src/`)**
- `App.tsx` - Main application with LangGraph stream integration and agent state management
- `components/ChatMessagesView.tsx` - Chat interface and message display
- `components/ActivityTimeline.tsx` - Real-time agent activity visualization
- `components/InputForm.tsx` - User input handling with agent/model selection
- `lib/agents.ts` - Agent configuration and validation
- `types/` - TypeScript type definitions for agents, messages, tools

**Backend (`backend/src/agent/`)**
- `app.py` - FastAPI application serving static frontend and mounting LangGraph API
- `chatbot_graph.py` - Basic conversational agent
- `deep_researcher.py` - Multi-step research agent with web search and reflection
- `math_agent.py` - Mathematical calculation agent
- `mcp_agent.py` - Model Context Protocol integration agent
- `state.py` - TypedDict state classes for different agents
- `tools_and_schemas.py` - Pydantic models for tool inputs/outputs

**Infrastructure**
- Redis - pub/sub for real-time streaming
- PostgreSQL - agent state persistence and task queuing
- LangGraph API - agent execution framework

### Agent System

The platform supports 4 specialized agents defined in `backend/langgraph.json`:
- `chatbot` - General conversation
- `deep_researcher` - Iterative web research with reflection
- `math_agent` - Mathematical calculations
- `mcp_agent` - External tool integration via MCP

Each agent is a LangGraph StateGraph with different capabilities and state management.

### MCP Integration

Model Context Protocol servers provide external tool access:
- `@modelcontextprotocol/server-filesystem` - File system operations
- `@modelcontextprotocol/server-brave-search` - Web search capabilities
- Configuration via environment variables (MCP_FILESYSTEM_ENABLED, MCP_BRAVE_SEARCH_ENABLED)

### Environment Configuration

Required: `GEMINI_API_KEY`
Optional: `LANGSMITH_API_KEY`, `BRAVE_API_KEY`, MCP server configs

### URL Configuration

Frontend connects to backend at:
- Development: `http://localhost:2024`
- Production: `http://localhost:8123`

Update `apiUrl` in `frontend/src/App.tsx` for different deployments.

### State Management

- Agent state persisted in PostgreSQL
- Real-time updates via Redis pub/sub
- Thread management for conversation continuity
- Activity timeline for agent thought process visualization

### Adding New Agents

1. Create new agent graph in `backend/src/agent/`
2. Add entry to `backend/langgraph.json`
3. Update `frontend/src/lib/agents.ts` and types
4. Add activity timeline processing in `App.tsx` if needed