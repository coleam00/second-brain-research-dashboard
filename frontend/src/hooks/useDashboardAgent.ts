/**
 * Custom hook for interacting with the Second Brain dashboard agent.
 *
 * Uses CopilotKit's useCoAgent for bidirectional state synchronization
 * with the Pydantic AI backend via AG-UI protocol.
 */

import { useCoAgent, useCoAgentStateRender } from "@copilotkit/react-core";
import { useMemo, useCallback, useState, useEffect, useRef } from "react";
import type { A2UIComponent, SemanticZone } from "@/lib/a2ui-catalog";

/**
 * Dashboard state synchronized with backend agent.
 * Must match DashboardState in agent/agent.py
 */
export interface DashboardState {
  markdown_content: string;
  document_title: string;
  document_type: string;
  content_analysis: Record<string, any>;
  layout_type: string;
  components: A2UIComponent[];
  status: "idle" | "analyzing" | "generating" | "complete" | "error";
  progress: number;
  current_step: string;
  activity_log: Array<{
    id: string;
    message: string;
    timestamp: string;
    status: "in_progress" | "completed" | "error";
  }>;
  error_message: string | null;
}

/**
 * Initial state for the dashboard agent.
 */
const initialState: DashboardState = {
  markdown_content: "",
  document_title: "",
  document_type: "",
  content_analysis: {},
  layout_type: "",
  components: [],
  status: "idle",
  progress: 0,
  current_step: "",
  activity_log: [],
  error_message: null,
};

/**
 * Group components by semantic zone for layout.
 */
function groupByZone(components: A2UIComponent[]): Record<SemanticZone, A2UIComponent[]> {
  const groups: Record<SemanticZone, A2UIComponent[]> = {
    hero: [],
    metrics: [],
    insights: [],
    content: [],
    media: [],
    resources: [],
    tags: [],
  };

  for (const comp of components) {
    const zone = (comp.zone as SemanticZone) || "content";
    if (groups[zone]) {
      groups[zone].push(comp);
    } else {
      groups.content.push(comp);
    }
  }

  return groups;
}

/**
 * Hook for dashboard agent interaction using direct AG-UI SSE connection.
 *
 * Provides:
 * - state: Current dashboard state (synced with backend)
 * - componentsByZone: Components grouped by semantic zone
 * - generateDashboard: Trigger dashboard generation
 * - isGenerating: Whether generation is in progress
 */
export function useDashboardAgent() {
  const [state, setState] = useState<DashboardState>(initialState);
  const abortControllerRef = useRef<AbortController | null>(null);

  // Group components by zone for rendering
  const componentsByZone = useMemo(
    () => groupByZone(state.components),
    [state.components]
  );

  // Convenience function to start generation
  const generateDashboard = useCallback(async (markdown: string) => {
    // Cancel any existing request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    const abortController = new AbortController();
    abortControllerRef.current = abortController;

    // Reset state
    setState({
      ...initialState,
      markdown_content: markdown,
      status: "analyzing",
      progress: 0,
      activity_log: [],
    });

    const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

    try {
      const response = await fetch(`${backendUrl}/agent`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'text/event-stream',
        },
        body: JSON.stringify({
          state: { markdown_content: markdown },
        }),
        signal: abortController.signal,
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No response body');
      }

      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');

        // Keep the last incomplete line in the buffer
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('event:')) {
            // Parse event type (not used currently, but available)
            continue;
          }
          if (line.startsWith('data:')) {
            const data = line.slice(5).trim();
            if (data === '[DONE]') continue;

            try {
              const event = JSON.parse(data);
              handleAgUIEvent(event, setState);
            } catch (e) {
              console.warn('Failed to parse SSE event:', data);
            }
          }
        }
      }
    } catch (error: any) {
      if (error.name === 'AbortError') {
        console.log('Request aborted');
        return;
      }
      console.error('Dashboard generation error:', error);
      setState(prev => ({
        ...prev,
        status: 'error',
        error_message: error.message,
      }));
    }
  }, []);

  // Derived state
  const isGenerating = state.status === "analyzing" || state.status === "generating";
  const isComplete = state.status === "complete";
  const hasError = state.status === "error";

  return {
    state,
    setState,
    componentsByZone,
    generateDashboard,
    isGenerating,
    isComplete,
    hasError,
  };
}

/**
 * Handle AG-UI protocol events and update state accordingly.
 */
function handleAgUIEvent(
  event: any,
  setState: React.Dispatch<React.SetStateAction<DashboardState>>
) {
  switch (event.type) {
    case 'RunStarted':
      console.log('[AG-UI] Run started:', event.runId);
      break;

    case 'StateSnapshot':
      console.log('[AG-UI] State snapshot received');
      if (event.snapshot) {
        setState(prev => ({
          ...prev,
          ...event.snapshot,
        }));
      }
      break;

    case 'StateDelta':
      console.log('[AG-UI] State delta:', event.delta?.length, 'operations');
      if (event.delta && Array.isArray(event.delta)) {
        setState(prev => applyJsonPatches(prev, event.delta));
      }
      break;

    case 'TextMessageContent':
      // Could be used for streaming text messages
      console.log('[AG-UI] Text:', event.textDelta);
      break;

    case 'RunFinished':
      console.log('[AG-UI] Run finished');
      break;

    default:
      console.log('[AG-UI] Unknown event type:', event.type);
  }
}

/**
 * Apply JSON Patch operations (RFC 6902) to state.
 */
function applyJsonPatches(
  state: DashboardState,
  patches: Array<{ op: string; path: string; value?: any }>
): DashboardState {
  // Create a deep copy of the state
  const newState = JSON.parse(JSON.stringify(state)) as DashboardState;

  for (const patch of patches) {
    const { op, path, value } = patch;
    const pathParts = path.split('/').filter(p => p !== '');

    try {
      switch (op) {
        case 'replace':
          setNestedValue(newState, pathParts, value);
          break;
        case 'add':
          if (path.endsWith('/-')) {
            // Add to array
            const arrayPath = pathParts.slice(0, -1);
            const arr = getNestedValue(newState, arrayPath);
            if (Array.isArray(arr)) {
              arr.push(value);
            }
          } else {
            setNestedValue(newState, pathParts, value);
          }
          break;
        case 'remove':
          const parentPath = pathParts.slice(0, -1);
          const key = pathParts[pathParts.length - 1];
          const parent = getNestedValue(newState, parentPath);
          if (Array.isArray(parent)) {
            parent.splice(parseInt(key), 1);
          } else if (parent && typeof parent === 'object') {
            delete parent[key];
          }
          break;
      }
    } catch (e) {
      console.warn('Failed to apply patch:', patch, e);
    }
  }

  return newState;
}

/**
 * Get nested value from object by path parts.
 */
function getNestedValue(obj: any, pathParts: string[]): any {
  let current = obj;
  for (const part of pathParts) {
    if (current === null || current === undefined) return undefined;
    current = current[part];
  }
  return current;
}

/**
 * Set nested value in object by path parts.
 */
function setNestedValue(obj: any, pathParts: string[], value: any): void {
  let current = obj;
  for (let i = 0; i < pathParts.length - 1; i++) {
    const part = pathParts[i];
    if (current[part] === undefined) {
      current[part] = {};
    }
    current = current[part];
  }
  current[pathParts[pathParts.length - 1]] = value;
}

/**
 * Hook to render agent state in chat/activity UI.
 *
 * Use this to show real-time activity updates as the agent
 * processes the document.
 */
export function useDashboardStateRender() {
  // This hook would integrate with CopilotKit's state rendering
  // For now, it's a placeholder that could be extended
  return null;
}
