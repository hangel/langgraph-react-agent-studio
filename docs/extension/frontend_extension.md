# Frontend Extension

Extending the frontend of the LangGraph React Agent Studio involves adding new UI components, integrating with new backend endpoints, and enhancing existing functionalities. The frontend is built with React, TypeScript, Tailwind CSS, and Radix UI.

## 1. Adding New UI Components

To add a new UI component, follow the existing patterns in `frontend/src/components/` and `frontend/src/components/ui/`.

*   **For reusable, atomic UI elements (e.g., buttons, cards, inputs)**: Create them within `frontend/src/components/ui/`. Leverage Radix UI primitives for accessibility and unstyled components, and apply Tailwind CSS for styling. Ensure they are generic and can be used across different parts of the application.

    **Example (`frontend/src/components/ui/new_component.tsx`):**
    ```typescript
    // Example: A simple custom alert component
    import * as React from "react";
    import { cva, type VariantProps } from "class-variance-authority";
    import { cn } from "@/lib/utils";

    const alertVariants = cva(
      "relative w-full rounded-lg border p-4 [&>svg~*]:pl-7 [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-foreground",
      {
        variants: {
          variant: {
            default: "bg-background text-foreground",
            destructive: "border-destructive/50 text-destructive dark:border-destructive [&>svg]:text-destructive",
          },
        },
        defaultVariants: {
          variant: "default",
        },
      }
    );

    interface AlertProps
      extends React.HTMLAttributes<HTMLDivElement>,
        VariantProps<typeof alertVariants> {}

    const Alert = React.forwardRef<HTMLDivElement, AlertProps>(
      ({ className, variant, ...props }, ref) => (
        <div
          ref={ref}
          role="alert"
          className={cn(alertVariants({ variant }), className)}
          {...props}
        />
      )
    );
    Alert.displayName = "Alert";

    const AlertTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
      ({ className, ...props }, ref) => (
        <h5
          ref={ref}
          className={cn("mb-1 font-medium leading-none tracking-tight", className)}
          {...props}
        />
      )
    );
    AlertTitle.displayName = "AlertTitle";

    const AlertDescription = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLParagraphElement>>(
      ({ className, ...props }, ref) => (
        <div
          ref={ref}
          className={cn("text-sm [&_p]:leading-relaxed", className)}
          {...props}
        />
      )
    );
    AlertDescription.displayName = "AlertDescription";

    export { Alert, AlertTitle, AlertDescription };
    ```

*   **For composite components (e.g., `ChatMessagesView`, `InputForm`)**: Create them directly within `frontend/src/components/`. These components typically combine multiple `ui/` primitives and handle more complex UI logic and state.

    **Example (`frontend/src/components/NewFeatureDisplay.tsx`):**
    ```typescript
    import React from 'react';
    import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
    import { Button } from './ui/button';

    interface NewFeatureDisplayProps {
      featureName: string;
      onActivate: () => void;
    }

    export const NewFeatureDisplay: React.FC<NewFeatureDisplayProps> = ({
      featureName,
      onActivate,
    }) => {
      return (
        <Card className="w-full max-w-md mx-auto">
          <CardHeader>
            <CardTitle>Introducing: {featureName}</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col items-center gap-4">
            <p>Click the button below to activate this exciting new feature!</p>
            <Button onClick={onActivate}>Activate {featureName}</Button>
          </CardContent>
        </Card>
      );
    };
    ```

## 2. Integrating with New Backend Endpoints

When you add new functionality to the backend that requires frontend interaction, you'll need to define new API calls and potentially new data types.

1.  **Define Types**: Create or extend types in `frontend/src/types/` to match the data structures expected from your new backend endpoints.

    **Example (`frontend/src/types/new_data.ts`):**
    ```typescript
    export interface NewBackendResponse {
      status: string;
      data: { key: string; value: any };
    }

    export interface NewBackendRequest {
      input: string;
      options?: Record<string, any>;
    }
    ```

2.  **Create API Utility Functions**: In `frontend/src/lib/`, create new functions or extend existing ones (e.g., `agents.ts`, `models.ts`) to make API calls to your new backend endpoints. Use `fetch` or a library like `axios` if introduced.

    **Example (`frontend/src/lib/api_service.ts`):**
    ```typescript
    import { NewBackendRequest, NewBackendResponse } from '@/types/new_data';

    const API_BASE_URL = import.meta.env.DEV
      ? 'http://localhost:2024'
      : 'http://localhost:8123';

    export async function callNewBackendEndpoint(
      requestData: NewBackendRequest
    ): Promise<NewBackendResponse> {
      const response = await fetch(`${API_BASE_URL}/api/new-endpoint`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return response.json();
    }
    ```

3.  **Integrate into Components**: Call these new utility functions from your React components (e.g., `App.tsx`, `ChatMessagesView.tsx`, or a new component) to fetch and display data.

    **Example (in a React component):**
    ```typescript
    import React, { useState } from 'react';
    import { callNewBackendEndpoint } from '@/lib/api_service';
    import { NewBackendRequest, NewBackendResponse } from '@/types/new_data';

    export const MyComponentWithNewApi: React.FC = () => {
      const [data, setData] = useState<NewBackendResponse | null>(null);
      const [loading, setLoading] = useState(false);
      const [error, setError] = useState<string | null>(null);

      const fetchData = async () => {
        setLoading(true);
        setError(null);
        try {
          const request: NewBackendRequest = { input: "example" };
          const response = await callNewBackendEndpoint(request);
          setData(response);
        } catch (err) {
          setError(err.message);
        } finally {
          setLoading(false);
        }
      };

      return (
        <div>
          <button onClick={fetchData} disabled={loading}>
            {loading ? "Loading..." : "Fetch New Data"}
          </button>
          {error && <p className="text-red-500">Error: {error}</p>}
          {data && (
            <div>
              <h3>New Data:</h3>
              <pre>{JSON.stringify(data, null, 2)}</pre>
            </div>
          )}
        </div>
      );
    };
    ```

## 3. Extending Existing Frontend Logic

Modifying existing logic often involves updating state management, event handling, or how data is processed from the LangGraph stream.

*   **Modifying `App.tsx`**: For changes affecting the overall application flow, agent selection, or how stream events are processed, `App.tsx` is the place to modify. For example, if you introduce a new event type from the backend, you would extend the `onUpdateEvent` logic.

    **Example (extending `onUpdateEvent` in `App.tsx` for a new event type):**
    ```typescript
    // ... inside onUpdateEvent callback in App.tsx
    if (selectedAgentId === AgentId.YOUR_NEW_AGENT) {
      if (
        'your_new_event' in event &&
        event.your_new_event &&
        typeof event.your_new_event === 'object'
      ) {
        const newEventData = event.your_new_event as { some_field: string };
        processedEvent = {
          title: 'New Agent Activity',
          data: `Processed new event with data: ${newEventData.some_field}`,
        };
      }
    }
    // ... rest of the onUpdateEvent logic
    ```

*   **Modifying `ChatMessagesView.tsx`**: For changes related to how messages are displayed or how sub-components (like `InputForm`, `ActivityTimeline`) interact within the chat view, modify this component.

*   **Updating `frontend/src/lib/agents.ts`**: If you add a new agent to the backend, you'll need to update the `AgentId` enum and the `AGENTS` array in this file to make it selectable in the frontend.

    **Example (`frontend/src/lib/agents.ts`):**
    ```typescript
    export enum AgentId {
      DEEP_RESEARCHER = 'deep_researcher',
      CHATBOT = 'chatbot',
      MATH_AGENT = 'math_agent',
      MCP_AGENT = 'mcp_agent',
      NEW_AGENT = 'new_agent', // Add your new agent ID here
    }

    export const AGENTS: AgentConfig[] = [
      // ... existing agents
      {
        id: AgentId.NEW_AGENT,
        name: 'My New Agent',
        description: 'A description of what your new agent does.',
        icon: '✨', // Choose an appropriate icon
        showActivityTimeline: true, // Or false, depending on your agent
        showEffort: false, // Or true
        showModel: false, // Or true
      },
    ];

    // ... rest of the file
    ```

## 4. Styling with Tailwind CSS

All styling is done using Tailwind CSS. When creating or modifying components:

*   Apply utility classes directly in your JSX (`className="flex items-center justify-between"`).
*   Refer to the [Tailwind CSS documentation](https://tailwindcss.com/docs) for available classes.
*   For conditional styling, use `clsx` and `tailwind-merge` (already configured in `frontend/src/lib/utils.ts`) to combine classes effectively.

    **Example:**
    ```typescript
    import { cn } from "@/lib/utils";

    <div className={cn(
      "p-4 rounded-md",
      isActive ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-800"
    )}>
      Hello
    </div>
    ```

By following these guidelines, you can effectively extend the frontend of the LangGraph React Agent Studio while maintaining consistency and adherence to the established architecture. 