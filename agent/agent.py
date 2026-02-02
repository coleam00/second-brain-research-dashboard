"""
Second Brain Agent - Pydantic AI agent with AG-UI protocol support.

This agent uses StateDeps for bidirectional state sync with the frontend
and emits proper AG-UI events for streaming components.
"""

import os
from typing import Any, Literal
from uuid import uuid4
from datetime import datetime

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel


# JSON Patch operation model (RFC 6902)
class JSONPatchOp(BaseModel):
    """JSON Patch operation for state updates."""
    op: Literal["add", "remove", "replace", "move", "copy", "test"]
    path: str
    value: Any = None
    from_: str | None = Field(default=None, alias="from")


class DashboardState(BaseModel):
    """
    Shared state between frontend and agent.

    This state is synchronized bidirectionally via AG-UI protocol.
    The frontend can read and update this state, and the agent
    can emit StateSnapshot/StateDelta events to update it.
    """
    # Document info
    markdown_content: str = ""
    document_title: str = ""
    document_type: str = ""  # tutorial, research, article, etc.

    # Analysis results
    content_analysis: dict[str, Any] = Field(default_factory=dict)
    layout_type: str = ""  # instructional, data, news, etc.

    # Generated components (A2UI format)
    components: list[dict[str, Any]] = Field(default_factory=list)

    # Processing status
    status: str = "idle"  # idle, analyzing, generating, complete, error
    progress: int = 0  # 0-100
    current_step: str = ""

    # Activity log for frontend rendering
    activity_log: list[dict[str, Any]] = Field(default_factory=list)

    # Error tracking
    error_message: str | None = None


def create_openrouter_model() -> OpenAIModel:
    """Create OpenRouter model instance."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable required")

    model_name = os.getenv("OPENROUTER_MODEL", "anthropic/claude-sonnet-4")
    os.environ["OPENROUTER_API_KEY"] = api_key
    return OpenAIModel(model_name, provider='openrouter')


def create_agent() -> Agent[DashboardState, str]:
    """
    Create the Second Brain agent with DashboardState dependencies.

    The agent uses DashboardState for state management and
    synchronization with the frontend.
    """
    model = create_openrouter_model()

    agent = Agent(
        model=model,
        deps_type=DashboardState,
        output_type=str,
        system_prompt="""You are a specialized AI assistant that transforms Markdown research documents into interactive dashboard components.

Your workflow:
1. Analyze the markdown content to understand its structure and type
2. Select an optimal layout strategy based on the content
3. Generate A2UI components that best represent the information

Always use your tools in sequence:
1. First call analyze_content() to understand the document
2. Then call select_layout() to choose the best layout
3. Finally call generate_dashboard_components() to create the UI

Respond conversationally while using tools to do the actual work."""
    )

    # Tool: Analyze Content
    @agent.tool
    async def analyze_content(
        ctx: RunContext[DashboardState],
    ) -> str:
        """
        Analyze the markdown content to determine document type and extract key elements.

        This tool updates the shared state with analysis results.
        """
        from content_analyzer import parse_markdown
        from llm_orchestrator import analyze_content_with_llm

        state = ctx.deps
        markdown = state.markdown_content

        # Update state to show we're analyzing
        state.status = "analyzing"
        state.progress = 20
        state.current_step = "Analyzing document structure..."
        state.activity_log.append({
            "id": str(uuid4()),
            "message": "Starting content analysis",
            "timestamp": datetime.now().isoformat(),
            "status": "in_progress"
        })

        # Parse markdown structure
        parsed = parse_markdown(markdown)

        # Get LLM analysis
        analysis = await analyze_content_with_llm(markdown)

        # Update state with results
        state.document_title = parsed.get("title", "Untitled")
        state.document_type = analysis.get("document_type", "article")
        state.content_analysis = {
            **parsed,
            **analysis
        }
        state.progress = 40
        state.activity_log.append({
            "id": str(uuid4()),
            "message": f"Document classified as: {analysis.get('document_type', 'article')}",
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        })

        return f"Content analyzed. Document type: {state.document_type}, Title: {state.document_title}"

    # Tool: Select Layout
    @agent.tool
    async def select_layout(
        ctx: RunContext[DashboardState],
    ) -> str:
        """
        Select the optimal layout strategy based on content analysis.

        Layout types: instructional, data, news, list, summary, resource, media
        """
        from llm_orchestrator import select_layout_with_llm

        state = ctx.deps

        state.current_step = "Selecting optimal layout..."
        state.progress = 50

        # Get layout recommendation from LLM
        layout_result = await select_layout_with_llm(state.content_analysis)
        layout_type = layout_result.get("layout_type", "content")

        state.layout_type = layout_type
        state.progress = 60
        state.activity_log.append({
            "id": str(uuid4()),
            "message": f"Selected layout: {layout_type}",
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        })

        return f"Layout selected: {layout_type}"

    # Tool: Generate Dashboard Components
    @agent.tool
    async def generate_dashboard_components(
        ctx: RunContext[DashboardState],
    ) -> str:
        """
        Generate A2UI dashboard components based on analysis and layout.

        This tool creates the actual UI components that will be rendered
        by the frontend's A2UI catalog.
        """
        from llm_orchestrator import (
            select_components_with_llm,
            build_a2ui_component,
            apply_layout_and_zone,
            expand_component_specs
        )

        state = ctx.deps

        # Initial progress update
        state.status = "generating"
        state.current_step = "Generating dashboard components..."
        state.progress = 70
        state.components = []  # Clear existing

        # Get component specifications from LLM
        component_specs = await select_components_with_llm(
            state.content_analysis,
            {"layout_type": state.layout_type},
            state.markdown_content
        )

        # Expand batch specs (e.g., ProConItem batches)
        expanded_specs = expand_component_specs(component_specs)

        # Build each component
        total = len(expanded_specs)
        components_built = 0

        for i, spec in enumerate(expanded_specs):
            component = build_a2ui_component(spec, state.content_analysis)
            if component is None:
                continue

            apply_layout_and_zone(component, spec)

            # Convert to dict for state
            component_dict = {
                "type": component.type,
                "id": component.id,
                "props": component.props,
                "layout": component.layout,
                "zone": component.zone
            }

            # Add component to state
            state.components.append(component_dict)
            components_built += 1

            # Update progress
            state.progress = 70 + int((i / total) * 25)

        # Final completion update
        state.status = "complete"
        state.progress = 100
        state.current_step = "Dashboard complete!"
        state.activity_log.append({
            "id": str(uuid4()),
            "message": f"Generated {components_built} components",
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        })

        return f"Generated {components_built} A2UI components for the dashboard"

    return agent


# Initialize agent (lazy loading)
_agent_instance = None


def get_agent() -> Agent[DashboardState, str]:
    """Get or create the agent instance."""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = create_agent()
    return _agent_instance
