# Backend Extension

Extending the backend of the LangGraph React Agent Studio primarily involves adding new agents, integrating new tools, and potentially incorporating new data sources or LLM routing mechanisms. The backend is built with Python, FastAPI, and LangGraph.

## 1. Adding New Agents

To add a new specialized agent, you will typically create a new Python file in `backend/src/agent/` and define its LangGraph `StateGraph`.

1.  **Define Agent State**: Create a new `TypedDict` in `backend/src/agent/state.py` to define the state specific to your new agent. This state will hold all the information passed between nodes in your agent's graph.

    **Example (`backend/src/agent/state.py`):**
    ```python
    from typing import TypedDict
    from langgraph.graph import add_messages
    from typing_extensions import Annotated
    import operator

    class NewAgentState(TypedDict):
        messages: Annotated[list, add_messages] # Standard for conversation history
        # Add other state variables specific to your agent
        custom_data: str
    ```

2.  **Create Agent Graph File**: Create a new Python file (e.g., `backend/src/agent/new_agent.py`) for your agent. In this file, define the nodes and edges of your agent's `StateGraph`.

    **Example (`backend/src/agent/new_agent.py`):**
    ```python
    import os
    from dotenv import load_dotenv
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langgraph.graph import END, START, StateGraph
    from langchain_core.messages import AIMessage, HumanMessage

    from agent.state import NewAgentState # Import your new state
    # from agent.tools_and_schemas import YourToolSchema # If using custom tools

    load_dotenv()

    if os.getenv("GEMINI_API_KEY") is None:
        raise ValueError("GEMINI_API_KEY is not set")

    # Define your agent's nodes
    def initial_node(state: NewAgentState) -> NewAgentState:
        print("Executing initial node...")
        return {"messages": [AIMessage(content="Hello from New Agent!")], "custom_data": "initial_value"}

    def processing_node(state: NewAgentState) -> NewAgentState:
        print(f"Processing custom data: {state['custom_data']}")
        # Example: Interact with LLM or use a tool
        llm = ChatGoogleGenerativeAI(model="gemini-pro", api_key=os.getenv("GEMINI_API_KEY"))
        response = llm.invoke(f"Process this: {state['messages'][-1].content}")
        return {"messages": [AIMessage(content=response.content)], "custom_data": "processed_value"}

    # Build the graph
    builder = StateGraph(NewAgentState)
    builder.add_node("initial_node", initial_node)
    builder.add_node("processing_node", processing_node)

    builder.add_edge(START, "initial_node")
    builder.add_edge("initial_node", "processing_node")
    builder.add_edge("processing_node", END)

    new_agent_graph = builder.compile(name="new-agent")
    ```

3.  **Register Agent in `app.py`**: Update the `LANGSERVE_GRAPHS` environment variable (or its equivalent in `app.py` if directly configured) to include your new agent's graph. In the Dockerfile, this is done via `ENV LANGSERVE_GRAPHS`.

    **Example (conceptual update for `LANGSERVE_GRAPHS`):**
    ```python
    # In Dockerfile or similar configuration
    ENV LANGSERVE_GRAPHS='{"deep_researcher": "/deps/backend/src/agent/deep_researcher.py:deep_researcher_graph", "chatbot": "/deps/backend/src/agent/chatbot_graph.py:chatbot_graph", "mcp_agent": "/deps/backend/src/agent/mcp_agent.py:mcp_agent_graph", "math_agent": "/deps/backend/src/agent/math_agent.py:math_agent_graph", "new_agent": "/deps/backend/src/agent/new_agent.py:new_agent_graph"}'
    ```

4.  **Update Frontend**: As described in `frontend_extension.md`, update `frontend/src/lib/agents.ts` to include your new agent's ID and configuration so it appears in the UI.

## 2. Integrating New Tools

LangGraph agents can leverage LangChain tools. To add a new tool:

1.  **Define Tool Schema**: If your tool requires structured input, define a Pydantic `BaseModel` in `backend/src/agent/tools_and_schemas.py`.

    **Example (`backend/src/agent/tools_and_schemas.py`):**
    ```python
    from pydantic import BaseModel, Field

    class MyNewToolInput(BaseModel):
        query: str = Field(description="The query for my new tool.")
        # Add other fields as needed
    ```

2.  **Implement Tool Function**: Create the Python function that performs the tool's action. This can be in `backend/src/agent/tools_and_schemas.py` or a new file in `backend/src/tools/`.

    **Example (`backend/src/tools/my_new_tool.py`):**
    ```python
    from langchain_core.tools import tool
    from backend.src.agent.tools_and_schemas import MyNewToolInput

    @tool("my_new_tool", args_schema=MyNewToolInput)
    def my_new_tool(item_name: str, quantity: int) -> str:
        """A new tool that processes an item with a given quantity and returns a string result."""
        # Implement your tool's logic here
        return f"Processed query: {query} with new tool."
    ```

3.  **Integrate Tool into Agent**: Import and use your tool within your agent's graph. You can bind it to an LLM or call it directly from a node.

    **Example (in `backend/src/agent/your_agent_graph.py`):**
    ```python
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.utils.function_calling import convert_to_openai_function
    from backend.src.tools.my_new_tool import my_new_tool

    # ... inside your agent's graph definition ...

    llm_with_tools = ChatGoogleGenerativeAI(model="gemini-pro", api_key=os.getenv("GEMINI_API_KEY"))
    llm_with_tools = llm_with_tools.bind_functions([convert_to_openai_function(my_new_tool)])

    # Then, in a node, you can invoke this LLM, and it might call your tool
    # Or, you can directly call the tool from a node:
    # result = my_new_tool.invoke({"query": "some input"})
    ```

## 3. New Databases

Integrating new databases involves setting up connection strings, defining ORM models (if using one), and updating relevant data access logic. The current setup uses PostgreSQL with LangGraph's built-in state persistence.

*   **Connection Configuration**: If you're adding a new database, you'll need to define its connection URI as an environment variable (e.g., in `.env` and `docker-compose.yml`).

    **Example (`.env` / `docker-compose.yml`):**
    ```
    NEW_DB_URI=postgresql://user:password@host:port/dbname
    ```

*   **Data Access Layer**: Create new Python modules (e.g., `backend/src/database/`) to encapsulate your database interactions. This could involve:
    *   Using an ORM like SQLAlchemy or FastAPI's SQLModel.
    *   Directly using a database driver (e.g., `psycopg2` for PostgreSQL, `pymongo` for MongoDB).

    **Example (conceptual `backend/src/database/new_db_models.py` with SQLAlchemy):**
    ```python
    from sqlalchemy import create_engine, Column, Integer, String
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker

    DATABASE_URL = os.getenv("NEW_DB_URI")
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    class NewDataItem(Base):
        __tablename__ = "new_data_items"
        id = Column(Integer, primary_key=True, index=True)
        name = Column(String, index=True)
        value = Column(String)

    Base.metadata.create_all(bind=engine)

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    ```

*   **Integration with Agents**: Agents can then interact with this new data access layer from their nodes to store or retrieve information.

## 4. LLM Routing / Selector

Implementing LLM routing or a selector allows your application to dynamically choose which LLM to use based on the user's query, agent state, or other criteria. This can be achieved within a LangGraph node.

*   **Decision Node**: Create a new node in your LangGraph agent that acts as a router. This node will analyze the input (e.g., user message, current state) and decide which LLM or sub-agent to route the request to.

    **Example (conceptual routing node in `backend/src/agent/your_agent_graph.py`):**
    ```python
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_openai import ChatOpenAI # Example for another LLM
    from langchain_core.messages import HumanMessage

    def llm_router(state: NewAgentState) -> str:
        last_message_content = state["messages"][-1].content

        if "math" in last_message_content.lower():
            return "use_math_llm"
        elif "creative" in last_message_content.lower():
            return "use_creative_llm"
        else:
            return "use_default_llm"

    def call_math_llm(state: NewAgentState) -> NewAgentState:
        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1)
        # ... logic to call math-optimized LLM ...
        response = llm.invoke(state["messages"])
        return {"messages": [AIMessage(content=response.content)]}

    def call_creative_llm(state: NewAgentState) -> NewAgentState:
        llm = ChatOpenAI(model="gpt-4", temperature=0.9) # Example
        # ... logic to call creative-optimized LLM ...
        response = llm.invoke(state["messages"])
        return {"messages": [AIMessage(content=response.content)]}

    def call_default_llm(state: NewAgentState) -> NewAgentState:
        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7)
        # ... logic to call default LLM ...
        response = llm.invoke(state["messages"])
        return {"messages": [AIMessage(content=response.content)]}

    # ... inside your agent's graph definition ...
    builder.add_node("llm_router", llm_router)
    builder.add_node("call_math_llm", call_math_llm)
    builder.add_node("call_creative_llm", call_creative_llm)
    builder.add_node("call_default_llm", call_default_llm)

    builder.add_edge(START, "llm_router")
    builder.add_conditional_edges(
        "llm_router",
        llm_router,
        {
            "use_math_llm": "call_math_llm",
            "use_creative_llm": "call_creative_llm",
            "use_default_llm": "call_default_llm",
        },
    )
    builder.add_edge("call_math_llm", END)
    builder.add_edge("call_creative_llm", END)
    builder.add_edge("call_default_llm", END)
    ```

*   **Configuration**: The choice of LLM can also be driven by configuration (e.g., environment variables, a dedicated config file like `backend/src/agent/configuration.py`). This allows for easy switching of models without code changes.

By following these guidelines, you can effectively extend the backend of the LangGraph React Agent Studio, adding new agents, tools, database integrations, and sophisticated LLM routing capabilities. 