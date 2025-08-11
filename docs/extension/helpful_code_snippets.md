# Helpful Code Snippets for Extending the Architecture

This document provides a collection of reusable code snippets to assist in extending the LangGraph React Agent Studio's functionality, covering both frontend and backend aspects.

## Backend Snippets

### 1. Defining a New LangGraph Agent State

To introduce new data that needs to persist and be passed between nodes in your LangGraph agent, define a new `TypedDict` in `backend/src/agent/state.py`.

```python
# backend/src/agent/state.py
from typing import TypedDict
from langgraph.graph import add_messages
from typing_extensions import Annotated
import operator

class MyNewAgentState(TypedDict):
    messages: Annotated[list, add_messages] # Standard for conversation history
    my_custom_string: str # A new string field
    my_custom_list: Annotated[list, operator.add] # A list that accumulates
    my_custom_boolean: bool = False # A boolean with a default value
```

### 2. Creating a New LangGraph Node

Nodes are the building blocks of your agent's graph. They perform specific actions and update the agent's state. Place new nodes in your agent's graph file (e.g., `backend/src/agent/your_agent_graph.py`).

```python
# backend/src/agent/your_agent_graph.py
from langchain_core.messages import AIMessage
from agent.state import MyNewAgentState # Import your custom state

def my_new_node(state: MyNewAgentState) -> MyNewAgentState:
    """A new node that processes custom data and updates the state."""
    current_string = state.get("my_custom_string", "")
    updated_string = f"Processed: {current_string}"

    # Simulate some logic, e.g., calling an LLM or a tool
    # llm_response = llm.invoke("some prompt")

    return {
        "messages": [AIMessage(content="Node executed successfully!")],
        "my_custom_string": updated_string,
        "my_custom_list": ["new_item_from_node"],
        "my_custom_boolean": True,
    }
```

### 3. Integrating a Custom Tool with LangChain

To allow your agents to interact with external services or perform specific actions, define a LangChain tool. This typically involves a Python function decorated with `@tool` and an optional Pydantic schema for structured input.

```python
# backend/src/tools/my_custom_tool.py
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# Optional: Define a schema for structured input
class MyCustomToolInput(BaseModel):
    item_name: str = Field(description="The name of the item to process.")
    quantity: int = Field(description="The quantity of the item.")

@tool("my_custom_tool", args_schema=MyCustomToolInput)
def my_custom_tool(item_name: str, quantity: int) -> str:
    """A new tool that processes an item with a given quantity and returns a status.

    This tool simulates an external API call or a complex operation.
    """
    if quantity <= 0:
        return "Error: Quantity must be positive."
    # Simulate processing
    result = f"Successfully processed {quantity} of {item_name}."
    return result

# To use in an agent:
# from backend.src.tools.my_custom_tool import my_custom_tool
# llm_with_tools = llm.bind_functions([convert_to_openai_function(my_custom_tool)])
```

### 4. Adding a New LLM Model Configuration

If you want to easily switch between different LLM models or configurations, you can extend `backend/src/agent/configuration.py`.

```python
# backend/src/agent/configuration.py
from dataclasses import dataclass
from langchain_core.runnables import RunnableConfig

@dataclass(kw_only=True)
class MyNewAgentConfiguration:
    model_name: str = "gemini-pro"
    temperature: float = 0.7
    # Add any other configuration parameters specific to your agent or LLM
    max_tokens: int = 1024

    @classmethod
    def from_runnable_config(cls, config: RunnableConfig) -> "MyNewAgentConfiguration":
        return cls(
            model_name=config.get("configurable", {}).get("model_name", cls.model_name),
            temperature=config.get("configurable", {}).get("temperature", cls.temperature),
            max_tokens=config.get("configurable", {}).get("max_tokens", cls.max_tokens),
        )
```

## Frontend Snippets

### 1. Creating a New UI Component (Radix UI + Tailwind CSS)

For consistent styling and accessibility, use Radix UI primitives and Tailwind CSS utility classes. Place these in `frontend/src/components/ui/`.

```typescript
// frontend/src/components/ui/info-box.tsx
import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const infoBoxVariants = cva(
  "rounded-md border p-4 text-sm",
  {
    variants: {
      variant: {
        default: "bg-blue-50 border-blue-200 text-blue-800 dark:bg-blue-950 dark:border-blue-800 dark:text-blue-200",
        warning: "bg-yellow-50 border-yellow-200 text-yellow-800 dark:bg-yellow-950 dark:border-yellow-800 dark:text-yellow-200",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
);

interface InfoBoxProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof infoBoxVariants> {}

const InfoBox = React.forwardRef<HTMLDivElement, InfoBoxProps>(
  ({ className, variant, ...props }, ref) => (
    <div
      ref={ref}
      role="alert"
      className={cn(infoBoxVariants({ variant }), className)}
      {...props}
    />
  )
);
InfoBox.displayName = "InfoBox";

export { InfoBox };
```

### 2. Fetching Data from a New Backend Endpoint

When you expose a new API endpoint from the backend, you'll need to call it from the frontend. Define types and a utility function.

```typescript
// frontend/src/types/api_responses.ts
export interface MyNewApiResponse {
  message: string;
  data: any;
}

// frontend/src/lib/api_client.ts
const API_BASE_URL = import.meta.env.DEV
  ? 'http://localhost:2024'
  : 'http://localhost:8123';

export async function fetchMyNewData(): Promise<MyNewApiResponse> {
  const response = await fetch(`${API_BASE_URL}/api/my-new-data`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
}

// In a React component (e.g., MyComponent.tsx)
import React, { useEffect, useState } from 'react';
import { fetchMyNewData } from '@/lib/api_client';
import { MyNewApiResponse } from '@/types/api_responses';

const MyComponent: React.FC = () => {
  const [data, setData] = useState<MyNewApiResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchMyNewData()
      .then(response => {
        setData(response);
      })
      .catch(err => {
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      <h1>Data from Backend:</h1>
      <p>{data?.message}</p>
      <pre>{JSON.stringify(data?.data, null, 2)}</pre>
    </div>
  );
};

export default MyComponent;
```

### 3. Extending Agent Selection in Frontend

When you add a new agent to the backend, you need to make it selectable in the frontend by updating `frontend/src/lib/agents.ts`.

```typescript
// frontend/src/lib/agents.ts
export enum AgentId {
  DEEP_RESEARCHER = 'deep_researcher',
  CHATBOT = 'chatbot',
  MATH_AGENT = 'math_agent',
  MCP_AGENT = 'mcp_agent',
  MY_NEW_AGENT = 'my_new_agent', // Add your new agent ID here
}

export interface AgentConfig {
  id: AgentId;
  name: string;
  description: string;
  icon: string; // Emoji or path to an icon
  showActivityTimeline: boolean;
  showEffort: boolean;
  showModel: boolean;
}

export const AGENTS: AgentConfig[] = [
  // ... existing agents
  {
    id: AgentId.MY_NEW_AGENT,
    name: 'My Custom Agent',
    description: 'A specialized agent for custom tasks.',
    icon: '🤖',
    showActivityTimeline: true,
    showEffort: false,
    showModel: true,
  },
];

export const DEFAULT_AGENT = AgentId.CHATBOT;

export function getAgentById(id: AgentId): AgentConfig | undefined {
  return AGENTS.find((agent) => agent.id === id);
}

export function isValidAgentId(id: string): id is AgentId {
  return Object.values(AgentId).includes(id as AgentId);
}
```

These snippets provide practical examples for common extension scenarios, helping developers quickly integrate new features into the LangGraph React Agent Studio. 