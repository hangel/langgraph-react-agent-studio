# Architecture Key Components Role

This document details the specific roles and responsibilities of key files and modules within the LangGraph React Agent Studio, providing a deeper understanding of their contribution to the overall architecture.

## Backend Key Components

### `backend/src/agent/app.py`
*   **Role**: The main FastAPI application entry point.
*   **Responsibilities**:
    *   Initializes and configures the FastAPI application.
    *   Mounts the React frontend's static build under the `/app` path, allowing the backend to serve the UI.
    *   Implicitly handles the routing for LangGraph API endpoints, as it builds upon the `langgraph-api` base image.

### `backend/src/agent/state.py`
*   **Role**: Defines the shared state structures for different LangGraph agents.
*   **Responsibilities**:
    *   Declares `TypedDict` classes (e.g., `OverallState`, `ChatbotState`, `MathAgentState`, `ReflectionState`, `QueryGenerationState`, `WebSearchState`, `SearchStateOutput`) that represent the data schema for each agent's state.
    *   Utilizes `Annotated` with `langgraph.graph.add_messages` and `operator.add` to define how messages are appended and how lists are combined within the state, enabling seamless state management across agent nodes.
    *   Crucial for defining the information flow and persistence within an agent's execution.

### `backend/src/agent/chatbot_graph.py` (Example Agent)
*   **Role**: Implements the logic and flow for the basic conversational chatbot agent.
*   **Responsibilities**:
    *   Defines a `StateGraph` using `ChatbotState` to orchestrate the agent's workflow.
    *   Contains the `chat_response` node, which uses `langchain_google_genai.ChatGoogleGenerativeAI` to interact with the Gemini LLM.
    *   Manages conversation context by passing message history to the LLM.
    *   Serves as a foundational example for how to construct new LangGraph agents.

### `backend/src/agent/deep_researcher.py`, `backend/src/agent/math_agent.py`, `backend/src/agent/mcp_agent.py`
*   **Role**: Implement the logic and specific workflows for their respective specialized agents.
*   **Responsibilities**:
    *   Each file defines its own `StateGraph` and nodes tailored to its domain (e.g., web research, mathematical calculations, MCP tool integration).
    *   They interact with various tools and LLMs as required by their specific tasks.

### `backend/src/agent/tools_and_schemas.py`
*   **Role**: Defines Pydantic models for structured data used by agents, particularly for tool inputs/outputs and reflection mechanisms.
*   **Responsibilities**:
    *   Declares `BaseModel` classes (e.g., `SearchQueryList`, `Reflection`) that enforce data validation and provide clear interfaces for agent interactions with tools or for structured reasoning outputs.

### `backend/src/agent/prompts.py`
*   **Role**: Stores the prompt templates used by the LLMs within the agents.
*   **Responsibilities**:
    *   Centralizes the definition of system instructions, user prompts, and other textual inputs that guide the LLM's behavior and responses.

### `backend/src/agent/configuration.py`
*   **Role**: Manages configuration settings for agents, such as LLM models and temperature.
*   **Responsibilities**:
    *   Provides a structured way to define and access agent-specific parameters, allowing for easy customization without modifying core agent logic.

## Frontend Key Components

### `frontend/src/App.tsx`
*   **Role**: The root component of the React application, managing global state and orchestrating UI interactions.
*   **Responsibilities**:
    *   Manages application-wide state, including the selected agent, live activity timeline events, and historical activities.
    *   Integrates with the LangGraph backend using the `@langchain/langgraph-sdk/react` `useStream` hook for real-time communication.
    *   Processes incoming events from the LangGraph stream (`onUpdateEvent`) to update the activity timeline, providing visual feedback on agent progress.
    *   Handles user input submission (`handleSubmit`), dynamically adjusting parameters based on the selected agent.
    *   Conditionally renders the `WelcomeScreen` or `ChatMessagesView` based on the conversation state.

### `frontend/src/main.tsx`
*   **Role**: The entry point for the React application.
*   **Responsibilities**:
    *   Renders the `App` component into the DOM.
    *   Sets up `StrictMode` for development and `BrowserRouter` for client-side routing.

### `frontend/src/components/ChatMessagesView.tsx`
*   **Role**: Displays the main conversation interface.
*   **Responsibilities**:
    *   Renders the list of messages exchanged between the user and the AI agent.
    *   Integrates `InputForm` for new messages, `ToolMessageDisplay` for tool-related outputs, and `ActivityTimeline` for agent process visualization.

### `frontend/src/components/InputForm.tsx`
*   **Role**: Provides the user input interface.
*   **Responsibilities**:
    *   Captures user messages, selected agent, effort level, and model choice.
    *   Triggers the `handleSubmit` function in `App.tsx` to send input to the backend.

### `frontend/src/components/ActivityTimeline.tsx`
*   **Role**: Visualizes the step-by-step thought process and actions of the AI agent.
*   **Responsibilities**:
    *   Displays the `processedEventsTimeline` data, providing real-time updates on agent activities like query generation, web research, reflection, and tool execution.

### `frontend/src/components/ToolMessageDisplay.tsx`
*   **Role**: Renders specific messages related to tool execution.
*   **Responsibilities**:
    *   Presents the output or status of tools invoked by the AI agents in a user-friendly format.

### `frontend/src/components/WelcomeScreen.tsx`
*   **Role**: The initial screen displayed when the application starts with no active conversation.
*   **Responsibilities**:
    *   Provides an introductory interface for users to select an agent and start a new conversation.

### `frontend/src/components/ui/` (UI Primitives)
*   **Role**: A collection of reusable, styled UI components.
*   **Responsibilities**:
    *   Provides foundational UI elements (e.g., `button`, `input`, `card`, `select`, `tabs`) built with Radix UI and styled with Tailwind CSS.
    *   Ensures consistent look and feel across the application and accelerates UI development.
