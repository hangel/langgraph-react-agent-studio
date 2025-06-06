export interface Agent {
  id: string;
  name: string;
  description: string;
  icon: string;
  capabilities: string[];
  showActivityTimeline: boolean;
}

export const AVAILABLE_AGENTS: Agent[] = [
  {
    id: 'agent',
    name: 'Research Agent',
    description: 'Deep research with web search and reflection',
    icon: 'search',
    capabilities: ['Web Research', 'Deep Research'],
    showActivityTimeline: true,
  },
  {
    id: 'chatbot',
    name: 'Chat Assistant',
    description: 'Simple conversational assistant',
    icon: 'message-circle',
    capabilities: ['General Chat', 'Quick Responses'],
    showActivityTimeline: false,
  },
];
