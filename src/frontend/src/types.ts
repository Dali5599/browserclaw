export interface Session {
  id: string;
  task: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'paused';
  mode: 'strict' | 'monitor' | 'permissive';
  createdAt: string;
  updatedAt: string;
  startedAt?: string;
  completedAt?: string;
  tokensUsed: number;
  cost: number;
  steps: number;
  currentUrl?: string;
  viewport?: ViewportSnapshot;
  actions: Action[];
  thoughts: Thought[];
}

export interface ViewportSnapshot {
  width: number;
  height: number;
  frameBase64: string;
  timestamp: string;
  boundingBoxes?: BoundingBox[];
}

export interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
  selector: string;
  tagName: string;
  text?: string;
  isInteractive: boolean;
}

export interface Action {
  id: string;
  sessionId: string;
  type: 'click' | 'type' | 'navigate' | 'scroll' | 'wait' | 'extract' | 'screenshot' | 'evaluate';
  target: string;
  params: Record<string, unknown>;
  status: 'pending' | 'running' | 'completed' | 'failed';
  startedAt: string;
  completedAt?: string;
  duration?: number;
  error?: string;
  result?: unknown;
  screenshot?: string;
}

export interface Thought {
  id: string;
  sessionId: string;
  content: string;
  timestamp: string;
  type: 'reasoning' | 'observation' | 'plan' | 'decision' | 'error';
  step: number;
}

export interface TokenStats {
  totalTokens: number;
  promptTokens: number;
  completionTokens: number;
  totalCost: number;
  sessionsCount: number;
}

export interface AgentConfig {
  mode: 'strict' | 'monitor' | 'permissive';
  maxSteps: number;
  timeout: number;
  headless: boolean;
  viewport: {
    width: number;
    height: number;
  };
}

export interface WSMessage {
  type: 'viewport' | 'thought' | 'action' | 'session_update' | 'session_complete' | 'error' | 'stats';
  payload: unknown;
  timestamp: string;
}

export interface StartSessionRequest {
  task: string;
  mode: 'strict' | 'monitor' | 'permissive';
  config?: Partial<AgentConfig>;
}

export interface SessionListItem {
  id: string;
  task: string;
  status: Session['status'];
  mode: Session['mode'];
  createdAt: string;
  completedAt?: string;
  tokensUsed: number;
  cost: number;
  steps: number;
}