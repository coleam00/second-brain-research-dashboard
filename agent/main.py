"""
Second Brain Agent - FastAPI application with AG-UI protocol endpoint.

This agent transforms Markdown research documents into generative UI dashboards
using Pydantic AI and the AG-UI protocol with proper event streaming.
"""

import os
import json
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our agent and state
from agent import get_agent, DashboardState

# Import the LLM-powered orchestrator for component generation
from llm_orchestrator import orchestrate_dashboard_with_llm

# Configuration
BACKEND_PORT = int(os.getenv("BACKEND_PORT", "8000"))
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-sonnet-4")


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    version: str
    agent_ready: bool


class AgentRequest(BaseModel):
    """AG-UI RunAgentInput compatible request model."""
    # AG-UI standard fields
    threadId: str | None = None
    runId: str | None = None
    messages: list[dict] | None = None
    state: dict | None = None

    # Legacy fields for backward compatibility
    markdown: str | None = None
    user_id: str | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    print(f"[*] Second Brain Agent starting on port {BACKEND_PORT}")
    print(f"[*] AG-UI endpoint: http://localhost:{BACKEND_PORT}/agent")
    print(f"[*] Legacy endpoint: http://localhost:{BACKEND_PORT}/ag-ui/stream")

    if not OPENROUTER_API_KEY:
        print("[!] WARNING: OPENROUTER_API_KEY not set")
    else:
        # Pre-initialize agent
        try:
            get_agent()
            print("[+] Pydantic AI agent initialized")
        except Exception as e:
            print(f"[-] Agent init failed: {e}")

    yield
    print("Second Brain Agent shutting down")


app = FastAPI(
    title="Second Brain Agent",
    description="AG-UI compliant agent for generative dashboards",
    version="0.2.0",
    lifespan=lifespan,
)

# CORS - Allow all for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version="0.2.0",
        agent_ready=OPENROUTER_API_KEY is not None,
    )


def emit_ag_ui_event(event_type: str, data: dict) -> str:
    """Format an AG-UI protocol event as SSE."""
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"


@app.post("/agent")
async def agent_endpoint(request: AgentRequest) -> StreamingResponse:
    """
    AG-UI protocol endpoint with proper event streaming.

    This endpoint accepts AG-UI RunAgentInput and returns a streaming
    response with proper AG-UI events (RunStarted, StateSnapshot,
    StateDelta, TextMessageContent, ToolCall*, RunFinished).

    The frontend's markdown content is passed via:
    - state.markdown_content (AG-UI standard)
    - markdown field (legacy support)
    """
    if not OPENROUTER_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OPENROUTER_API_KEY not configured",
        )

    # Extract markdown from either new or legacy format
    markdown_content = ""
    if request.state and "markdown_content" in request.state:
        markdown_content = request.state["markdown_content"]
    elif request.markdown:
        markdown_content = request.markdown

    if not markdown_content or not markdown_content.strip():
        raise HTTPException(
            status_code=400,
            detail="Markdown content is required",
        )

    # Generate IDs if not provided
    thread_id = request.threadId or str(uuid4())
    run_id = request.runId or str(uuid4())

    async def event_generator() -> AsyncGenerator[str, None]:
        """Generate AG-UI protocol events."""
        try:
            # Emit RunStarted
            yield emit_ag_ui_event("RunStarted", {
                "type": "RunStarted",
                "threadId": thread_id,
                "runId": run_id,
            })

            # Create initial state
            state = DashboardState(markdown_content=markdown_content)

            # Emit StateSnapshot (initial state)
            yield emit_ag_ui_event("StateSnapshot", {
                "type": "StateSnapshot",
                "snapshot": state.model_dump(),
            })

            # Process with orchestrator and emit StateDelta events
            print(f"\n[AGENT] Starting dashboard generation for {len(markdown_content)} chars")

            # Update state to analyzing
            state.status = "analyzing"
            state.progress = 10
            state.current_step = "Starting analysis..."

            yield emit_ag_ui_event("StateDelta", {
                "type": "StateDelta",
                "delta": [
                    {"op": "replace", "path": "/status", "value": "analyzing"},
                    {"op": "replace", "path": "/progress", "value": 10},
                    {"op": "replace", "path": "/current_step", "value": "Starting analysis..."},
                ]
            })

            # Use the LLM orchestrator to generate components
            component_count = 0
            async for component in orchestrate_dashboard_with_llm(markdown_content):
                component_count += 1

                # Convert component to dict
                component_dict = {
                    "type": component.type,
                    "id": component.id,
                    "props": component.props,
                }
                if component.layout:
                    component_dict["layout"] = component.layout
                if component.zone:
                    component_dict["zone"] = component.zone

                # Add to state
                state.components.append(component_dict)

                # Calculate progress (components usually happen at 70-95%)
                progress = min(70 + (component_count * 2), 95)

                # Emit StateDelta for new component
                yield emit_ag_ui_event("StateDelta", {
                    "type": "StateDelta",
                    "delta": [
                        {"op": "add", "path": "/components/-", "value": component_dict},
                        {"op": "replace", "path": "/progress", "value": progress},
                        {"op": "replace", "path": "/status", "value": "generating"},
                        {"op": "replace", "path": "/current_step", "value": f"Generated {component.type}"},
                    ]
                })

                # Also emit as TextMessageContent for chat-like display
                yield emit_ag_ui_event("TextMessageContent", {
                    "type": "TextMessageContent",
                    "textDelta": f"Generated {component.type} component\n",
                })

            # Emit final state update
            yield emit_ag_ui_event("StateDelta", {
                "type": "StateDelta",
                "delta": [
                    {"op": "replace", "path": "/status", "value": "complete"},
                    {"op": "replace", "path": "/progress", "value": 100},
                    {"op": "replace", "path": "/current_step", "value": "Dashboard complete!"},
                    {"op": "add", "path": "/activity_log/-", "value": {
                        "id": str(uuid4()),
                        "message": f"Generated {component_count} components",
                        "timestamp": __import__('datetime').datetime.now().isoformat(),
                        "status": "completed"
                    }}
                ]
            })

            # Emit RunFinished
            yield emit_ag_ui_event("RunFinished", {
                "type": "RunFinished",
                "threadId": thread_id,
                "runId": run_id,
            })

            print(f"[AGENT] Complete - generated {component_count} components")

        except Exception as e:
            import traceback
            print(f"[AGENT ERROR] {e}")
            traceback.print_exc()

            # Emit error event
            yield emit_ag_ui_event("StateDelta", {
                "type": "StateDelta",
                "delta": [
                    {"op": "replace", "path": "/status", "value": "error"},
                    {"op": "replace", "path": "/error_message", "value": str(e)},
                ]
            })

            yield emit_ag_ui_event("RunFinished", {
                "type": "RunFinished",
                "threadId": thread_id,
                "runId": run_id,
            })

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# Legacy endpoint for backward compatibility
@app.post("/ag-ui/stream")
async def legacy_stream(request: AgentRequest) -> StreamingResponse:
    """
    Legacy endpoint that streams components directly.

    This maintains backward compatibility with the existing frontend
    while transitioning to the new AG-UI protocol.
    """
    if not OPENROUTER_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="OPENROUTER_API_KEY not configured",
        )

    # Extract markdown
    markdown_content = ""
    if request.state and "markdown_content" in request.state:
        markdown_content = request.state["markdown_content"]
    elif request.markdown:
        markdown_content = request.markdown

    if not markdown_content or not markdown_content.strip():
        raise HTTPException(
            status_code=400,
            detail="Markdown content is required",
        )

    async def event_generator() -> AsyncGenerator[str, None]:
        """Generate SSE events with components."""
        try:
            print(f"\n[LEGACY] Starting dashboard generation")

            component_count = 0
            async for component in orchestrate_dashboard_with_llm(markdown_content):
                component_count += 1

                component_dict = {
                    "type": component.type,
                    "id": component.id,
                    "props": component.props,
                }
                if component.layout:
                    component_dict["layout"] = component.layout
                if component.zone:
                    component_dict["zone"] = component.zone

                yield f"data: {json.dumps(component_dict)}\n\n"

            yield f"data: [DONE]\n\n"
            print(f"[LEGACY] Complete - {component_count} components")

        except Exception as e:
            import traceback
            traceback.print_exc()
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/")
async def root():
    return {
        "name": "Second Brain Agent",
        "version": "0.2.0",
        "endpoints": {
            "health": "/health",
            "agent": "/agent (POST, AG-UI protocol)",
            "legacy": "/ag-ui/stream (POST, legacy SSE)",
        },
        "documentation": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=BACKEND_PORT, reload=True)
