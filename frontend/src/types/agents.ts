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
    id: 'deep_researcher',
    name: 'Deep Researcher',
    description: 'Advanced deep research with enhanced analysis',
    icon: 'search',
    capabilities: ['Advanced Web Research', 'Deep Analysis'],
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
