"""
Second Brain Agent - Pydantic AI agent configuration with OpenRouter.

This module defines the core Pydantic AI agent that transforms Markdown research
documents into generative UI dashboards using Claude Sonnet 4 via OpenRouter.
"""

import os
from typing import Any
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel


class AgentState(BaseModel):
    """
    State model for the Second Brain Agent.

    Tracks the document content being analyzed and the analysis results
    throughout the agent's processing pipeline.
    """

    document_content: str = Field(
        description="The original Markdown content provided by the user"
    )

    content_type: str | None = Field(
        default=None,
        description="Detected content type (e.g., 'research', 'tutorial', 'article', 'notes')"
    )

    layout_type: str | None = Field(
        default=None,
        description="Optimal layout type selected (e.g., 'magazine', 'dashboard', 'tutorial')"
    )

    analysis_results: dict[str, Any] = Field(
        default_factory=dict,
        description="Extracted components and metadata from content analysis"
    )

    error_message: str | None = Field(
        default=None,
        description="Error message if processing fails"
    )


def create_openrouter_model(model_name: str, api_key: str) -> OpenAIModel:
    """
    Create an OpenRouter model instance configured for Claude Sonnet 4.

    OpenRouter uses OpenAI-compatible API, so we use OpenAIModel from Pydantic AI
    with the 'openrouter' provider.

    Args:
        model_name: The OpenRouter model identifier (e.g., "anthropic/claude-sonnet-4")
        api_key: OpenRouter API key

    Returns:
        Configured OpenAIModel instance
    """
    # Set the API key in environment for the provider to pick up
    os.environ["OPENROUTER_API_KEY"] = api_key
    return OpenAIModel(model_name, provider='openrouter')


# Create the agent instance
def create_agent() -> Agent[AgentState, str]:
    """
    Create and configure the Second Brain Pydantic AI agent.

    The agent uses Claude Sonnet 4 via OpenRouter to analyze Markdown content
    and generate dashboard layouts.

    Returns:
        Configured Pydantic AI Agent instance

    Raises:
        ValueError: If OPENROUTER_API_KEY is not set in environment
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY environment variable is required. "
            "Please set it in your .env file."
        )

    model_name = os.getenv("OPENROUTER_MODEL", "anthropic/claude-sonnet-4")

    # Create OpenRouter model instance
    model = create_openrouter_model(model_name, api_key)

    # Create agent with system prompt
    agent_instance = Agent(
        model=model,
        deps_type=AgentState,
        output_type=str,
        system_prompt=(
            "You are a specialized AI assistant that analyzes Markdown research documents "
            "and transforms them into structured dashboard layouts. Your role is to:\n"
            "1. Analyze the content type and structure of Markdown documents\n"
            "2. Extract key components (headlines, statistics, quotes, code blocks, etc.)\n"
            "3. Determine the optimal layout type for presenting the information\n"
            "4. Generate component definitions following the AG-UI protocol\n\n"
            "You should respond with structured data that can be used to build "
            "interactive, visual dashboards that make research documents more engaging "
            "and easier to navigate."
        ),
    )

    # Register tools
    @agent_instance.tool
    async def analyze_content_type(ctx: RunContext[AgentState], markdown_content: str) -> str:
        """
        Analyze the Markdown content to determine its type.

        This tool examines the structure, headers, and content patterns to classify
        the document as research, tutorial, article, notes, etc.

        Args:
            ctx: Agent context with state
            markdown_content: The Markdown content to analyze

        Returns:
            Content type classification (e.g., 'research', 'tutorial', 'article')
        """
        # Simple heuristic-based classification
        content_lower = markdown_content.lower()

        # Check for tutorial indicators
        if any(word in content_lower for word in ['step', 'tutorial', 'how to', 'guide', 'lesson']):
            content_type = 'tutorial'
        # Check for research indicators
        elif any(word in content_lower for word in ['abstract', 'methodology', 'results', 'conclusion', 'references']):
            content_type = 'research'
        # Check for code-heavy content
        elif markdown_content.count('```') >= 4:
            content_type = 'technical_guide'
        # Default to article
        else:
            content_type = 'article'

        # Update state
        ctx.deps.content_type = content_type

        return f"Content classified as: {content_type}"

    @agent_instance.tool
    async def extract_components(ctx: RunContext[AgentState], markdown_content: str) -> dict[str, Any]:
        """
        Extract key components from the Markdown content.

        This tool identifies and extracts headlines, statistics, quotes, code blocks,
        images, and other structural elements for dashboard rendering.

        Args:
            ctx: Agent context with state
            markdown_content: The Markdown content to analyze

        Returns:
            Dictionary of extracted components
        """
        import re

        components = {
            'headlines': [],
            'code_blocks': [],
            'quotes': [],
            'images': [],
            'statistics': [],
        }

        # Extract headlines (# headers)
        headlines = re.findall(r'^#+\s+(.+)$', markdown_content, re.MULTILINE)
        components['headlines'] = headlines[:5]  # Top 5 headlines

        # Extract code blocks
        code_blocks = re.findall(r'```(\w*)\n(.*?)```', markdown_content, re.DOTALL)
        components['code_blocks'] = [
            {'language': lang or 'text', 'code': code.strip()}
            for lang, code in code_blocks[:3]  # Top 3 code blocks
        ]

        # Extract blockquotes
        quotes = re.findall(r'^>\s+(.+)$', markdown_content, re.MULTILINE)
        components['quotes'] = quotes[:3]  # Top 3 quotes

        # Extract image references
        images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', markdown_content)
        components['images'] = [
            {'alt': alt, 'url': url}
            for alt, url in images[:5]  # Top 5 images
        ]

        # Extract potential statistics (numbers with context)
        stats = re.findall(r'\b(\d+(?:\.\d+)?%?)\s+(\w+)', markdown_content)
        components['statistics'] = [
            {'value': value, 'label': label}
            for value, label in stats[:5]  # Top 5 statistics
        ]

        # Update state
        ctx.deps.analysis_results = components

        return components

    return agent_instance


# Initialize the agent (will be imported by main.py)
# Only initialize if API key is available
try:
    agent = create_agent()
except ValueError as e:
    # Allow module to load even without API key for testing
    print(f"Warning: {e}")
    agent = None
