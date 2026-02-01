"""
A2UI Generator Module - Base infrastructure for A2UI component generation.

This module provides foundational functions for generating A2UI (Agent-to-UI) components
that comply with the A2UI v0.8 protocol specification. It includes the base component model,
ID generation, component emission, and factory functions.

A2UI Protocol Compliance:
- All components must have: type, id, props
- Type format: "a2ui.ComponentName" (e.g., "a2ui.StatCard")
- IDs must be unique within a component tree
- Props are component-specific key-value pairs
- Optional children field for layout components
"""

import uuid
import json
import re
from typing import Any, AsyncGenerator
from pydantic import BaseModel, Field, field_validator


class A2UIComponent(BaseModel):
    """
    Pydantic model for A2UI component specification.

    Represents a single UI component in the A2UI protocol format.
    All components must conform to this structure for proper rendering.

    Attributes:
        type: Component type identifier (e.g., "a2ui.StatCard", "a2ui.VideoCard")
        id: Unique identifier for this component instance
        props: Component-specific properties as a dictionary
        children: Optional list of child component IDs or nested structure for layouts

    Example:
        ```python
        component = A2UIComponent(
            type="a2ui.StatCard",
            id="stat-1",
            props={
                "value": "$196B",
                "label": "AI Market Size",
                "trend": "up",
                "trendValue": "+23%"
            }
        )
        ```
    """

    type: str = Field(
        description="A2UI component type (must start with 'a2ui.')",
        pattern=r"^a2ui\.[A-Z][a-zA-Z0-9]*$"
    )

    id: str = Field(
        description="Unique component identifier (kebab-case recommended)"
    )

    props: dict[str, Any] = Field(
        default_factory=dict,
        description="Component properties (component-specific)"
    )

    children: list[str] | dict[str, list[str]] | None = Field(
        default=None,
        description="Child component IDs (for layout components) or nested structure (for tabs/accordion)"
    )

    layout: dict[str, str] | None = Field(
        default=None,
        description="Layout hints for positioning: width ('full', 'half', 'third', 'quarter'), priority ('high', 'medium', 'low')"
    )

    zone: str | None = Field(
        default=None,
        description="Semantic zone for grouping: 'hero', 'metrics', 'insights', 'content', 'media', 'resources', 'tags'"
    )

    @field_validator('type')
    @classmethod
    def validate_type(cls, v: str) -> str:
        """Validate that type follows a2ui.ComponentName format."""
        if not v.startswith('a2ui.'):
            raise ValueError(f"Component type must start with 'a2ui.', got: {v}")
        return v

    @field_validator('id')
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Validate that ID is non-empty."""
        if not v or not v.strip():
            raise ValueError("Component ID cannot be empty")
        return v.strip()


# Component type registry - maps component types to validation rules
VALID_COMPONENT_TYPES = {
    # News & Trends
    "a2ui.HeadlineCard",
    "a2ui.TrendIndicator",
    "a2ui.TimelineEvent",
    "a2ui.NewsTicker",

    # Media
    "a2ui.VideoCard",
    "a2ui.ImageCard",
    "a2ui.PlaylistCard",
    "a2ui.PodcastCard",

    # Data & Statistics
    "a2ui.StatCard",
    "a2ui.MetricRow",
    "a2ui.ProgressRing",
    "a2ui.ComparisonBar",
    "a2ui.DataTable",
    "a2ui.MiniChart",

    # Lists & Rankings
    "a2ui.RankedItem",
    "a2ui.ChecklistItem",
    "a2ui.ProConItem",
    "a2ui.BulletPoint",

    # Resources & Links
    "a2ui.LinkCard",
    "a2ui.ToolCard",
    "a2ui.BookCard",
    "a2ui.RepoCard",

    # People & Entities
    "a2ui.ProfileCard",
    "a2ui.CompanyCard",
    "a2ui.QuoteCard",
    "a2ui.ExpertTip",

    # Summary & Overview
    "a2ui.TLDR",
    "a2ui.KeyTakeaways",
    "a2ui.ExecutiveSummary",
    "a2ui.TableOfContents",

    # Comparison
    "a2ui.ComparisonTable",
    "a2ui.VsCard",
    "a2ui.FeatureMatrix",
    "a2ui.PricingTable",

    # Instructional
    "a2ui.StepCard",
    "a2ui.CodeBlock",
    "a2ui.CalloutCard",
    "a2ui.CommandCard",

    # Layout
    "a2ui.Section",
    "a2ui.Grid",
    "a2ui.Columns",
    "a2ui.Tabs",
    "a2ui.Accordion",
    "a2ui.Carousel",
    "a2ui.Sidebar",

    # Tags & Categories
    "a2ui.TagCloud",
    "a2ui.CategoryBadge",
    "a2ui.DifficultyBadge",
    "a2ui.Tag",
    "a2ui.Badge",
    "a2ui.CategoryTag",
    "a2ui.StatusIndicator",
    "a2ui.PriorityBadge",
}


# ID counter for sequential IDs within a session
_id_counter = 0


def generate_id(component_type: str, prefix: str | None = None) -> str:
    """
    Generate a unique component ID.

    Creates unique IDs using either a prefix-based counter or UUID fallback.
    IDs follow kebab-case convention for consistency.

    Strategies:
    1. If prefix provided: "{prefix}-{counter}" (e.g., "stat-1", "video-2")
    2. If no prefix: extract from component type + counter (e.g., "stat-card-1")
    3. Fallback: UUID4 for guaranteed uniqueness

    Args:
        component_type: A2UI component type (e.g., "a2ui.StatCard")
        prefix: Optional custom prefix for the ID (e.g., "stat", "video")

    Returns:
        Unique component ID string

    Examples:
        >>> generate_id("a2ui.StatCard", "stat")
        "stat-1"
        >>> generate_id("a2ui.VideoCard")
        "video-card-1"
        >>> generate_id("a2ui.Section", "intro")
        "intro-1"
    """
    global _id_counter
    _id_counter += 1

    if prefix:
        return f"{prefix}-{_id_counter}"

    # Extract component name from type (a2ui.StatCard -> stat-card)
    if component_type.startswith("a2ui."):
        # Convert PascalCase to kebab-case
        name = component_type[5:]  # Remove "a2ui."
        # Insert hyphens before capital letters and convert to lowercase
        kebab_name = ''.join(['-' + c.lower() if c.isupper() else c for c in name]).lstrip('-')
        return f"{kebab_name}-{_id_counter}"

    # Fallback to UUID
    return f"component-{uuid.uuid4().hex[:8]}"


def reset_id_counter():
    """
    Reset the global ID counter.

    Useful for testing or when starting a new component generation session.
    This ensures IDs start from 1 again.
    """
    global _id_counter
    _id_counter = 0


def generate_component(
    component_type: str,
    props: dict[str, Any],
    component_id: str | None = None,
    children: list[str] | dict[str, list[str]] | None = None,
    layout: dict[str, str] | None = None
) -> A2UIComponent:
    """
    Generate a base A2UI component with validation.

    Factory function for creating A2UI components with automatic ID generation
    and type validation. Ensures all components conform to A2UI protocol.

    Args:
        component_type: A2UI component type (must be in VALID_COMPONENT_TYPES)
        props: Component properties dictionary
        component_id: Optional custom ID (auto-generated if not provided)
        children: Optional child component IDs for layout components
        layout: Optional layout hints (width, priority)

    Returns:
        A2UIComponent instance ready for emission

    Raises:
        ValueError: If component_type is not valid
        ValidationError: If props don't meet component requirements

    Examples:
        >>> component = generate_component(
        ...     "a2ui.StatCard",
        ...     {"value": "$196B", "label": "Market Size", "trend": "up"},
        ...     layout={"width": "third"}
        ... )
        >>> component.type
        "a2ui.StatCard"
        >>> component.id
        "stat-card-1"
    """
    # Validate component type
    if component_type not in VALID_COMPONENT_TYPES:
        raise ValueError(
            f"Invalid component type: {component_type}. "
            f"Must be one of: {', '.join(sorted(VALID_COMPONENT_TYPES))}"
        )

    # Generate ID if not provided
    if component_id is None:
        component_id = generate_id(component_type)

    # Create and validate component
    component = A2UIComponent(
        type=component_type,
        id=component_id,
        props=props,
        children=children,
        layout=layout
    )

    return component


async def emit_components(
    components: list[A2UIComponent],
    stream_format: str = "ag-ui"
) -> AsyncGenerator[str, None]:
    """
    Emit A2UI components in AG-UI streaming format.

    Converts A2UI components to Server-Sent Events (SSE) format for streaming
    to the frontend via the AG-UI protocol. Each component is sent as a separate
    event with proper SSE formatting.

    AG-UI Protocol Format:
    - Each event starts with "data: "
    - JSON payload contains component definition
    - Events separated by double newlines
    - Compatible with EventSource API on frontend

    Args:
        components: List of A2UIComponent instances to emit
        stream_format: Output format ("ag-ui" for SSE, "json" for plain JSON)

    Yields:
        Formatted event strings ready for SSE streaming

    Examples:
        >>> components = [
        ...     generate_component("a2ui.StatCard", {"value": "100", "label": "Users"}),
        ...     generate_component("a2ui.StatCard", {"value": "50", "label": "Active"})
        ... ]
        >>> async for event in emit_components(components):
        ...     print(event)
        data: {"type": "a2ui.StatCard", "id": "stat-card-1", ...}

        data: {"type": "a2ui.StatCard", "id": "stat-card-2", ...}
    """
    for component in components:
        # Convert component to dict for JSON serialization
        component_dict = component.model_dump(exclude_none=True)

        if stream_format == "ag-ui":
            # AG-UI SSE format: "data: {json}\n\n"
            json_str = json.dumps(component_dict)
            yield f"data: {json_str}\n\n"
        elif stream_format == "json":
            # Plain JSON (for testing or alternative protocols)
            yield json.dumps(component_dict) + "\n"
        else:
            raise ValueError(f"Unknown stream format: {stream_format}")


def validate_component_props(component_type: str, props: dict[str, Any]) -> bool:
    """
    Validate that component props contain required fields.

    Basic validation for common component types. Checks that required
    properties are present in the props dictionary.

    Note: This is a basic validator. Full validation should be handled
    by component-specific generator functions.

    Args:
        component_type: A2UI component type
        props: Component properties to validate

    Returns:
        True if props are valid, raises ValueError otherwise

    Raises:
        ValueError: If required props are missing
    """
    # Define required props for common components
    required_props = {
        "a2ui.StatCard": ["value", "label"],
        "a2ui.VideoCard": ["videoId", "platform"],
        "a2ui.HeadlineCard": ["title"],
        "a2ui.RankedItem": ["rank", "title"],
        "a2ui.CodeBlock": ["code", "language"],
        "a2ui.Section": ["title"],
        "a2ui.Grid": ["columns"],
        "a2ui.TLDR": ["summary"],
    }

    if component_type in required_props:
        missing = [prop for prop in required_props[component_type] if prop not in props]
        if missing:
            raise ValueError(
                f"{component_type} missing required props: {', '.join(missing)}"
            )

    return True


# Helper function for bulk component generation
def generate_components_batch(
    component_specs: list[tuple[str, dict[str, Any]]]
) -> list[A2UIComponent]:
    """
    Generate multiple components from specifications.

    Convenience function for creating many components at once from a list
    of (type, props) tuples.

    Args:
        component_specs: List of (component_type, props) tuples

    Returns:
        List of generated A2UIComponent instances

    Examples:
        >>> specs = [
        ...     ("a2ui.StatCard", {"value": "100", "label": "Users"}),
        ...     ("a2ui.StatCard", {"value": "50", "label": "Active"}),
        ...     ("a2ui.VideoCard", {"videoId": "abc123", "platform": "youtube"})
        ... ]
        >>> components = generate_components_batch(specs)
        >>> len(components)
        3
    """
    components = []
    for component_type, props in component_specs:
        component = generate_component(component_type, props)
        components.append(component)
    return components


# News Component Generators

def generate_headline_card(
    title: str,
    summary: str,
    source: str,
    published_at: str,
    sentiment: str = "neutral",
    image_url: str | None = None
) -> A2UIComponent:
    """
    Generate a HeadlineCard A2UI component for news articles.

    Creates a headline card component displaying news article information
    including title, summary, source, and optional sentiment/image.

    Args:
        title: Article headline/title
        summary: Brief article summary or excerpt
        source: News source name (e.g., "TechCrunch", "Reuters")
        published_at: Publication timestamp (ISO 8601 format recommended)
        sentiment: Sentiment indicator - "positive", "negative", or "neutral" (default)
        image_url: Optional URL to article thumbnail/hero image

    Returns:
        A2UIComponent configured as HeadlineCard

    Examples:
        >>> card = generate_headline_card(
        ...     title="AI Breakthrough Announced",
        ...     summary="Major advancement in natural language processing",
        ...     source="Tech Daily",
        ...     published_at="2026-01-30T10:00:00Z",
        ...     sentiment="positive"
        ... )
        >>> card.type
        "a2ui.HeadlineCard"
    """
    props = {
        "title": title,
        "summary": summary,
        "source": source,
        "publishedAt": published_at,
        "sentiment": sentiment,
    }

    if image_url:
        props["imageUrl"] = image_url

    return generate_component("a2ui.HeadlineCard", props)


def generate_trend_indicator(
    label: str,
    value: float,
    trend: str,
    change: float,
    unit: str = ""
) -> A2UIComponent:
    """
    Generate a TrendIndicator A2UI component for displaying trends.

    Creates a trend indicator showing a metric value, direction, and change amount.
    Useful for displaying market movements, statistics changes, etc.

    Args:
        label: Metric label/name (e.g., "Stock Price", "User Growth")
        value: Current metric value
        trend: Trend direction - "up", "down", or "stable"
        change: Amount of change (e.g., 5.2 for +5.2% or -5.2 for -5.2%)
        unit: Optional unit suffix (e.g., "%", "points", "USD")

    Returns:
        A2UIComponent configured as TrendIndicator

    Raises:
        ValueError: If trend is not "up", "down", or "stable"

    Examples:
        >>> indicator = generate_trend_indicator(
        ...     label="Market Cap",
        ...     value=2.5,
        ...     trend="up",
        ...     change=12.3,
        ...     unit="%"
        ... )
        >>> indicator.props["trend"]
        "up"
    """
    valid_trends = {"up", "down", "stable"}
    if trend not in valid_trends:
        raise ValueError(
            f"Invalid trend value: {trend}. Must be one of: {', '.join(valid_trends)}"
        )

    props = {
        "label": label,
        "value": value,
        "trend": trend,
        "change": change,
    }

    if unit:
        props["unit"] = unit

    return generate_component("a2ui.TrendIndicator", props)


def generate_timeline_event(
    title: str,
    timestamp: str,
    content: str,
    event_type: str = "article",
    icon: str | None = None
) -> A2UIComponent:
    """
    Generate a TimelineEvent A2UI component for timeline displays.

    Creates a timeline event entry with title, timestamp, content, and optional
    event type classification and icon.

    Args:
        title: Event title/headline
        timestamp: Event timestamp (ISO 8601 format recommended)
        content: Event description/details
        event_type: Event classification - "article", "announcement", "milestone", or "update"
        icon: Optional icon identifier for the event

    Returns:
        A2UIComponent configured as TimelineEvent

    Raises:
        ValueError: If event_type is not valid

    Examples:
        >>> event = generate_timeline_event(
        ...     title="Product Launch",
        ...     timestamp="2026-01-15T09:00:00Z",
        ...     content="New AI model released to public",
        ...     event_type="milestone"
        ... )
        >>> event.props["eventType"]
        "milestone"
    """
    valid_event_types = {"article", "announcement", "milestone", "update"}
    if event_type not in valid_event_types:
        raise ValueError(
            f"Invalid event_type: {event_type}. "
            f"Must be one of: {', '.join(valid_event_types)}"
        )

    props = {
        "title": title,
        "timestamp": timestamp,
        "content": content,
        "eventType": event_type,
    }

    if icon:
        props["icon"] = icon

    return generate_component("a2ui.TimelineEvent", props)


def generate_news_ticker(items: list[dict[str, str]]) -> A2UIComponent:
    """
    Generate a NewsTicker A2UI component for scrolling news updates.

    Creates a news ticker component displaying multiple brief news items
    in a scrolling or rotating format. Items should contain text, url, and timestamp.

    Args:
        items: List of news items, each with keys: "text", "url", "timestamp"
               Maximum 10 items recommended for performance

    Returns:
        A2UIComponent configured as NewsTicker with items as children

    Raises:
        ValueError: If items list is empty or exceeds 10 items
        ValueError: If items don't have required keys

    Examples:
        >>> ticker = generate_news_ticker([
        ...     {
        ...         "text": "Markets up 2% on strong earnings",
        ...         "url": "https://example.com/market-news",
        ...         "timestamp": "2026-01-30T10:00:00Z"
        ...     },
        ...     {
        ...         "text": "New AI regulation proposed",
        ...         "url": "https://example.com/ai-regulation",
        ...         "timestamp": "2026-01-30T09:30:00Z"
        ...     }
        ... ])
        >>> len(ticker.props["items"])
        2
    """
    if not items:
        raise ValueError("NewsTicker requires at least one item")

    if len(items) > 10:
        raise ValueError(
            f"NewsTicker supports up to 10 items, got {len(items)}. "
            "Consider using pagination for more items."
        )

    # Validate that all items have required keys
    required_keys = {"text", "url", "timestamp"}
    for i, item in enumerate(items):
        missing_keys = required_keys - set(item.keys())
        if missing_keys:
            raise ValueError(
                f"Item {i} missing required keys: {', '.join(missing_keys)}. "
                f"Required: text, url, timestamp"
            )

    props = {
        "items": items
    }

    return generate_component("a2ui.NewsTicker", props)


# Media Component Generators

def extract_youtube_id(url: str) -> str | None:
    """
    Extract YouTube video ID from various YouTube URL formats.

    Supports common YouTube URL formats including:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/v/VIDEO_ID
    - http://www.youtube.com/watch?v=VIDEO_ID (with or without www)

    Args:
        url: YouTube URL string to parse

    Returns:
        11-character video ID if valid YouTube URL, None otherwise

    Examples:
        >>> extract_youtube_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        "dQw4w9WgXcQ"
        >>> extract_youtube_id("https://youtu.be/dQw4w9WgXcQ")
        "dQw4w9WgXcQ"
        >>> extract_youtube_id("https://www.youtube.com/embed/dQw4w9WgXcQ")
        "dQw4w9WgXcQ"
        >>> extract_youtube_id("invalid-url")
        None
    """
    if not url:
        return None

    # Regex patterns for different YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/)([a-zA-Z0-9_-]{11})',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def generate_video_card(
    title: str,
    description: str,
    video_id: str | None = None,
    video_url: str | None = None,
    thumbnail_url: str | None = None,
    duration: str | None = None
) -> A2UIComponent:
    """
    Generate a VideoCard A2UI component for video content.

    Creates a video card component supporting both YouTube videos (via video_id)
    and generic video URLs. Automatically extracts video ID from YouTube URLs.

    Args:
        title: Video title
        description: Video description/summary
        video_id: YouTube video ID (11 characters, e.g., "dQw4w9WgXcQ")
        video_url: Generic video URL or YouTube URL (will auto-extract ID for YouTube)
        thumbnail_url: Optional thumbnail/preview image URL
        duration: Optional video duration (e.g., "5:23", "1:30:45")

    Returns:
        A2UIComponent configured as VideoCard

    Raises:
        ValueError: If neither video_id nor video_url is provided

    Examples:
        >>> # YouTube video with ID
        >>> card = generate_video_card(
        ...     title="Introduction to AI",
        ...     description="Learn the basics of artificial intelligence",
        ...     video_id="dQw4w9WgXcQ",
        ...     duration="10:30"
        ... )

        >>> # YouTube video with URL (auto-extracts ID)
        >>> card = generate_video_card(
        ...     title="Tutorial",
        ...     description="Step-by-step guide",
        ...     video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        ... )

        >>> # Generic video URL
        >>> card = generate_video_card(
        ...     title="Product Demo",
        ...     description="Our latest product in action",
        ...     video_url="https://example.com/video.mp4",
        ...     thumbnail_url="https://example.com/thumb.jpg"
        ... )
    """
    # Validate that we have either video_id or video_url
    if not video_id and not video_url:
        raise ValueError("VideoCard requires either video_id or video_url")

    props = {
        "title": title,
        "description": description,
    }

    # Handle YouTube URL extraction
    if video_url and not video_id:
        extracted_id = extract_youtube_id(video_url)
        if extracted_id:
            video_id = extracted_id
            props["videoId"] = video_id
            props["platform"] = "youtube"
        else:
            # Generic video URL
            props["videoUrl"] = video_url
    elif video_id:
        # Direct video ID provided (assume YouTube)
        props["videoId"] = video_id
        props["platform"] = "youtube"

    # Add optional fields
    if thumbnail_url:
        props["thumbnailUrl"] = thumbnail_url

    if duration:
        props["duration"] = duration

    return generate_component("a2ui.VideoCard", props)


def generate_image_card(
    title: str,
    image_url: str,
    alt_text: str | None = None,
    caption: str | None = None,
    credit: str | None = None
) -> A2UIComponent:
    """
    Generate an ImageCard A2UI component for image content.

    Creates an image card component with title, image URL, and optional metadata
    like alt text, caption, and credit attribution.

    Args:
        title: Image title/heading
        image_url: URL to the image file (must be valid URL format)
        alt_text: Alternative text for accessibility (recommended)
        caption: Image caption/description
        credit: Photo credit/attribution (e.g., "Photo by John Doe")

    Returns:
        A2UIComponent configured as ImageCard

    Raises:
        ValueError: If image_url is empty or invalid format

    Examples:
        >>> # Basic image card
        >>> card = generate_image_card(
        ...     title="Beautiful Sunset",
        ...     image_url="https://example.com/sunset.jpg"
        ... )

        >>> # Image card with all metadata
        >>> card = generate_image_card(
        ...     title="Mountain Landscape",
        ...     image_url="https://example.com/mountain.jpg",
        ...     alt_text="Snow-capped mountain peaks at sunrise",
        ...     caption="The view from base camp at 4,000m elevation",
        ...     credit="Photo by Jane Smith"
        ... )
    """
    # Validate image_url
    if not image_url or not image_url.strip():
        raise ValueError("ImageCard requires a valid image_url")

    # Basic URL validation (check for http/https)
    if not image_url.startswith(("http://", "https://")):
        raise ValueError(f"image_url must be a valid URL starting with http:// or https://, got: {image_url}")

    props = {
        "title": title,
        "imageUrl": image_url,
    }

    # Add optional fields
    if alt_text:
        props["altText"] = alt_text

    if caption:
        props["caption"] = caption

    if credit:
        props["credit"] = credit

    return generate_component("a2ui.ImageCard", props)


def generate_playlist_card(
    title: str,
    description: str,
    items: list[dict[str, str]],
    platform: str = "youtube"
) -> A2UIComponent:
    """
    Generate a PlaylistCard A2UI component for playlists.

    Creates a playlist card component with a list of media items. Supports
    YouTube, Spotify, and custom playlists.

    Args:
        title: Playlist title
        description: Playlist description/summary
        items: List of playlist items, each with:
               - "title": Item title (required)
               - "url" or "videoId": Item link/ID (required)
               - "duration": Optional duration
        platform: Platform type - "youtube", "spotify", or "custom" (default: "youtube")

    Returns:
        A2UIComponent configured as PlaylistCard with children structure

    Raises:
        ValueError: If items list is empty or exceeds 20 items
        ValueError: If items don't have required keys
        ValueError: If platform is not valid

    Examples:
        >>> # YouTube playlist
        >>> card = generate_playlist_card(
        ...     title="AI Tutorial Series",
        ...     description="Complete guide to machine learning",
        ...     items=[
        ...         {"title": "Introduction", "videoId": "abc123", "duration": "10:30"},
        ...         {"title": "Deep Learning", "videoId": "def456", "duration": "15:45"}
        ...     ],
        ...     platform="youtube"
        ... )

        >>> # Spotify playlist
        >>> card = generate_playlist_card(
        ...     title="Focus Music",
        ...     description="Music for deep work",
        ...     items=[
        ...         {"title": "Track 1", "url": "https://spotify.com/track/1"},
        ...         {"title": "Track 2", "url": "https://spotify.com/track/2"}
        ...     ],
        ...     platform="spotify"
        ... )
    """
    # Validate platform
    valid_platforms = {"youtube", "spotify", "custom"}
    if platform not in valid_platforms:
        raise ValueError(
            f"Invalid platform: {platform}. "
            f"Must be one of: {', '.join(valid_platforms)}"
        )

    # Validate items list
    if not items:
        raise ValueError("PlaylistCard requires at least one item")

    if len(items) > 20:
        raise ValueError(
            f"PlaylistCard supports up to 20 items, got {len(items)}. "
            "Consider splitting into multiple playlists."
        )

    # Validate that all items have required keys (title + url or videoId)
    for i, item in enumerate(items):
        if "title" not in item:
            raise ValueError(f"Item {i} missing required key: 'title'")

        if "url" not in item and "videoId" not in item:
            raise ValueError(
                f"Item {i} missing required key: must have either 'url' or 'videoId'"
            )

    props = {
        "title": title,
        "description": description,
        "platform": platform,
        "items": items,
    }

    return generate_component("a2ui.PlaylistCard", props)


def generate_podcast_card(
    title: str,
    description: str,
    episode_title: str,
    audio_url: str,
    duration: int,
    episode_number: int | None = None,
    platform: str | None = None
) -> A2UIComponent:
    """
    Generate a PodcastCard A2UI component for podcast episodes.

    Creates a podcast card component with episode information and audio playback.
    Supports various podcast platforms and direct audio URLs.

    Args:
        title: Podcast show title
        description: Podcast/episode description
        episode_title: Episode title/name
        audio_url: URL to audio file (MP3, etc.)
        duration: Episode duration in minutes
        episode_number: Optional episode number
        platform: Optional platform - "spotify", "apple", "rss", or "custom"

    Returns:
        A2UIComponent configured as PodcastCard

    Raises:
        ValueError: If audio_url is invalid
        ValueError: If duration is not positive
        ValueError: If platform is not valid

    Examples:
        >>> # Basic podcast card
        >>> card = generate_podcast_card(
        ...     title="Tech Talk",
        ...     description="Weekly tech discussions",
        ...     episode_title="AI Revolution",
        ...     audio_url="https://example.com/episode-5.mp3",
        ...     duration=45
        ... )

        >>> # Podcast with all metadata
        >>> card = generate_podcast_card(
        ...     title="The AI Podcast",
        ...     description="Exploring artificial intelligence",
        ...     episode_title="Deep Learning Fundamentals",
        ...     audio_url="https://example.com/episode.mp3",
        ...     duration=60,
        ...     episode_number=10,
        ...     platform="spotify"
        ... )
    """
    # Validate audio_url
    if not audio_url or not audio_url.strip():
        raise ValueError("PodcastCard requires a valid audio_url")

    # Validate duration
    if duration <= 0:
        raise ValueError(f"Duration must be positive, got: {duration}")

    # Validate platform if provided
    if platform:
        valid_platforms = {"spotify", "apple", "rss", "custom"}
        if platform not in valid_platforms:
            raise ValueError(
                f"Invalid platform: {platform}. "
                f"Must be one of: {', '.join(valid_platforms)}"
            )

    props = {
        "title": title,
        "description": description,
        "episodeTitle": episode_title,
        "audioUrl": audio_url,
        "duration": duration,
    }

    # Add optional fields
    if episode_number is not None:
        props["episodeNumber"] = episode_number

    if platform:
        props["platform"] = platform

    return generate_component("a2ui.PodcastCard", props)


# Data Component Generators

def generate_stat_card(
    title: str,
    value: str,
    unit: str | None = None,
    change: float | None = None,
    change_type: str = "neutral",
    highlight: bool = False
) -> A2UIComponent:
    """
    Generate a StatCard A2UI component for displaying statistics.

    Creates a stat card component showing a key metric with optional unit,
    change indicator, and highlighting. Useful for dashboards and KPIs.

    Args:
        title: Statistic label/title (e.g., "Total Users", "Revenue")
        value: Statistic value (can be string or number, e.g., "1,234", "$5.2M")
        unit: Optional unit suffix (e.g., "%", "$", "points", "users")
        change: Optional change value (percentage or absolute)
        change_type: Change indicator - "positive", "negative", or "neutral" (default)
        highlight: Whether to highlight this stat as important (default: False)

    Returns:
        A2UIComponent configured as StatCard

    Raises:
        ValueError: If change_type is not valid

    Examples:
        >>> # Basic stat card
        >>> card = generate_stat_card(
        ...     title="Total Users",
        ...     value="1,234"
        ... )

        >>> # Stat card with all features
        >>> card = generate_stat_card(
        ...     title="Revenue",
        ...     value="$5.2M",
        ...     unit="USD",
        ...     change=12.5,
        ...     change_type="positive",
        ...     highlight=True
        ... )

        >>> # Percentage stat with negative change
        >>> card = generate_stat_card(
        ...     title="Error Rate",
        ...     value="2.3",
        ...     unit="%",
        ...     change=-0.5,
        ...     change_type="positive"  # Lower error rate is positive
        ... )
    """
    # Validate change_type
    valid_change_types = {"positive", "negative", "neutral"}
    if change_type not in valid_change_types:
        raise ValueError(
            f"Invalid change_type: {change_type}. "
            f"Must be one of: {', '.join(valid_change_types)}"
        )

    props = {
        "title": title,
        "value": value,
        "changeType": change_type,
        "highlight": highlight,
    }

    # Add optional fields
    if unit:
        props["unit"] = unit

    if change is not None:
        props["change"] = change

    return generate_component("a2ui.StatCard", props)


def generate_metric_row(
    label: str,
    value: str,
    unit: str | None = None,
    status: str | None = None
) -> A2UIComponent:
    """
    Generate a MetricRow A2UI component for displaying key metrics.

    Creates a compact row-based metric display with optional status indicator.
    Useful for lists of related metrics or KPI dashboards.

    Args:
        label: Metric label/name (e.g., "CPU Usage", "Response Time")
        value: Metric value (string or number)
        unit: Optional unit (e.g., "%", "ms", "MB")
        status: Optional status - "good", "warning", "critical", or "neutral"

    Returns:
        A2UIComponent configured as MetricRow

    Raises:
        ValueError: If status is not valid

    Examples:
        >>> # Basic metric row
        >>> row = generate_metric_row(
        ...     label="CPU Usage",
        ...     value="45"
        ... )

        >>> # Metric with unit and status
        >>> row = generate_metric_row(
        ...     label="Response Time",
        ...     value="125",
        ...     unit="ms",
        ...     status="good"
        ... )

        >>> # Warning status metric
        >>> row = generate_metric_row(
        ...     label="Memory Usage",
        ...     value="85",
        ...     unit="%",
        ...     status="warning"
        ... )
    """
    # Validate status if provided
    if status:
        valid_statuses = {"good", "warning", "critical", "neutral"}
        if status not in valid_statuses:
            raise ValueError(
                f"Invalid status: {status}. "
                f"Must be one of: {', '.join(valid_statuses)}"
            )

    props = {
        "label": label,
        "value": value,
    }

    # Add optional fields
    if unit:
        props["unit"] = unit

    if status:
        props["status"] = status

    return generate_component("a2ui.MetricRow", props)


def generate_progress_ring(
    label: str,
    current: float,
    maximum: float = 100,
    unit: str | None = None,
    color: str = "blue"
) -> A2UIComponent:
    """
    Generate a ProgressRing A2UI component (circular progress indicator).

    Creates a circular progress ring showing current value out of maximum.
    Automatically calculates percentage. Useful for goals, completion, etc.

    Args:
        label: Progress label (e.g., "Course Progress", "Storage Used")
        current: Current value (e.g., 75)
        maximum: Maximum value (default: 100)
        unit: Optional unit (e.g., "%", "GB", "tasks")
        color: Ring color - "blue", "green", "red", "yellow", "purple", "gray" (default: "blue")

    Returns:
        A2UIComponent configured as ProgressRing

    Raises:
        ValueError: If current or maximum is negative
        ValueError: If color is not valid

    Examples:
        >>> # Basic progress ring (75%)
        >>> ring = generate_progress_ring(
        ...     label="Course Progress",
        ...     current=75
        ... )

        >>> # Storage usage with custom max and unit
        >>> ring = generate_progress_ring(
        ...     label="Storage Used",
        ...     current=45.2,
        ...     maximum=100,
        ...     unit="GB",
        ...     color="green"
        ... )

        >>> # Task completion
        >>> ring = generate_progress_ring(
        ...     label="Tasks Complete",
        ...     current=8,
        ...     maximum=10,
        ...     unit="tasks",
        ...     color="purple"
        ... )
    """
    # Validate current and maximum
    if current < 0:
        raise ValueError(f"Current value cannot be negative, got: {current}")

    if maximum <= 0:
        raise ValueError(f"Maximum value must be positive, got: {maximum}")

    # Validate color
    valid_colors = {"blue", "green", "red", "yellow", "purple", "gray"}
    if color not in valid_colors:
        raise ValueError(
            f"Invalid color: {color}. "
            f"Must be one of: {', '.join(valid_colors)}"
        )

    props = {
        "label": label,
        "current": current,
        "maximum": maximum,
        "color": color,
    }

    # Add optional fields
    if unit:
        props["unit"] = unit

    return generate_component("a2ui.ProgressRing", props)


def generate_comparison_bar(
    label: str,
    items: list[dict[str, any]],
    max_value: float | None = None
) -> A2UIComponent:
    """
    Generate a ComparisonBar A2UI component for comparing multiple values.

    Creates a comparison bar chart for visualizing relative values.
    Supports up to 10 items with automatic or manual max value.

    Args:
        label: Comparison label/title (e.g., "Browser Market Share", "Team Performance")
        items: List of items to compare, each with:
                - "label": Item label (required)
                - "value": Item value (required, number)
                - "color": Optional color (hex or name)
        max_value: Optional maximum value for scale (auto-calculated if not provided)

    Returns:
        A2UIComponent configured as ComparisonBar

    Raises:
        ValueError: If items list is empty or exceeds 10 items
        ValueError: If items don't have required keys
        ValueError: If max_value is negative

    Examples:
        >>> # Browser market share comparison
        >>> bar = generate_comparison_bar(
        ...     label="Browser Market Share",
        ...     items=[
        ...         {"label": "Chrome", "value": 65.5, "color": "green"},
        ...         {"label": "Safari", "value": 18.2, "color": "blue"},
        ...         {"label": "Firefox", "value": 8.1, "color": "orange"},
        ...         {"label": "Edge", "value": 5.8, "color": "teal"}
        ...     ]
        ... )

        >>> # Team performance with auto max
        >>> bar = generate_comparison_bar(
        ...     label="Team Performance",
        ...     items=[
        ...         {"label": "Team A", "value": 92},
        ...         {"label": "Team B", "value": 88},
        ...         {"label": "Team C", "value": 95}
        ...     ]
        ... )
    """
    # Validate items list
    if not items:
        raise ValueError("ComparisonBar requires at least one item")

    if len(items) > 10:
        raise ValueError(
            f"ComparisonBar supports up to 10 items, got {len(items)}. "
            "Consider using a different visualization for more items."
        )

    # Validate that all items have required keys
    for i, item in enumerate(items):
        if "label" not in item:
            raise ValueError(f"Item {i} missing required key: 'label'")

        if "value" not in item:
            raise ValueError(f"Item {i} missing required key: 'value'")

        # Validate value is a number
        if not isinstance(item["value"], (int, float)):
            raise ValueError(
                f"Item {i} value must be a number, got: {type(item['value']).__name__}"
            )

    # Auto-calculate max_value if not provided
    if max_value is None:
        max_value = max(item["value"] for item in items)

    # Validate max_value
    if max_value < 0:
        raise ValueError(f"max_value cannot be negative, got: {max_value}")

    props = {
        "label": label,
        "items": items,
        "maxValue": max_value,
    }

    return generate_component("a2ui.ComparisonBar", props)


def generate_data_table(
    headers: list[str],
    rows: list[list[any]],
    sortable: bool = False,
    filterable: bool = False,
    striped: bool = True
) -> A2UIComponent:
    """
    Generate a DataTable A2UI component for tabular data.

    Creates a data table with headers and rows. Supports sorting, filtering,
    and striped styling. Maximum 50 rows for performance.

    Args:
        headers: List of column header names
        rows: List of data rows (each row is a list of cell values)
        sortable: Enable column sorting (default: False)
        filterable: Enable table filtering (default: False)
        striped: Use alternating row colors (default: True)

    Returns:
        A2UIComponent configured as DataTable

    Raises:
        ValueError: If headers is empty
        ValueError: If rows is empty or exceeds 50 rows
        ValueError: If row lengths don't match header length

    Examples:
        >>> # Basic data table
        >>> table = generate_data_table(
        ...     headers=["Name", "Age", "City"],
        ...     rows=[
        ...         ["Alice", 28, "New York"],
        ...         ["Bob", 34, "San Francisco"],
        ...         ["Charlie", 23, "Boston"]
        ...     ]
        ... )

        >>> # Sortable and filterable table
        >>> table = generate_data_table(
        ...     headers=["Product", "Price", "Stock", "Status"],
        ...     rows=[
        ...         ["Widget A", "$29.99", 150, "In Stock"],
        ...         ["Widget B", "$39.99", 0, "Out of Stock"],
        ...         ["Widget C", "$19.99", 45, "Low Stock"]
        ...     ],
        ...     sortable=True,
        ...     filterable=True,
        ...     striped=True
        ... )
    """
    # Validate headers
    if not headers:
        raise ValueError("DataTable requires at least one header")

    # Validate rows
    if not rows:
        raise ValueError("DataTable requires at least one row")

    if len(rows) > 50:
        raise ValueError(
            f"DataTable supports up to 50 rows for performance, got {len(rows)}. "
            "Consider pagination or filtering for larger datasets."
        )

    # Validate that all rows have the same length as headers
    header_count = len(headers)
    for i, row in enumerate(rows):
        if len(row) != header_count:
            raise ValueError(
                f"Row {i} has {len(row)} cells, but expected {header_count} "
                f"to match headers: {headers}"
            )

    props = {
        "headers": headers,
        "rows": rows,
        "sortable": sortable,
        "filterable": filterable,
        "striped": striped,
    }

    return generate_component("a2ui.DataTable", props)


def generate_mini_chart(
    chart_type: str,
    data_points: list[float],
    labels: list[str] | None = None,
    title: str | None = None
) -> A2UIComponent:
    """
    Generate a MiniChart A2UI component for small data visualizations.

    Creates a compact chart for visualizing trends and patterns.
    Supports multiple chart types with 5-100 data points.

    Args:
        chart_type: Chart type - "line", "bar", "area", "pie", or "donut"
        data_points: List of numeric data points (5-100 points)
        labels: Optional list of labels (one per data point)
        title: Optional chart title

    Returns:
        A2UIComponent configured as MiniChart

    Raises:
        ValueError: If chart_type is not valid
        ValueError: If data_points has fewer than 5 or more than 100 points
        ValueError: If labels provided but length doesn't match data_points

    Examples:
        >>> # Line chart for trend
        >>> chart = generate_mini_chart(
        ...     chart_type="line",
        ...     data_points=[10, 12, 15, 14, 18, 22, 25],
        ...     title="Weekly Sales"
        ... )

        >>> # Bar chart with labels
        >>> chart = generate_mini_chart(
        ...     chart_type="bar",
        ...     data_points=[45, 62, 38, 55, 70],
        ...     labels=["Q1", "Q2", "Q3", "Q4", "Q5"],
        ...     title="Quarterly Revenue"
        ... )

        >>> # Pie chart for distribution
        >>> chart = generate_mini_chart(
        ...     chart_type="pie",
        ...     data_points=[35, 25, 20, 15, 5],
        ...     labels=["Chrome", "Safari", "Firefox", "Edge", "Other"],
        ...     title="Browser Share"
        ... )
    """
    # Validate chart_type
    valid_chart_types = {"line", "bar", "area", "pie", "donut"}
    if chart_type not in valid_chart_types:
        raise ValueError(
            f"Invalid chart_type: {chart_type}. "
            f"Must be one of: {', '.join(valid_chart_types)}"
        )

    # Validate data_points
    if len(data_points) < 5:
        raise ValueError(
            f"MiniChart requires at least 5 data points, got {len(data_points)}"
        )

    if len(data_points) > 100:
        raise ValueError(
            f"MiniChart supports up to 100 data points, got {len(data_points)}. "
            "Consider data aggregation or a different visualization."
        )

    # Validate all data points are numbers
    for i, point in enumerate(data_points):
        if not isinstance(point, (int, float)):
            raise ValueError(
                f"Data point {i} must be a number, got: {type(point).__name__}"
            )

    # Validate labels if provided
    if labels is not None:
        if len(labels) != len(data_points):
            raise ValueError(
                f"Labels length ({len(labels)}) must match data_points length ({len(data_points)})"
            )

    props = {
        "chartType": chart_type,
        "dataPoints": data_points,
    }

    # Add optional fields
    if labels:
        props["labels"] = labels

    if title:
        props["title"] = title

    return generate_component("a2ui.MiniChart", props)


# List Component Generators

def generate_ranked_item(
    rank: int,
    title: str,
    description: str | None = None,
    score: float | None = None,
    score_max: float = 10,
    icon: str | None = None
) -> A2UIComponent:
    """
    Generate a RankedItem A2UI component for ranked list items.

    Creates a ranked item component for displaying items in a ranked list,
    leaderboard, or top-N list. Supports highlighting for top items (rank 1-3).

    Args:
        rank: Item rank (integer >= 1, e.g., 1 for #1, 2 for #2)
        title: Item title/name (e.g., "GPT-4", "Tesla Model 3")
        description: Optional item description or details
        score: Optional numeric score (0 to score_max)
        score_max: Maximum score value (default: 10)
        icon: Optional icon identifier (e.g., "trophy", "star")

    Returns:
        A2UIComponent configured as RankedItem

    Raises:
        ValueError: If rank is less than 1
        ValueError: If score is negative or exceeds score_max
        ValueError: If score_max is not positive

    Examples:
        >>> # Basic ranked item
        >>> item = generate_ranked_item(
        ...     rank=1,
        ...     title="GPT-4"
        ... )

        >>> # Ranked item with all features (top item with trophy)
        >>> item = generate_ranked_item(
        ...     rank=1,
        ...     title="Tesla Model 3",
        ...     description="Best-selling electric vehicle worldwide",
        ...     score=9.5,
        ...     score_max=10,
        ...     icon="trophy"
        ... )

        >>> # Mid-ranked item with score
        >>> item = generate_ranked_item(
        ...     rank=5,
        ...     title="Product X",
        ...     description="Solid performer in category",
        ...     score=7.8,
        ...     score_max=10
        ... )
    """
    # Validate rank
    if rank < 1:
        raise ValueError(f"Rank must be >= 1, got: {rank}")

    # Validate score_max
    if score_max <= 0:
        raise ValueError(f"score_max must be positive, got: {score_max}")

    # Validate score if provided
    if score is not None:
        if score < 0:
            raise ValueError(f"Score cannot be negative, got: {score}")
        if score > score_max:
            raise ValueError(
                f"Score ({score}) cannot exceed score_max ({score_max})"
            )

    props = {
        "rank": rank,
        "title": title,
        "scoreMax": score_max,
    }

    # Add optional fields
    if description:
        props["description"] = description

    if score is not None:
        props["score"] = score

    if icon:
        props["icon"] = icon

    return generate_component("a2ui.RankedItem", props)


def generate_checklist_item(
    text: str,
    checked: bool = False,
    priority: str | None = None,
    due_date: str | None = None
) -> A2UIComponent:
    """
    Generate a ChecklistItem A2UI component for to-do lists and checklists.

    Creates a checklist item with checkbox state, optional priority,
    and due date. Useful for task lists, to-do lists, and checklists.

    Args:
        text: Checklist item text/description
        checked: Whether the item is checked/complete (default: False)
        priority: Optional priority level - "high", "medium", or "low"
        due_date: Optional due date (YYYY-MM-DD format recommended)

    Returns:
        A2UIComponent configured as ChecklistItem

    Raises:
        ValueError: If text is empty
        ValueError: If priority is not "high", "medium", or "low"

    Examples:
        >>> # Basic unchecked item
        >>> item = generate_checklist_item(
        ...     text="Complete project proposal"
        ... )

        >>> # Checked item with priority
        >>> item = generate_checklist_item(
        ...     text="Review PR #123",
        ...     checked=True,
        ...     priority="high"
        ... )

        >>> # High priority item with due date
        >>> item = generate_checklist_item(
        ...     text="Submit quarterly report",
        ...     checked=False,
        ...     priority="high",
        ...     due_date="2026-02-15"
        ... )

        >>> # Low priority completed item
        >>> item = generate_checklist_item(
        ...     text="Update documentation",
        ...     checked=True,
        ...     priority="low",
        ...     due_date="2026-01-30"
        ... )
    """
    # Validate text
    if not text or not text.strip():
        raise ValueError("ChecklistItem text cannot be empty")

    # Validate priority if provided
    if priority:
        valid_priorities = {"high", "medium", "low"}
        if priority not in valid_priorities:
            raise ValueError(
                f"Invalid priority: {priority}. "
                f"Must be one of: {', '.join(valid_priorities)}"
            )

    props = {
        "text": text.strip(),
        "checked": checked,
    }

    # Add optional fields
    if priority:
        props["priority"] = priority

    if due_date:
        props["dueDate"] = due_date

    return generate_component("a2ui.ChecklistItem", props)


def generate_pro_con_item(
    title: str,
    pros: list[str],
    cons: list[str],
    verdict: str | None = None
) -> A2UIComponent:
    """
    Generate a ProConItem A2UI component for pros/cons analysis.

    Creates a pros and cons comparison component for decision analysis,
    product evaluations, or comparative assessments. Supports visual
    separation of pros and cons with optional verdict/recommendation.

    Args:
        title: Item/topic title (e.g., "Remote Work", "Product X")
        pros: List of pros/advantages (1-10 items)
        cons: List of cons/disadvantages (1-10 items)
        verdict: Optional verdict/recommendation text

    Returns:
        A2UIComponent configured as ProConItem

    Raises:
        ValueError: If title is empty
        ValueError: If pros or cons list is empty
        ValueError: If pros or cons list exceeds 10 items

    Examples:
        >>> # Basic pros/cons analysis
        >>> item = generate_pro_con_item(
        ...     title="Remote Work",
        ...     pros=[
        ...         "Flexible schedule",
        ...         "No commute time",
        ...         "Better work-life balance"
        ...     ],
        ...     cons=[
        ...         "Less face-to-face interaction",
        ...         "Potential isolation",
        ...         "Harder to separate work/home"
        ...     ]
        ... )

        >>> # Product comparison with verdict
        >>> item = generate_pro_con_item(
        ...     title="Electric Vehicle vs Gas Car",
        ...     pros=[
        ...         "Lower running costs",
        ...         "Environmentally friendly",
        ...         "Quiet operation",
        ...         "Lower maintenance"
        ...     ],
        ...     cons=[
        ...         "Higher upfront cost",
        ...         "Limited charging infrastructure",
        ...         "Range anxiety"
        ...     ],
        ...     verdict="Best for urban commuters with home charging"
        ... )

        >>> # Technology evaluation
        >>> item = generate_pro_con_item(
        ...     title="GraphQL vs REST",
        ...     pros=[
        ...         "Flexible queries",
        ...         "Single endpoint",
        ...         "Strong typing"
        ...     ],
        ...     cons=[
        ...         "Steeper learning curve",
        ...         "Query complexity",
        ...         "Caching challenges"
        ...     ],
        ...     verdict="Choose GraphQL for complex data requirements"
        ... )
    """
    # Validate title
    if not title or not title.strip():
        raise ValueError("ProConItem title cannot be empty")

    # Validate pros list
    if not pros:
        raise ValueError("ProConItem requires at least one pro")

    if len(pros) > 10:
        raise ValueError(
            f"ProConItem supports up to 10 pros, got {len(pros)}. "
            "Consider summarizing or grouping similar points."
        )

    # Validate cons list
    if not cons:
        raise ValueError("ProConItem requires at least one con")

    if len(cons) > 10:
        raise ValueError(
            f"ProConItem supports up to 10 cons, got {len(cons)}. "
            "Consider summarizing or grouping similar points."
        )

    props = {
        "title": title.strip(),
        "pros": pros,
        "cons": cons,
    }

    # Add optional verdict
    if verdict:
        props["verdict"] = verdict

    return generate_component("a2ui.ProConItem", props)


def generate_bullet_point(
    text: str,
    level: int = 0,
    icon: str | None = None,
    highlight: bool = False
) -> A2UIComponent:
    """
    Generate a BulletPoint A2UI component for bulleted lists.

    Creates a bullet point component supporting hierarchical nested lists
    with customizable icons and highlighting. Useful for structured content,
    outlines, and nested information.

    Args:
        text: Bullet point text content
        level: Nesting level (0-3, where 0 is root, 1-3 are nested)
        icon: Optional icon identifier (e.g., "circle", "square", "arrow")
        highlight: Whether to highlight this bullet point (default: False)

    Returns:
        A2UIComponent configured as BulletPoint

    Raises:
        ValueError: If text is empty
        ValueError: If level is not between 0 and 3

    Examples:
        >>> # Basic root bullet point
        >>> bullet = generate_bullet_point(
        ...     text="Main point"
        ... )

        >>> # Level 1 nested bullet
        >>> bullet = generate_bullet_point(
        ...     text="Sub-point under main item",
        ...     level=1
        ... )

        >>> # Highlighted bullet with custom icon
        >>> bullet = generate_bullet_point(
        ...     text="Important takeaway",
        ...     level=0,
        ...     icon="star",
        ...     highlight=True
        ... )

        >>> # Deep nested bullet (level 3)
        >>> bullet = generate_bullet_point(
        ...     text="Detailed sub-sub-sub point",
        ...     level=3,
        ...     icon="circle"
        ... )

        >>> # Level 2 bullet with arrow icon
        >>> bullet = generate_bullet_point(
        ...     text="Action item",
        ...     level=2,
        ...     icon="arrow"
        ... )
    """
    # Validate text
    if not text or not text.strip():
        raise ValueError("BulletPoint text cannot be empty")

    # Validate level
    if level < 0 or level > 3:
        raise ValueError(
            f"Level must be between 0 and 3 (inclusive), got: {level}"
        )

    props = {
        "text": text.strip(),
        "level": level,
        "highlight": highlight,
    }

    # Add optional icon
    if icon:
        props["icon"] = icon

    return generate_component("a2ui.BulletPoint", props)


# Resource Component Generators

def extract_domain(url: str) -> str:
    """
    Extract domain from any URL.

    Extracts the domain name from a URL by parsing the netloc component.
    Handles various URL formats and removes www. prefix if present.

    Args:
        url: URL string to extract domain from

    Returns:
        Domain name (e.g., "example.com")

    Raises:
        ValueError: If URL is invalid or empty

    Examples:
        >>> extract_domain("https://example.com/path")
        "example.com"
        >>> extract_domain("https://www.github.com/user/repo")
        "github.com"
        >>> extract_domain("http://subdomain.example.com:8080/page")
        "subdomain.example.com"
    """
    if not url or not url.strip():
        raise ValueError("URL cannot be empty")

    # Ensure URL has scheme for parsing
    if not url.startswith(("http://", "https://")):
        raise ValueError(f"URL must start with http:// or https://, got: {url}")

    # Parse URL
    from urllib.parse import urlparse
    parsed = urlparse(url)
    domain = parsed.netloc

    if not domain:
        raise ValueError(f"Could not extract domain from URL: {url}")

    # Remove port if present
    if ':' in domain:
        domain = domain.split(':')[0]

    # Remove www. prefix if present
    if domain.startswith('www.'):
        domain = domain[4:]

    return domain


def extract_github_repo_info(url_or_owner_repo: str) -> dict[str, str]:
    """
    Extract GitHub repository information from URL or owner/repo string.

    Parses various GitHub URL formats or "owner/repo" string format
    to extract owner and repository name.

    Supported formats:
    - https://github.com/owner/repo
    - http://github.com/owner/repo
    - github.com/owner/repo
    - owner/repo

    Args:
        url_or_owner_repo: GitHub URL or "owner/repo" string

    Returns:
        Dictionary with keys: "owner", "repo", "url"

    Raises:
        ValueError: If format is invalid or cannot be parsed

    Examples:
        >>> extract_github_repo_info("https://github.com/facebook/react")
        {"owner": "facebook", "repo": "react", "url": "https://github.com/facebook/react"}
        >>> extract_github_repo_info("facebook/react")
        {"owner": "facebook", "repo": "react", "url": "https://github.com/facebook/react"}
        >>> extract_github_repo_info("github.com/torvalds/linux")
        {"owner": "torvalds", "repo": "linux", "url": "https://github.com/torvalds/linux"}
    """
    if not url_or_owner_repo or not url_or_owner_repo.strip():
        raise ValueError("GitHub URL or owner/repo cannot be empty")

    input_str = url_or_owner_repo.strip()

    # Pattern 1: Full GitHub URL
    github_url_pattern = r'(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/\s]+)'
    match = re.match(github_url_pattern, input_str)

    if match:
        owner = match.group(1)
        repo = match.group(2).rstrip('/')
        # Remove .git suffix if present
        if repo.endswith('.git'):
            repo = repo[:-4]
        return {
            "owner": owner,
            "repo": repo,
            "url": f"https://github.com/{owner}/{repo}"
        }

    # Pattern 2: owner/repo format
    owner_repo_pattern = r'^([^/\s]+)/([^/\s]+)$'
    match = re.match(owner_repo_pattern, input_str)

    if match:
        owner = match.group(1)
        repo = match.group(2)
        return {
            "owner": owner,
            "repo": repo,
            "url": f"https://github.com/{owner}/{repo}"
        }

    raise ValueError(
        f"Invalid GitHub URL or owner/repo format: {input_str}. "
        "Expected formats: 'https://github.com/owner/repo', 'github.com/owner/repo', or 'owner/repo'"
    )


def generate_link_card(
    title: str,
    url: str,
    description: str | None = None,
    domain: str | None = None,
    image_url: str | None = None,
    tags: list[str] | None = None
) -> A2UIComponent:
    """
    Generate a LinkCard A2UI component for external resource links.

    Creates a link card component for bookmarks, curated links, and resource
    collections. Automatically extracts domain from URL if not provided.

    Args:
        title: Link title/heading
        url: Link URL (must be valid HTTP/HTTPS URL)
        description: Optional link description or summary
        domain: Optional domain name (auto-extracted from URL if not provided)
        image_url: Optional preview/thumbnail image URL
        tags: Optional list of tags (max 5)

    Returns:
        A2UIComponent configured as LinkCard

    Raises:
        ValueError: If URL is invalid format
        ValueError: If tags list exceeds 5 items

    Examples:
        >>> # Basic link card
        >>> card = generate_link_card(
        ...     title="React Documentation",
        ...     url="https://react.dev/learn"
        ... )

        >>> # Link card with all metadata
        >>> card = generate_link_card(
        ...     title="Introduction to Machine Learning",
        ...     url="https://example.com/ml-intro",
        ...     description="Comprehensive guide to ML fundamentals",
        ...     domain="example.com",
        ...     image_url="https://example.com/ml-preview.jpg",
        ...     tags=["machine-learning", "tutorial", "beginner"]
        ... )
    """
    # Validate URL format
    if not url or not url.strip():
        raise ValueError("LinkCard requires a valid URL")

    if not url.startswith(("http://", "https://")):
        raise ValueError(f"URL must start with http:// or https://, got: {url}")

    # Auto-extract domain if not provided
    if not domain:
        domain = extract_domain(url)

    # Validate tags
    if tags and len(tags) > 5:
        raise ValueError(
            f"LinkCard supports up to 5 tags, got {len(tags)}. "
            "Consider using only the most relevant tags."
        )

    props = {
        "title": title,
        "url": url,
        "domain": domain,
    }

    # Add optional fields
    if description:
        props["description"] = description

    if image_url:
        props["imageUrl"] = image_url

    if tags:
        props["tags"] = tags

    return generate_component("a2ui.LinkCard", props)


def generate_tool_card(
    name: str,
    description: str,
    url: str,
    category: str | None = None,
    pricing: str | None = None,
    icon_url: str | None = None,
    features: list[str] | None = None
) -> A2UIComponent:
    """
    Generate a ToolCard A2UI component for software tools/services.

    Creates a tool card component for tool recommendations, tech stacks,
    and resource catalogs. Supports categorization and feature highlights.

    Args:
        name: Tool name (e.g., "VS Code", "Figma", "GitHub")
        description: Tool description/summary
        url: Tool website URL (must be valid HTTP/HTTPS URL)
        category: Optional category - "ide", "analytics", "design", "productivity", etc.
        pricing: Optional pricing model - "free", "freemium", "paid"
        icon_url: Optional tool icon/logo URL
        features: Optional list of key features (max 5)

    Returns:
        A2UIComponent configured as ToolCard

    Raises:
        ValueError: If URL is invalid format
        ValueError: If pricing is not valid
        ValueError: If features list exceeds 5 items

    Examples:
        >>> # Basic tool card
        >>> card = generate_tool_card(
        ...     name="VS Code",
        ...     description="Free code editor from Microsoft",
        ...     url="https://code.visualstudio.com"
        ... )

        >>> # Tool card with all features
        >>> card = generate_tool_card(
        ...     name="Figma",
        ...     description="Collaborative interface design tool",
        ...     url="https://www.figma.com",
        ...     category="design",
        ...     pricing="freemium",
        ...     icon_url="https://www.figma.com/favicon.ico",
        ...     features=["Real-time collaboration", "Prototyping", "Design systems"]
        ... )
    """
    # Validate URL format
    if not url or not url.strip():
        raise ValueError("ToolCard requires a valid URL")

    if not url.startswith(("http://", "https://")):
        raise ValueError(f"URL must start with http:// or https://, got: {url}")

    # Validate pricing if provided
    if pricing:
        valid_pricing = {"free", "freemium", "paid"}
        if pricing not in valid_pricing:
            raise ValueError(
                f"Invalid pricing: {pricing}. "
                f"Must be one of: {', '.join(valid_pricing)}"
            )

    # Validate features
    if features and len(features) > 5:
        raise ValueError(
            f"ToolCard supports up to 5 features, got {len(features)}. "
            "Consider highlighting only the most important features."
        )

    props = {
        "name": name,
        "description": description,
        "url": url,
    }

    # Add optional fields
    if category:
        props["category"] = category

    if pricing:
        props["pricing"] = pricing

    if icon_url:
        props["iconUrl"] = icon_url

    if features:
        props["features"] = features

    return generate_component("a2ui.ToolCard", props)


def generate_book_card(
    title: str,
    author: str,
    year: int | None = None,
    isbn: str | None = None,
    url: str | None = None,
    cover_image_url: str | None = None,
    rating: float | None = None,
    description: str | None = None
) -> A2UIComponent:
    """
    Generate a BookCard A2UI component for books/publications.

    Creates a book card component for book recommendations and reading lists.
    Supports ISBN validation and rating display.

    Args:
        title: Book title
        author: Book author name(s)
        year: Optional publication year
        isbn: Optional ISBN (10 or 13 digits)
        url: Optional URL to purchase/view the book
        cover_image_url: Optional book cover image URL
        rating: Optional rating (0-5 scale)
        description: Optional book description/summary

    Returns:
        A2UIComponent configured as BookCard

    Raises:
        ValueError: If ISBN format is invalid (must be 10 or 13 digits)
        ValueError: If rating is not between 0 and 5
        ValueError: If URL is provided but invalid format

    Examples:
        >>> # Basic book card
        >>> card = generate_book_card(
        ...     title="Clean Code",
        ...     author="Robert C. Martin"
        ... )

        >>> # Book card with all metadata
        >>> card = generate_book_card(
        ...     title="The Pragmatic Programmer",
        ...     author="Andrew Hunt, David Thomas",
        ...     year=2019,
        ...     isbn="9780135957059",
        ...     url="https://pragprog.com/titles/tpp20/",
        ...     cover_image_url="https://pragprog.com/titles/tpp20/tpp20.jpg",
        ...     rating=4.5,
        ...     description="Your journey to mastery"
        ... )
    """
    # Validate ISBN if provided
    if isbn:
        # Remove hyphens and spaces
        isbn_clean = isbn.replace('-', '').replace(' ', '')
        if not (len(isbn_clean) == 10 or len(isbn_clean) == 13):
            raise ValueError(
                f"Invalid ISBN format: {isbn}. "
                "ISBN must be 10 or 13 digits (hyphens/spaces allowed)"
            )
        if not isbn_clean.isdigit():
            raise ValueError(
                f"Invalid ISBN format: {isbn}. "
                "ISBN must contain only digits (and optional hyphens/spaces)"
            )

    # Validate rating if provided
    if rating is not None:
        if rating < 0 or rating > 5:
            raise ValueError(
                f"Rating must be between 0 and 5, got: {rating}"
            )

    # Validate URL if provided
    if url and not url.startswith(("http://", "https://")):
        raise ValueError(f"URL must start with http:// or https://, got: {url}")

    props = {
        "title": title,
        "author": author,
    }

    # Add optional fields
    if year is not None:
        props["year"] = year

    if isbn:
        props["isbn"] = isbn

    if url:
        props["url"] = url

    if cover_image_url:
        props["coverImageUrl"] = cover_image_url

    if rating is not None:
        props["rating"] = rating

    if description:
        props["description"] = description

    return generate_component("a2ui.BookCard", props)


def generate_repo_card(
    name: str,
    owner: str | None = None,
    repo_url: str | None = None,
    description: str | None = None,
    language: str | None = None,
    stars: int | None = None,
    fork_count: int | None = None,
    topics: list[str] | None = None
) -> A2UIComponent:
    """
    Generate a RepoCard A2UI component for GitHub repositories.

    Creates a repository card component for code repositories and open-source
    projects. Automatically constructs GitHub URL from owner + name if needed.
    Supports GitHub metadata like stars, forks, and topics.

    Args:
        name: Repository name (e.g., "react", "tensorflow")
        owner: Optional GitHub username/org (e.g., "facebook", "tensorflow")
        repo_url: Optional repository URL (can auto-construct from owner + name)
        description: Optional repository description
        language: Optional primary programming language
        stars: Optional star count
        fork_count: Optional fork count
        topics: Optional list of repository topics (max 5)

    Returns:
        A2UIComponent configured as RepoCard

    Raises:
        ValueError: If neither repo_url nor (owner + name) is provided
        ValueError: If repo_url is provided but invalid GitHub URL
        ValueError: If topics list exceeds 5 items
        ValueError: If stars or fork_count is negative

    Examples:
        >>> # Repository from URL
        >>> card = generate_repo_card(
        ...     name="react",
        ...     repo_url="https://github.com/facebook/react"
        ... )

        >>> # Repository from owner + name
        >>> card = generate_repo_card(
        ...     name="tensorflow",
        ...     owner="tensorflow",
        ...     description="Open source machine learning framework",
        ...     language="Python",
        ...     stars=185000,
        ...     fork_count=74000,
        ...     topics=["machine-learning", "deep-learning", "python"]
        ... )

        >>> # Repository with all metadata
        >>> card = generate_repo_card(
        ...     name="vscode",
        ...     owner="microsoft",
        ...     description="Visual Studio Code",
        ...     language="TypeScript",
        ...     stars=150000,
        ...     fork_count=26000,
        ...     topics=["editor", "typescript", "electron"]
        ... )
    """
    # Extract repo info from URL if provided
    if repo_url:
        try:
            repo_info = extract_github_repo_info(repo_url)
            if not owner:
                owner = repo_info["owner"]
            # Use canonical URL
            repo_url = repo_info["url"]
        except ValueError:
            # Not a GitHub URL, use as-is
            if not repo_url.startswith(("http://", "https://")):
                raise ValueError(f"repo_url must start with http:// or https://, got: {repo_url}")

    # Construct GitHub URL from owner + name if not provided
    if not repo_url:
        if not owner:
            raise ValueError(
                "RepoCard requires either repo_url or both owner and name"
            )
        repo_url = f"https://github.com/{owner}/{name}"

    # Validate topics
    if topics and len(topics) > 5:
        raise ValueError(
            f"RepoCard supports up to 5 topics, got {len(topics)}. "
            "Consider using only the most relevant topics."
        )

    # Validate stars
    if stars is not None and stars < 0:
        raise ValueError(f"Star count cannot be negative, got: {stars}")

    # Validate fork_count
    if fork_count is not None and fork_count < 0:
        raise ValueError(f"Fork count cannot be negative, got: {fork_count}")

    props = {
        "name": name,
        "repoUrl": repo_url,
    }

    # Add optional fields
    if owner:
        props["owner"] = owner

    if description:
        props["description"] = description

    if language:
        props["language"] = language

    if stars is not None:
        props["stars"] = stars

    if fork_count is not None:
        props["forkCount"] = fork_count

    if topics:
        props["topics"] = topics

    return generate_component("a2ui.RepoCard", props)


# People Component Generators

def generate_profile_card(
    name: str,
    title: str,
    bio: str | None = None,
    avatar_url: str | None = None,
    contact: dict[str, str] | None = None,
    social_links: list[dict[str, str]] | None = None
) -> A2UIComponent:
    """
    Generate a ProfileCard A2UI component for person profiles.

    Creates a profile card component for team bios, expert profiles, and author cards.
    Supports contact information and social media links.

    Args:
        name: Person's full name (e.g., "Jane Smith", "Dr. John Doe")
        title: Person's title/role (e.g., "Senior Engineer", "CEO", "AI Researcher")
        bio: Optional short biography or description
        avatar_url: Optional URL to avatar/profile image
        contact: Optional contact information dict with keys:
                 - "email": Email address (validated)
                 - "phone": Phone number
                 - "location": Location/city
        social_links: Optional list of social media links (max 5), each with:
                     - "platform": Platform name (twitter, linkedin, github, website, etc.)
                     - "url": Profile URL

    Returns:
        A2UIComponent configured as ProfileCard

    Raises:
        ValueError: If name or title is empty
        ValueError: If email format is invalid
        ValueError: If social_links exceeds 5 items
        ValueError: If social_links items don't have required keys

    Examples:
        >>> # Basic profile card
        >>> card = generate_profile_card(
        ...     name="Jane Smith",
        ...     title="AI Researcher"
        ... )

        >>> # Profile card with all features
        >>> card = generate_profile_card(
        ...     name="Dr. John Doe",
        ...     title="Chief Technology Officer",
        ...     bio="20+ years building scalable systems",
        ...     avatar_url="https://example.com/avatar.jpg",
        ...     contact={
        ...         "email": "john@example.com",
        ...         "phone": "+1-555-0100",
        ...         "location": "San Francisco, CA"
        ...     },
        ...     social_links=[
        ...         {"platform": "twitter", "url": "https://twitter.com/johndoe"},
        ...         {"platform": "linkedin", "url": "https://linkedin.com/in/johndoe"},
        ...         {"platform": "github", "url": "https://github.com/johndoe"}
        ...     ]
        ... )
    """
    # Validate name
    if not name or not name.strip():
        raise ValueError("ProfileCard name cannot be empty")

    # Validate title
    if not title or not title.strip():
        raise ValueError("ProfileCard title cannot be empty")

    # Validate email format if provided in contact
    if contact and "email" in contact:
        email = contact["email"]
        # Basic email validation
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError(f"Invalid email format: {email}")

    # Validate social_links
    if social_links:
        if len(social_links) > 5:
            raise ValueError(
                f"ProfileCard supports up to 5 social links, got {len(social_links)}. "
                "Consider using only the most important platforms."
            )

        # Validate that all social_links have required keys
        for i, link in enumerate(social_links):
            if "platform" not in link:
                raise ValueError(f"Social link {i} missing required key: 'platform'")
            if "url" not in link:
                raise ValueError(f"Social link {i} missing required key: 'url'")

    props = {
        "name": name.strip(),
        "title": title.strip(),
    }

    # Add optional fields
    if bio:
        props["bio"] = bio

    if avatar_url:
        props["avatarUrl"] = avatar_url

    if contact:
        props["contact"] = contact

    if social_links:
        props["socialLinks"] = social_links

    return generate_component("a2ui.ProfileCard", props)


def generate_company_card(
    name: str,
    description: str,
    logo_url: str | None = None,
    website: str | None = None,
    headquarters: str | None = None,
    founded_year: int | None = None,
    employee_count: str | None = None,
    industries: list[str] | None = None
) -> A2UIComponent:
    """
    Generate a CompanyCard A2UI component for company profiles.

    Creates a company card component for company information, partner profiles,
    and vendor cards. Supports company metadata and industry categorization.

    Args:
        name: Company name (e.g., "Acme Corp", "TechStart Inc.")
        description: Company description/summary
        logo_url: Optional URL to company logo
        website: Optional company website URL (validated)
        headquarters: Optional headquarters location (e.g., "San Francisco, CA")
        founded_year: Optional founding year (validated 1800-current year)
        employee_count: Optional employee count range (e.g., "100-500", "1000+")
        industries: Optional list of industries/sectors (max 5)

    Returns:
        A2UIComponent configured as CompanyCard

    Raises:
        ValueError: If name or description is empty
        ValueError: If website URL format is invalid
        ValueError: If founded_year is not between 1800 and current year
        ValueError: If industries list exceeds 5 items

    Examples:
        >>> # Basic company card
        >>> card = generate_company_card(
        ...     name="Acme Corp",
        ...     description="Leading provider of innovative solutions"
        ... )

        >>> # Company card with all features
        >>> card = generate_company_card(
        ...     name="TechStart Inc.",
        ...     description="AI-powered analytics platform",
        ...     logo_url="https://example.com/logo.png",
        ...     website="https://techstart.com",
        ...     headquarters="San Francisco, CA",
        ...     founded_year=2015,
        ...     employee_count="100-500",
        ...     industries=["Technology", "Artificial Intelligence", "Analytics"]
        ... )
    """
    from datetime import datetime

    # Validate name
    if not name or not name.strip():
        raise ValueError("CompanyCard name cannot be empty")

    # Validate description
    if not description or not description.strip():
        raise ValueError("CompanyCard description cannot be empty")

    # Validate website URL format if provided
    if website:
        if not website.startswith(("http://", "https://")):
            raise ValueError(f"Website URL must start with http:// or https://, got: {website}")

    # Validate founded_year if provided
    if founded_year is not None:
        current_year = datetime.now().year
        if founded_year < 1800 or founded_year > current_year:
            raise ValueError(
                f"Founded year must be between 1800 and {current_year}, got: {founded_year}"
            )

    # Validate industries
    if industries:
        if len(industries) > 5:
            raise ValueError(
                f"CompanyCard supports up to 5 industries, got {len(industries)}. "
                "Consider using only the most relevant industries."
            )

    props = {
        "name": name.strip(),
        "description": description.strip(),
    }

    # Add optional fields
    if logo_url:
        props["logoUrl"] = logo_url

    if website:
        props["website"] = website

    if headquarters:
        props["headquarters"] = headquarters

    if founded_year is not None:
        props["foundedYear"] = founded_year

    if employee_count:
        props["employeeCount"] = employee_count

    if industries:
        props["industries"] = industries

    return generate_component("a2ui.CompanyCard", props)


def generate_quote_card(
    text: str,
    author: str,
    source: str | None = None,
    highlight: bool = False
) -> A2UIComponent:
    """
    Generate a QuoteCard A2UI component for quotes and testimonials.

    Creates a quote card component for testimonials, famous quotes, and
    inspirational content. Supports highlighting for featured quotes.

    Args:
        text: Quote text/content (up to 500 characters)
        author: Person who said/wrote the quote
        source: Optional source (book, article, speech, etc.)
        highlight: Whether to highlight as featured quote (default: False)

    Returns:
        A2UIComponent configured as QuoteCard

    Raises:
        ValueError: If text is empty
        ValueError: If text exceeds 500 characters
        ValueError: If author is empty

    Examples:
        >>> # Basic quote card
        >>> card = generate_quote_card(
        ...     text="The best way to predict the future is to invent it.",
        ...     author="Alan Kay"
        ... )

        >>> # Quote card with all features
        >>> card = generate_quote_card(
        ...     text="Stay hungry, stay foolish.",
        ...     author="Steve Jobs",
        ...     source="Stanford Commencement Speech, 2005",
        ...     highlight=True
        ... )

        >>> # Testimonial quote
        >>> card = generate_quote_card(
        ...     text="This product changed how we work. Highly recommended!",
        ...     author="Jane Smith",
        ...     source="TechCrunch Review"
        ... )
    """
    # Validate text
    if not text or not text.strip():
        raise ValueError("QuoteCard text cannot be empty")

    # Validate text length
    if len(text.strip()) > 500:
        raise ValueError(
            f"QuoteCard text must be 500 characters or less, got {len(text.strip())} characters"
        )

    # Validate author
    if not author or not author.strip():
        raise ValueError("QuoteCard author cannot be empty")

    props = {
        "text": text.strip(),
        "author": author.strip(),
        "highlight": highlight,
    }

    # Add optional source
    if source:
        props["source"] = source

    return generate_component("a2ui.QuoteCard", props)


def generate_expert_tip(
    title: str,
    content: str,
    expert_name: str | None = None,
    difficulty: str | None = None,
    category: str | None = None
) -> A2UIComponent:
    """
    Generate an ExpertTip A2UI component for expert advice and tips.

    Creates an expert tip component for tips, advice, best practices, and tutorials.
    Supports difficulty levels and categorization.

    Args:
        title: Tip title/heading
        content: Tip content/description
        expert_name: Optional name of the expert providing the tip
        difficulty: Optional difficulty level - "beginner", "intermediate", or "advanced"
        category: Optional category (e.g., "development", "design", "productivity")

    Returns:
        A2UIComponent configured as ExpertTip

    Raises:
        ValueError: If title or content is empty
        ValueError: If difficulty is not valid

    Examples:
        >>> # Basic expert tip
        >>> tip = generate_expert_tip(
        ...     title="Use Async/Await",
        ...     content="Always use async/await instead of callbacks for cleaner code"
        ... )

        >>> # Expert tip with all features
        >>> tip = generate_expert_tip(
        ...     title="Optimize React Performance",
        ...     content="Use React.memo() to prevent unnecessary re-renders of components",
        ...     expert_name="Sarah Johnson",
        ...     difficulty="intermediate",
        ...     category="development"
        ... )

        >>> # Beginner tip
        >>> tip = generate_expert_tip(
        ...     title="Git Commit Messages",
        ...     content="Write clear, descriptive commit messages in present tense",
        ...     expert_name="John Doe",
        ...     difficulty="beginner",
        ...     category="productivity"
        ... )
    """
    # Validate title
    if not title or not title.strip():
        raise ValueError("ExpertTip title cannot be empty")

    # Validate content
    if not content or not content.strip():
        raise ValueError("ExpertTip content cannot be empty")

    # Validate difficulty if provided
    if difficulty:
        valid_difficulties = {"beginner", "intermediate", "advanced"}
        if difficulty not in valid_difficulties:
            raise ValueError(
                f"Invalid difficulty: {difficulty}. "
                f"Must be one of: {', '.join(valid_difficulties)}"
            )

    props = {
        "title": title.strip(),
        "content": content.strip(),
    }

    # Add optional fields
    if expert_name:
        props["expertName"] = expert_name

    if difficulty:
        props["difficulty"] = difficulty

    if category:
        props["category"] = category

    return generate_component("a2ui.ExpertTip", props)


# =============================================================================
# SUMMARY & OVERVIEW COMPONENT GENERATORS
# =============================================================================


def generate_tldr(
    content: str,
    max_length: int = 200
) -> A2UIComponent:
    """
    Generate a TLDR (Too Long; Didn't Read) A2UI component for quick summaries.

    Creates a concise summary component for highlighting key information at a glance.
    Ideal for summarizing articles, research papers, or long-form content.

    Args:
        content: Short summary text (max 300 characters)
        max_length: Optional maximum character length for display (default 200)

    Returns:
        A2UIComponent configured as TLDR

    Raises:
        ValueError: If content is empty
        ValueError: If content exceeds 300 characters
        ValueError: If max_length is not positive

    Examples:
        >>> # Basic TLDR
        >>> tldr = generate_tldr(
        ...     "AI market expected to reach $196B by 2030, driven by enterprise adoption."
        ... )

        >>> # TLDR with custom max length
        >>> tldr = generate_tldr(
        ...     "Study shows 73% of organizations plan to adopt AI within 2 years.",
        ...     max_length=150
        ... )
    """
    # Validate content
    if not content or not content.strip():
        raise ValueError("TLDR content cannot be empty")

    content_stripped = content.strip()
    if len(content_stripped) > 300:
        raise ValueError(
            f"TLDR content must be 300 characters or less, got {len(content_stripped)} characters"
        )

    # Validate max_length
    if max_length <= 0:
        raise ValueError(f"max_length must be positive, got {max_length}")

    props = {
        "content": content_stripped,
        "maxLength": max_length,
    }

    return generate_component("a2ui.TLDR", props)


def generate_key_takeaways(
    items: list[str],
    category: str | None = None,
    icon: str | None = None
) -> A2UIComponent:
    """
    Generate a KeyTakeaways A2UI component for highlighting main points.

    Creates a component for displaying key points, insights, learnings, conclusions,
    or recommendations from content. Supports categorization and custom icons.

    Args:
        items: List of 1-10 key points/takeaways
        category: Optional category type - "insights", "learnings", "conclusions", "recommendations"
        icon: Optional icon name for the takeaways

    Returns:
        A2UIComponent configured as KeyTakeaways

    Raises:
        ValueError: If items list is empty or has more than 10 items
        ValueError: If any item is empty
        ValueError: If category is not valid

    Examples:
        >>> # Basic key takeaways
        >>> takeaways = generate_key_takeaways([
        ...     "AI adoption increasing across industries",
        ...     "Cloud infrastructure is critical for AI deployment",
        ...     "Data quality remains biggest challenge"
        ... ])

        >>> # Categorized takeaways with icon
        >>> takeaways = generate_key_takeaways(
        ...     items=[
        ...         "Focus on user experience first",
        ...         "Iterate based on feedback",
        ...         "Measure everything"
        ...     ],
        ...     category="insights",
        ...     icon="lightbulb"
        ... )
    """
    # Validate items count
    if not items:
        raise ValueError("KeyTakeaways must have at least 1 item")

    if len(items) > 10:
        raise ValueError(
            f"KeyTakeaways can have at most 10 items, got {len(items)} items"
        )

    # Validate each item
    for i, item in enumerate(items):
        if not item or not item.strip():
            raise ValueError(f"KeyTakeaways item {i} cannot be empty")

    # Validate category if provided
    if category:
        valid_categories = {"insights", "learnings", "conclusions", "recommendations"}
        if category not in valid_categories:
            raise ValueError(
                f"Invalid category: {category}. "
                f"Must be one of: {', '.join(sorted(valid_categories))}"
            )

    props = {
        "items": [item.strip() for item in items],
    }

    # Add optional fields
    if category:
        props["category"] = category

    if icon:
        props["icon"] = icon

    return generate_component("a2ui.KeyTakeaways", props)


def generate_executive_summary(
    title: str,
    summary: str,
    key_metrics: dict[str, str] | None = None,
    recommendations: list[str] | None = None
) -> A2UIComponent:
    """
    Generate an ExecutiveSummary A2UI component for detailed business summaries.

    Creates a comprehensive summary component for business reports, research papers,
    or complex content requiring detailed overview with metrics and recommendations.

    Args:
        title: Summary title/heading
        summary: Detailed summary text (50-2000 characters)
        key_metrics: Optional dict of metric name to value pairs
        recommendations: Optional list of 1-5 recommended actions

    Returns:
        A2UIComponent configured as ExecutiveSummary

    Raises:
        ValueError: If title or summary is empty
        ValueError: If summary is not between 50-2000 characters
        ValueError: If recommendations list has more than 5 items

    Examples:
        >>> # Basic executive summary
        >>> summary = generate_executive_summary(
        ...     title="Q4 2024 AI Market Analysis",
        ...     summary="The AI market showed significant growth in Q4 2024..."
        ... )

        >>> # Full executive summary with metrics and recommendations
        >>> summary = generate_executive_summary(
        ...     title="Annual AI Adoption Report",
        ...     summary="Enterprise AI adoption reached record levels in 2024, "
        ...             "with 73% of Fortune 500 companies implementing AI solutions...",
        ...     key_metrics={
        ...         "Market Size": "$196B",
        ...         "Growth Rate": "+23%",
        ...         "Adoption Rate": "73%"
        ...     },
        ...     recommendations=[
        ...         "Invest in AI infrastructure",
        ...         "Prioritize data quality",
        ...         "Build internal AI expertise"
        ...     ]
        ... )
    """
    # Validate title
    if not title or not title.strip():
        raise ValueError("ExecutiveSummary title cannot be empty")

    # Validate summary
    if not summary or not summary.strip():
        raise ValueError("ExecutiveSummary summary cannot be empty")

    summary_stripped = summary.strip()
    if len(summary_stripped) < 50:
        raise ValueError(
            f"ExecutiveSummary summary must be at least 50 characters, got {len(summary_stripped)} characters"
        )

    if len(summary_stripped) > 2000:
        raise ValueError(
            f"ExecutiveSummary summary must be 2000 characters or less, got {len(summary_stripped)} characters"
        )

    # Validate recommendations if provided
    if recommendations is not None:
        if len(recommendations) > 5:
            raise ValueError(
                f"ExecutiveSummary can have at most 5 recommendations, got {len(recommendations)} recommendations"
            )

        for i, rec in enumerate(recommendations):
            if not rec or not rec.strip():
                raise ValueError(f"ExecutiveSummary recommendation {i} cannot be empty")

    props = {
        "title": title.strip(),
        "summary": summary_stripped,
    }

    # Add optional fields
    if key_metrics:
        props["keyMetrics"] = key_metrics

    if recommendations:
        props["recommendations"] = [rec.strip() for rec in recommendations]

    return generate_component("a2ui.ExecutiveSummary", props)


def generate_table_of_contents(
    items: list[dict[str, str]],
    include_page_numbers: bool = False
) -> A2UIComponent:
    """
    Generate a TableOfContents A2UI component for navigating long documents.

    Creates a hierarchical table of contents for navigating sections in long documents,
    articles, or reports. Supports nested heading levels and anchor linking.

    Args:
        items: List of 1-50 section entries with 'title', optional 'anchor', and optional 'level' (0-3)
        include_page_numbers: Whether to show page numbers (default False for web, True for PDFs)

    Returns:
        A2UIComponent configured as TableOfContents

    Raises:
        ValueError: If items list is empty or has more than 50 items
        ValueError: If any item is missing required 'title' field
        ValueError: If level is not in range 0-3

    Examples:
        >>> # Basic table of contents
        >>> toc = generate_table_of_contents([
        ...     {"title": "Introduction", "anchor": "intro"},
        ...     {"title": "Methodology", "anchor": "methods"},
        ...     {"title": "Results", "anchor": "results"},
        ...     {"title": "Conclusion", "anchor": "conclusion"}
        ... ])

        >>> # Hierarchical table of contents with levels
        >>> toc = generate_table_of_contents(
        ...     items=[
        ...         {"title": "Introduction", "anchor": "intro", "level": 0},
        ...         {"title": "Background", "anchor": "background", "level": 1},
        ...         {"title": "Historical Context", "anchor": "history", "level": 2},
        ...         {"title": "Current State", "anchor": "current", "level": 2},
        ...         {"title": "Methodology", "anchor": "methods", "level": 0},
        ...         {"title": "Data Collection", "anchor": "data", "level": 1},
        ...         {"title": "Analysis Approach", "anchor": "analysis", "level": 1}
        ...     ],
        ...     include_page_numbers=False
        ... )
    """
    # Validate items count
    if not items:
        raise ValueError("TableOfContents must have at least 1 item")

    if len(items) > 50:
        raise ValueError(
            f"TableOfContents can have at most 50 items, got {len(items)} items"
        )

    # Validate each item
    validated_items = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"TableOfContents item {i} must be a dictionary")

        if "title" not in item:
            raise ValueError(f"TableOfContents item {i} must have 'title' field")

        if not item["title"] or not item["title"].strip():
            raise ValueError(f"TableOfContents item {i} title cannot be empty")

        # Validate level if provided
        if "level" in item:
            level = item["level"]
            if not isinstance(level, int) or level < 0 or level > 3:
                raise ValueError(
                    f"TableOfContents item {i} level must be 0-3, got {level}"
                )

        validated_item = {"title": item["title"].strip()}

        # Add optional anchor
        if "anchor" in item and item["anchor"]:
            validated_item["anchor"] = item["anchor"]

        # Add optional level (default to 0)
        validated_item["level"] = item.get("level", 0)

        validated_items.append(validated_item)

    props = {
        "items": validated_items,
        "includePageNumbers": include_page_numbers,
    }

    return generate_component("a2ui.TableOfContents", props)


# =============================================================================
# INSTRUCTIONAL COMPONENT GENERATORS
# =============================================================================


def detect_language(code: str, filename: str = None) -> str:
    """
    Detect programming language from code content or filename.

    Analyzes code patterns and syntax to determine the programming language.
    Uses filename extension as a hint when provided.

    Args:
        code: The code content to analyze
        filename: Optional filename to extract extension hint

    Returns:
        Language identifier (python, javascript, java, etc.) or "text" if unknown

    Examples:
        >>> detect_language("def hello():\\n    print('hi')")
        'python'

        >>> detect_language("function hello() { console.log('hi'); }")
        'javascript'

        >>> detect_language("SELECT * FROM users", "query.sql")
        'sql'
    """
    code = code.strip()

    # Try filename extension first
    if filename:
        ext = filename.split('.')[-1].lower()
        extension_map = {
            'py': 'python',
            'js': 'javascript',
            'jsx': 'javascript',
            'ts': 'typescript',
            'tsx': 'typescript',
            'java': 'java',
            'cpp': 'cpp',
            'c': 'c',
            'cs': 'csharp',
            'go': 'go',
            'rs': 'rust',
            'rb': 'ruby',
            'php': 'php',
            'swift': 'swift',
            'kt': 'kotlin',
            'scala': 'scala',
            'r': 'r',
            'sql': 'sql',
            'sh': 'bash',
            'bash': 'bash',
            'zsh': 'zsh',
            'ps1': 'powershell',
            'html': 'html',
            'css': 'css',
            'scss': 'scss',
            'json': 'json',
            'xml': 'xml',
            'yaml': 'yaml',
            'yml': 'yaml',
            'md': 'markdown',
            'tex': 'latex',
        }
        if ext in extension_map:
            return extension_map[ext]

    # Pattern-based detection
    patterns = [
        # Python
        (r'^\s*(def|class|import|from .* import|if __name__|async def)', 'python'),
        (r'print\s*\(|\.append\(|\.extend\(', 'python'),

        # TypeScript (check before JavaScript since TS is superset of JS)
        (r':\s*(string|number|boolean|any)\s*[;=)]', 'typescript'),

        # JavaScript
        (r'^\s*(function|const|let|var|import |export |=>)', 'javascript'),
        (r'console\.log|\.map\(|\.filter\(|\.reduce\(', 'javascript'),

        # Java
        (r'^\s*(public|private|protected)\s+(class|interface|static|void)', 'java'),
        (r'System\.out\.println|\.toString\(\)|new \w+\(', 'java'),

        # C/C++
        (r'^\s*#include\s*<|^\s*#define\s+', 'cpp'),
        (r'std::|cout\s*<<|cin\s*>>', 'cpp'),
        (r'printf\s*\(|scanf\s*\(|malloc\s*\(', 'c'),

        # Go
        (r'^\s*func\s+\w+\s*\(|package\s+\w+', 'go'),
        (r'fmt\.Print|:=\s*', 'go'),

        # Rust
        (r'^\s*fn\s+\w+|let\s+mut\s+', 'rust'),
        (r'println!\(|impl\s+\w+', 'rust'),

        # Ruby
        (r'^\s*def\s+\w+|^\s*class\s+\w+|^\s*module\s+', 'ruby'),
        (r'puts\s+|end\s*$|@\w+\s*=', 'ruby'),

        # PHP
        (r'<\?php|^\s*\$\w+\s*=', 'php'),

        # SQL
        (r'^\s*(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP)\s+', 'sql'),

        # Shell/Bash
        (r'^\s*#!/bin/(bash|sh)|^\s*export\s+\w+=', 'bash'),

        # HTML
        (r'^\s*<!DOCTYPE html>|<html|<head|<body|<div', 'html'),

        # CSS
        (r'^\s*[\w\-\.#]+\s*\{|\s*(margin|padding|color|background):', 'css'),

        # JSON
        (r'^\s*\{[\s\n]*"[\w\-]+":', 'json'),

        # YAML
        (r'^\w+:\s*$|^\s+-\s+\w+:', 'yaml'),

        # Markdown
        (r'^#+\s+\w+|^\*\*\w+|^\[.*\]\(.*\)', 'markdown'),
    ]

    for pattern, language in patterns:
        if re.search(pattern, code, re.MULTILINE | re.IGNORECASE):
            return language

    return 'text'


def generate_step_card(
    step_number: int,
    title: str,
    description: str,
    details: str = None,
    icon: str = None,
    action: str = None
) -> A2UIComponent:
    """
    Generate a StepCard A2UI component for tutorial/guide steps.

    Creates a step card component for displaying sequential instructions
    in tutorials, guides, or step-by-step workflows. Each card represents
    a single step with a number, title, and description.

    Args:
        step_number: Step number (1-999, must be positive)
        title: Step title/heading
        description: Brief step description or instruction
        details: Optional longer explanation or additional context
        icon: Optional icon name for visual representation
        action: Optional call-to-action text (e.g., "Try it now", "Learn more")

    Returns:
        A2UIComponent configured as StepCard

    Raises:
        ValueError: If step_number is not positive

    Examples:
        >>> # Basic step card
        >>> step = generate_step_card(
        ...     step_number=1,
        ...     title="Install Dependencies",
        ...     description="Run npm install to install all required packages"
        ... )

        >>> # Step card with all features
        >>> step = generate_step_card(
        ...     step_number=2,
        ...     title="Configure Environment",
        ...     description="Set up your environment variables",
        ...     details="Create a .env file in the project root with your API keys",
        ...     icon="settings",
        ...     action="View example .env file"
        ... )
    """
    # Validate step_number
    if not isinstance(step_number, int) or step_number <= 0:
        raise ValueError(f"step_number must be a positive integer, got: {step_number}")

    if step_number > 999:
        raise ValueError(f"step_number must be 999 or less, got: {step_number}")

    props = {
        "stepNumber": step_number,
        "title": title.strip(),
        "description": description.strip(),
    }

    # Add optional fields
    if details:
        props["details"] = details.strip()

    if icon:
        props["icon"] = icon.strip()

    if action:
        props["action"] = action.strip()

    return generate_component("a2ui.StepCard", props)


def generate_code_block(
    code: str,
    language: str = None,
    filename: str = None,
    highlight_lines: list[int] = None,
    copy_button: bool = True
) -> A2UIComponent:
    """
    Generate a CodeBlock A2UI component for displaying code snippets.

    Creates a code block component with syntax highlighting, optional line
    highlighting, and copy functionality. Automatically detects language
    if not specified.

    Args:
        code: Code content to display
        language: Programming language (auto-detected if None)
        filename: Optional filename to display and help with language detection
        highlight_lines: Optional list of line numbers to highlight (1-indexed)
        copy_button: Whether to show copy button (default: True)

    Returns:
        A2UIComponent configured as CodeBlock

    Raises:
        ValueError: If code is empty
        ValueError: If highlight_lines contains invalid line numbers

    Examples:
        >>> # Basic code block (auto-detect language)
        >>> code = generate_code_block(
        ...     code="def hello():\\n    print('Hello, world!')"
        ... )

        >>> # Code block with all features
        >>> code = generate_code_block(
        ...     code="const x = 10;\\nconst y = 20;\\nconst sum = x + y;",
        ...     language="javascript",
        ...     filename="sum.js",
        ...     highlight_lines=[3],
        ...     copy_button=True
        ... )

        >>> # Code block from file
        >>> code = generate_code_block(
        ...     code="SELECT * FROM users WHERE active = 1",
        ...     filename="query.sql"
        ... )
    """
    # Validate code
    if not code or not code.strip():
        raise ValueError("code cannot be empty")

    code = code.strip()

    # Auto-detect language if not provided
    if language is None:
        language = detect_language(code, filename)

    # Validate highlight_lines if provided
    if highlight_lines:
        code_lines = code.split('\n')
        num_lines = len(code_lines)
        for line_num in highlight_lines:
            if not isinstance(line_num, int) or line_num < 1 or line_num > num_lines:
                raise ValueError(
                    f"Invalid line number {line_num} in highlight_lines. "
                    f"Must be between 1 and {num_lines}"
                )

    props = {
        "code": code,
        "language": language,
        "copyButton": copy_button,
    }

    # Add optional fields
    if filename:
        props["filename"] = filename.strip()

    if highlight_lines:
        props["highlightLines"] = sorted(highlight_lines)

    return generate_component("a2ui.CodeBlock", props)


def generate_callout_card(
    type: str,
    title: str,
    content: str,
    icon: str = None
) -> A2UIComponent:
    """
    Generate a CalloutCard A2UI component for highlighted information.

    Creates a callout card component for displaying important information,
    tips, warnings, or notes with visual differentiation by type.

    Args:
        type: Callout type - "info", "warning", "success", "error", "tip", or "note"
        title: Callout title/heading
        content: Callout content/message
        icon: Optional custom icon name (defaults based on type)

    Returns:
        A2UIComponent configured as CalloutCard

    Raises:
        ValueError: If type is not valid

    Examples:
        >>> # Info callout
        >>> callout = generate_callout_card(
        ...     type="info",
        ...     title="Getting Started",
        ...     content="Follow the steps below to set up your project"
        ... )

        >>> # Warning callout with custom icon
        >>> callout = generate_callout_card(
        ...     type="warning",
        ...     title="Breaking Change",
        ...     content="This version introduces breaking changes to the API",
        ...     icon="alert-triangle"
        ... )

        >>> # Success tip
        >>> callout = generate_callout_card(
        ...     type="tip",
        ...     title="Pro Tip",
        ...     content="Use keyboard shortcuts to speed up your workflow"
        ... )
    """
    # Validate type
    valid_types = {"info", "warning", "success", "error", "tip", "note"}
    if type not in valid_types:
        raise ValueError(
            f"Invalid type: {type}. Must be one of: {', '.join(valid_types)}"
        )

    props = {
        "type": type,
        "title": title.strip(),
        "content": content.strip(),
    }

    # Add optional icon
    if icon:
        props["icon"] = icon.strip()

    return generate_component("a2ui.CalloutCard", props)


def generate_command_card(
    command: str,
    description: str = None,
    output: str = None,
    platform: str = None,
    copy_button: bool = True
) -> A2UIComponent:
    """
    Generate a CommandCard A2UI component for CLI commands.

    Creates a command card component for displaying terminal/shell commands
    with optional description, expected output, and platform-specific styling.

    Args:
        command: The command text (required)
        description: Optional description of what the command does
        output: Optional expected output from the command
        platform: Optional platform identifier - "bash", "zsh", "powershell", "cmd", or "terminal"
        copy_button: Whether to show copy button (default: True)

    Returns:
        A2UIComponent configured as CommandCard

    Raises:
        ValueError: If command is empty
        ValueError: If platform is not valid

    Examples:
        >>> # Basic command
        >>> cmd = generate_command_card(
        ...     command="npm install"
        ... )

        >>> # Command with all features
        >>> cmd = generate_command_card(
        ...     command="git clone https://github.com/user/repo.git",
        ...     description="Clone the repository to your local machine",
        ...     output="Cloning into 'repo'...\\nDone.",
        ...     platform="bash",
        ...     copy_button=True
        ... )

        >>> # PowerShell command
        >>> cmd = generate_command_card(
        ...     command="Get-Process | Where-Object {$_.CPU -gt 100}",
        ...     description="Find processes using high CPU",
        ...     platform="powershell"
        ... )
    """
    # Validate command
    if not command or not command.strip():
        raise ValueError("command cannot be empty")

    # Validate platform if provided
    if platform:
        valid_platforms = {"bash", "zsh", "powershell", "cmd", "terminal"}
        if platform not in valid_platforms:
            raise ValueError(
                f"Invalid platform: {platform}. "
                f"Must be one of: {', '.join(valid_platforms)}"
            )

    props = {
        "command": command.strip(),
        "copyButton": copy_button,
    }

    # Add optional fields
    if description:
        props["description"] = description.strip()

    if output:
        props["output"] = output.strip()

    if platform:
        props["platform"] = platform

    return generate_component("a2ui.CommandCard", props)


def generate_comparison_table(
    headers: list[str],
    rows: list[dict[str, any]],
    highlighted_column: int | None = None
) -> A2UIComponent:
    """
    Generate a ComparisonTable A2UI component for side-by-side comparisons.

    Creates a comparison table for viewing multiple items or options side by side.
    Ideal for product comparisons, feature comparisons, or any data requiring
    structured comparison across multiple dimensions.

    Args:
        headers: List of column names/headers (2-10 columns)
        rows: List of row data dictionaries where keys match headers
        highlighted_column: Optional index (0-based) of column to highlight (typically the winner)

    Returns:
        A2UIComponent configured as ComparisonTable

    Raises:
        ValueError: If headers list has fewer than 2 or more than 10 items
        ValueError: If rows list is empty or has more than 50 rows
        ValueError: If row data keys don't match headers
        ValueError: If highlighted_column is out of range

    Examples:
        >>> # Product comparison
        >>> table = generate_comparison_table(
        ...     headers=["Feature", "Product A", "Product B", "Product C"],
        ...     rows=[
        ...         {"Feature": "Price", "Product A": "$99", "Product B": "$149", "Product C": "$199"},
        ...         {"Feature": "Storage", "Product A": "128GB", "Product B": "256GB", "Product C": "512GB"},
        ...         {"Feature": "RAM", "Product A": "8GB", "Product B": "16GB", "Product C": "32GB"}
        ...     ],
        ...     highlighted_column=1
        ... )

        >>> # Browser feature comparison
        >>> table = generate_comparison_table(
        ...     headers=["Browser", "Speed", "Privacy", "Extensions"],
        ...     rows=[
        ...         {"Browser": "Chrome", "Speed": "Fast", "Privacy": "Low", "Extensions": "Many"},
        ...         {"Browser": "Firefox", "Speed": "Fast", "Privacy": "High", "Extensions": "Many"},
        ...         {"Browser": "Safari", "Speed": "Fast", "Privacy": "Medium", "Extensions": "Few"}
        ...     ]
        ... )
    """
    # Validate headers
    if len(headers) < 2:
        raise ValueError("ComparisonTable requires at least 2 columns")

    if len(headers) > 10:
        raise ValueError(
            f"ComparisonTable supports up to 10 columns, got {len(headers)}"
        )

    # Validate rows
    if not rows:
        raise ValueError("ComparisonTable requires at least 1 row")

    if len(rows) > 50:
        raise ValueError(
            f"ComparisonTable supports up to 50 rows, got {len(rows)}"
        )

    # Validate each row has data for all headers
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ValueError(f"Row {i} must be a dictionary")

        for header in headers:
            if header not in row:
                raise ValueError(f"Row {i} missing data for header '{header}'")

    # Validate highlighted_column if provided
    if highlighted_column is not None:
        if not isinstance(highlighted_column, int):
            raise ValueError("highlighted_column must be an integer")

        if highlighted_column < 0 or highlighted_column >= len(headers):
            raise ValueError(
                f"highlighted_column must be 0-{len(headers)-1}, got {highlighted_column}"
            )

    props = {
        "headers": headers,
        "rows": rows,
    }

    if highlighted_column is not None:
        props["highlightedColumn"] = highlighted_column

    return generate_component("a2ui.ComparisonTable", props)


def generate_vs_card(
    item_a: dict[str, str],
    item_b: dict[str, str],
    winner: str | None = None
) -> A2UIComponent:
    """
    Generate a VsCard A2UI component for "X vs Y" head-to-head comparisons.

    Creates a visual card comparing two items in a "versus" format.
    Ideal for product matchups, technology comparisons, or any binary comparison.

    Args:
        item_a: Dictionary with "name" and "description" for first item
        item_b: Dictionary with "name" and "description" for second item
        winner: Optional winner indicator ("a", "b", or None for neutral comparison)

    Returns:
        A2UIComponent configured as VsCard

    Raises:
        ValueError: If item_a or item_b missing required keys
        ValueError: If winner is not "a", "b", or None

    Examples:
        >>> # Technology comparison
        >>> card = generate_vs_card(
        ...     item_a={"name": "React", "description": "Component-based UI library"},
        ...     item_b={"name": "Vue", "description": "Progressive JavaScript framework"},
        ...     winner="a"
        ... )

        >>> # Product comparison (neutral)
        >>> card = generate_vs_card(
        ...     item_a={"name": "MacBook Pro", "description": "Apple's premium laptop"},
        ...     item_b={"name": "Dell XPS", "description": "Dell's flagship ultrabook"}
        ... )
    """
    # Validate item_a
    if not isinstance(item_a, dict):
        raise ValueError("item_a must be a dictionary")

    if "name" not in item_a:
        raise ValueError("item_a must have 'name' field")

    if "description" not in item_a:
        raise ValueError("item_a must have 'description' field")

    # Validate item_b
    if not isinstance(item_b, dict):
        raise ValueError("item_b must be a dictionary")

    if "name" not in item_b:
        raise ValueError("item_b must have 'name' field")

    if "description" not in item_b:
        raise ValueError("item_b must have 'description' field")

    # Validate winner
    if winner is not None and winner not in ["a", "b"]:
        raise ValueError("winner must be 'a', 'b', or None")

    props = {
        "itemA": {
            "name": item_a["name"],
            "description": item_a["description"]
        },
        "itemB": {
            "name": item_b["name"],
            "description": item_b["description"]
        }
    }

    if winner is not None:
        props["winner"] = winner

    return generate_component("a2ui.VsCard", props)


def generate_feature_matrix(
    features: list[str],
    items: list[dict[str, any]],
    title: str | None = None
) -> A2UIComponent:
    """
    Generate a FeatureMatrix A2UI component for feature comparison across items.

    Creates a matrix showing which features are included/excluded for each item.
    Ideal for capability matrices, feature comparison charts, or product tiers.

    Args:
        features: List of feature names (1-20 features)
        items: List of item dictionaries with "name" and boolean feature flags
        title: Optional matrix title

    Returns:
        A2UIComponent configured as FeatureMatrix

    Raises:
        ValueError: If features list is empty or has more than 20 items
        ValueError: If items list is empty or has more than 10 items
        ValueError: If any item missing "name" field
        ValueError: If feature values are not boolean

    Examples:
        >>> # Software tier comparison
        >>> matrix = generate_feature_matrix(
        ...     features=["API Access", "Priority Support", "Advanced Analytics", "Custom Branding"],
        ...     items=[
        ...         {"name": "Free", "API Access": False, "Priority Support": False,
        ...          "Advanced Analytics": False, "Custom Branding": False},
        ...         {"name": "Pro", "API Access": True, "Priority Support": False,
        ...          "Advanced Analytics": True, "Custom Branding": False},
        ...         {"name": "Enterprise", "API Access": True, "Priority Support": True,
        ...          "Advanced Analytics": True, "Custom Branding": True}
        ...     ],
        ...     title="Plan Features"
        ... )

        >>> # Phone model comparison
        >>> matrix = generate_feature_matrix(
        ...     features=["5G", "Wireless Charging", "Water Resistant", "Face ID"],
        ...     items=[
        ...         {"name": "iPhone 12", "5G": True, "Wireless Charging": True,
        ...          "Water Resistant": True, "Face ID": True},
        ...         {"name": "iPhone 11", "5G": False, "Wireless Charging": True,
        ...          "Water Resistant": True, "Face ID": True}
        ...     ]
        ... )
    """
    # Validate features
    if not features:
        raise ValueError("FeatureMatrix requires at least 1 feature")

    if len(features) > 20:
        raise ValueError(
            f"FeatureMatrix supports up to 20 features, got {len(features)}"
        )

    # Validate items
    if not items:
        raise ValueError("FeatureMatrix requires at least 1 item")

    if len(items) > 10:
        raise ValueError(
            f"FeatureMatrix supports up to 10 items, got {len(items)}"
        )

    # Validate each item
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"Item {i} must be a dictionary")

        if "name" not in item:
            raise ValueError(f"Item {i} must have 'name' field")

        # Check that all features are present and boolean
        for feature in features:
            if feature not in item:
                raise ValueError(f"Item {i} missing feature '{feature}'")

            if not isinstance(item[feature], bool):
                raise ValueError(
                    f"Item {i} feature '{feature}' must be boolean, got {type(item[feature]).__name__}"
                )

    props = {
        "features": features,
        "items": items,
    }

    if title is not None:
        props["title"] = title

    return generate_component("a2ui.FeatureMatrix", props)


def generate_pricing_table(
    title: str,
    tiers: list[dict[str, any]],
    currency: str = "USD",
    features: list[str] | None = None
) -> A2UIComponent:
    """
    Generate a PricingTable A2UI component for displaying pricing tiers.

    Creates a pricing comparison table for services or products with multiple tiers.
    Ideal for SaaS pricing pages, subscription plans, or service comparisons.

    Args:
        title: Table title (e.g., "Choose Your Plan")
        tiers: List of 1-5 pricing tier dictionaries with name, price, description
        currency: Currency code (USD, EUR, GBP, etc.) - default USD
        features: Optional list of features to show in rows

    Returns:
        A2UIComponent configured as PricingTable

    Raises:
        ValueError: If title is empty
        ValueError: If tiers list is empty or has more than 5 tiers
        ValueError: If any tier missing required fields
        ValueError: If features length doesn't match features_included length

    Examples:
        >>> # SaaS pricing table
        >>> table = generate_pricing_table(
        ...     title="Choose Your Plan",
        ...     tiers=[
        ...         {
        ...             "name": "Starter",
        ...             "price": 9,
        ...             "description": "Perfect for individuals",
        ...             "features_included": [True, False, False]
        ...         },
        ...         {
        ...             "name": "Pro",
        ...             "price": 29,
        ...             "description": "For small teams",
        ...             "features_included": [True, True, False],
        ...             "recommended": True
        ...         },
        ...         {
        ...             "name": "Enterprise",
        ...             "price": 99,
        ...             "description": "For large organizations",
        ...             "features_included": [True, True, True]
        ...         }
        ...     ],
        ...     currency="USD",
        ...     features=["Basic Support", "Priority Support", "Custom Integrations"]
        ... )

        >>> # Simple pricing (no features)
        >>> table = generate_pricing_table(
        ...     title="Subscription Plans",
        ...     tiers=[
        ...         {"name": "Monthly", "price": 15, "description": "Billed monthly"},
        ...         {"name": "Yearly", "price": 150, "description": "Billed annually - Save 17%"}
        ...     ]
        ... )
    """
    # Validate title
    if not title or not title.strip():
        raise ValueError("PricingTable title cannot be empty")

    # Validate tiers
    if not tiers:
        raise ValueError("PricingTable requires at least 1 tier")

    if len(tiers) > 5:
        raise ValueError(
            f"PricingTable supports up to 5 tiers, got {len(tiers)}"
        )

    # Validate each tier
    for i, tier in enumerate(tiers):
        if not isinstance(tier, dict):
            raise ValueError(f"Tier {i} must be a dictionary")

        if "name" not in tier:
            raise ValueError(f"Tier {i} must have 'name' field")

        if "price" not in tier:
            raise ValueError(f"Tier {i} must have 'price' field")

        if "description" not in tier:
            raise ValueError(f"Tier {i} must have 'description' field")

        # Validate price is a number
        if not isinstance(tier["price"], (int, float)):
            raise ValueError(
                f"Tier {i} price must be a number, got {type(tier['price']).__name__}"
            )

        # If features provided, validate features_included
        if features and "features_included" in tier:
            if len(tier["features_included"]) != len(features):
                raise ValueError(
                    f"Tier {i} features_included must have {len(features)} items, "
                    f"got {len(tier['features_included'])}"
                )

    props = {
        "title": title.strip(),
        "tiers": tiers,
        "currency": currency,
    }

    if features is not None:
        props["features"] = features

    return generate_component("a2ui.PricingTable", props)


# ============================================================================
# LAYOUT COMPONENT GENERATORS
# ============================================================================


def generate_section(
    title: str,
    content: list[str],
    footer: str | None = None,
    style: str | None = None
) -> A2UIComponent:
    """
    Generate a Section A2UI component for grouping related content.

    Creates a section container with header, content area, and optional footer.
    Sections are used to organize dashboard content into logical groups with
    clear visual separation and hierarchy.

    Args:
        title: Section heading/title
        content: List of child component IDs to include in section body
        footer: Optional footer text or component ID
        style: Optional style variant ("default", "bordered", "elevated", "subtle")

    Returns:
        A2UIComponent configured as Section

    Raises:
        ValueError: If title is empty
        ValueError: If content list is empty
        ValueError: If style is not a valid option

    Examples:
        >>> # Basic section with content
        >>> section = generate_section(
        ...     title="Key Metrics",
        ...     content=["stat-1", "stat-2", "stat-3"]
        ... )

        >>> # Section with footer and style
        >>> section = generate_section(
        ...     title="Recent Activity",
        ...     content=["event-1", "event-2"],
        ...     footer="Updated 5 minutes ago",
        ...     style="elevated"
        ... )
    """
    # Validate title
    if not title or not title.strip():
        raise ValueError("Section title cannot be empty")

    # Validate content
    if not content:
        raise ValueError("Section requires at least 1 content item")

    if not isinstance(content, list):
        raise ValueError(f"Section content must be a list, got {type(content).__name__}")

    # Validate style if provided
    valid_styles = {"default", "bordered", "elevated", "subtle"}
    if style and style not in valid_styles:
        raise ValueError(
            f"Section style must be one of {valid_styles}, got: {style}"
        )

    props = {
        "title": title.strip(),
    }

    if footer:
        props["footer"] = footer

    if style:
        props["style"] = style

    component = generate_component("a2ui.Section", props)
    component.children = content

    return component


def generate_grid(
    columns: int,
    items: list[str],
    gap: str | None = None,
    align: str | None = None
) -> A2UIComponent:
    """
    Generate a Grid A2UI component for multi-column responsive layouts.

    Creates a responsive grid layout that automatically wraps items into the
    specified number of columns. Grid adapts to screen size and maintains
    consistent spacing.

    Args:
        columns: Number of columns (1-6)
        items: List of child component IDs to display in grid
        gap: Optional gap size ("sm", "md", "lg", or CSS value like "1rem")
        align: Optional vertical alignment ("start", "center", "end", "stretch")

    Returns:
        A2UIComponent configured as Grid

    Raises:
        ValueError: If columns is not between 1 and 6
        ValueError: If items list is empty
        ValueError: If align is not a valid option

    Examples:
        >>> # Basic 3-column grid
        >>> grid = generate_grid(
        ...     columns=3,
        ...     items=["card-1", "card-2", "card-3", "card-4", "card-5", "card-6"]
        ... )

        >>> # Grid with custom gap and alignment
        >>> grid = generate_grid(
        ...     columns=2,
        ...     items=["stat-1", "stat-2", "stat-3", "stat-4"],
        ...     gap="lg",
        ...     align="center"
        ... )
    """
    # Validate columns
    if not isinstance(columns, int):
        raise ValueError(f"Grid columns must be an integer, got {type(columns).__name__}")

    if columns < 1 or columns > 6:
        raise ValueError(f"Grid columns must be between 1 and 6, got {columns}")

    # Validate items
    if not items:
        raise ValueError("Grid requires at least 1 item")

    if not isinstance(items, list):
        raise ValueError(f"Grid items must be a list, got {type(items).__name__}")

    # Validate align if provided
    valid_align = {"start", "center", "end", "stretch"}
    if align and align not in valid_align:
        raise ValueError(
            f"Grid align must be one of {valid_align}, got: {align}"
        )

    props = {
        "columns": columns,
    }

    if gap:
        props["gap"] = gap

    if align:
        props["align"] = align

    component = generate_component("a2ui.Grid", props)
    component.children = items

    return component


def generate_columns(
    widths: list[str],
    items: list[str],
    gap: str | None = None
) -> A2UIComponent:
    """
    Generate a Columns A2UI component for flexible width column layouts.

    Creates a multi-column layout with custom width ratios for each column.
    Supports percentage-based, fractional, and fixed width specifications.

    Args:
        widths: List of width specifications (e.g., ["50%", "50%"], ["2fr", "1fr"], ["300px", "auto"])
        items: List of child component IDs, one per column
        gap: Optional gap size ("sm", "md", "lg", or CSS value like "1rem")

    Returns:
        A2UIComponent configured as Columns

    Raises:
        ValueError: If widths and items lists have different lengths
        ValueError: If widths or items list is empty
        ValueError: If more than 4 columns specified

    Examples:
        >>> # Two equal columns
        >>> cols = generate_columns(
        ...     widths=["50%", "50%"],
        ...     items=["main-content", "sidebar-content"]
        ... )

        >>> # Three columns with different widths
        >>> cols = generate_columns(
        ...     widths=["2fr", "1fr", "1fr"],
        ...     items=["content-1", "content-2", "content-3"],
        ...     gap="md"
        ... )
    """
    # Validate widths
    if not widths:
        raise ValueError("Columns requires at least 1 width specification")

    if not isinstance(widths, list):
        raise ValueError(f"Columns widths must be a list, got {type(widths).__name__}")

    if len(widths) > 4:
        raise ValueError(f"Columns supports up to 4 columns, got {len(widths)}")

    # Validate items
    if not items:
        raise ValueError("Columns requires at least 1 item")

    if not isinstance(items, list):
        raise ValueError(f"Columns items must be a list, got {type(items).__name__}")

    # Validate lengths match
    if len(widths) != len(items):
        raise ValueError(
            f"Columns widths and items must have same length. "
            f"Got {len(widths)} widths and {len(items)} items"
        )

    props = {
        "widths": widths,
    }

    if gap:
        props["gap"] = gap

    component = generate_component("a2ui.Columns", props)
    component.children = items

    return component


def generate_tabs(
    tabs_data: list[dict[str, Any]],
    active_tab: int = 0
) -> A2UIComponent:
    """
    Generate a Tabs A2UI component for tabbed interface organization.

    Creates a tabbed interface for organizing related content into separate
    views. Only one tab is visible at a time, reducing clutter and improving
    navigation.

    Args:
        tabs_data: List of tab dictionaries with "label" and "content" (list of component IDs)
        active_tab: Index of initially active tab (default: 0)

    Returns:
        A2UIComponent configured as Tabs

    Raises:
        ValueError: If tabs_data is empty
        ValueError: If active_tab index is out of range
        ValueError: If any tab missing "label" or "content" fields
        ValueError: If more than 8 tabs specified

    Examples:
        >>> # Basic tabs
        >>> tabs = generate_tabs(
        ...     tabs_data=[
        ...         {"label": "Overview", "content": ["summary-1", "stats-1"]},
        ...         {"label": "Details", "content": ["table-1", "chart-1"]},
        ...         {"label": "History", "content": ["timeline-1"]}
        ...     ]
        ... )

        >>> # Tabs with custom active tab
        >>> tabs = generate_tabs(
        ...     tabs_data=[
        ...         {"label": "All", "content": ["list-all"]},
        ...         {"label": "Active", "content": ["list-active"]},
        ...         {"label": "Completed", "content": ["list-completed"]}
        ...     ],
        ...     active_tab=1  # Start with "Active" tab
        ... )
    """
    # Validate tabs_data
    if not tabs_data:
        raise ValueError("Tabs requires at least 1 tab")

    if not isinstance(tabs_data, list):
        raise ValueError(f"Tabs tabs_data must be a list, got {type(tabs_data).__name__}")

    if len(tabs_data) > 8:
        raise ValueError(f"Tabs supports up to 8 tabs, got {len(tabs_data)}")

    # Validate each tab
    for i, tab in enumerate(tabs_data):
        if not isinstance(tab, dict):
            raise ValueError(f"Tab {i} must be a dictionary")

        if "label" not in tab:
            raise ValueError(f"Tab {i} must have 'label' field")

        if "content" not in tab:
            raise ValueError(f"Tab {i} must have 'content' field")

        if not isinstance(tab["content"], list):
            raise ValueError(
                f"Tab {i} content must be a list, got {type(tab['content']).__name__}"
            )

    # Validate active_tab
    if not isinstance(active_tab, int):
        raise ValueError(f"Tabs active_tab must be an integer, got {type(active_tab).__name__}")

    if active_tab < 0 or active_tab >= len(tabs_data):
        raise ValueError(
            f"Tabs active_tab must be between 0 and {len(tabs_data) - 1}, got {active_tab}"
        )

    props = {
        "tabs": [{"label": tab["label"]} for tab in tabs_data],
        "activeTab": active_tab,
    }

    # Build children structure as dict mapping tab indices to content
    children = {str(i): tab["content"] for i, tab in enumerate(tabs_data)}

    component = generate_component("a2ui.Tabs", props)
    component.children = children

    return component


def generate_accordion(
    items: list[dict[str, Any]],
    allow_multiple: bool = False
) -> A2UIComponent:
    """
    Generate an Accordion A2UI component for collapsible content sections.

    Creates an accordion with expandable/collapsible sections. Saves vertical
    space by allowing users to show/hide content sections as needed.

    Args:
        items: List of accordion item dictionaries with "title" and "content" (list of component IDs)
        allow_multiple: Whether multiple sections can be open simultaneously (default: False)

    Returns:
        A2UIComponent configured as Accordion

    Raises:
        ValueError: If items is empty
        ValueError: If any item missing "title" or "content" fields
        ValueError: If more than 10 accordion items specified

    Examples:
        >>> # Basic accordion (only one section open at a time)
        >>> accordion = generate_accordion(
        ...     items=[
        ...         {"title": "Getting Started", "content": ["step-1", "step-2", "step-3"]},
        ...         {"title": "Advanced Features", "content": ["feature-1", "feature-2"]},
        ...         {"title": "Troubleshooting", "content": ["faq-1", "faq-2"]}
        ...     ]
        ... )

        >>> # Accordion allowing multiple open sections
        >>> accordion = generate_accordion(
        ...     items=[
        ...         {"title": "API Reference", "content": ["api-doc-1"]},
        ...         {"title": "Code Examples", "content": ["code-1", "code-2"]},
        ...         {"title": "Best Practices", "content": ["tip-1", "tip-2", "tip-3"]}
        ...     ],
        ...     allow_multiple=True
        ... )
    """
    # Validate items
    if not items:
        raise ValueError("Accordion requires at least 1 item")

    if not isinstance(items, list):
        raise ValueError(f"Accordion items must be a list, got {type(items).__name__}")

    if len(items) > 10:
        raise ValueError(f"Accordion supports up to 10 items, got {len(items)}")

    # Validate each item
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"Accordion item {i} must be a dictionary")

        if "title" not in item:
            raise ValueError(f"Accordion item {i} must have 'title' field")

        if "content" not in item:
            raise ValueError(f"Accordion item {i} must have 'content' field")

        if not isinstance(item["content"], list):
            raise ValueError(
                f"Accordion item {i} content must be a list, got {type(item['content']).__name__}"
            )

    props = {
        "items": [{"title": item["title"]} for item in items],
        "allowMultiple": allow_multiple,
    }

    # Build children structure as dict mapping item indices to content
    children = {str(i): item["content"] for i, item in enumerate(items)}

    component = generate_component("a2ui.Accordion", props)
    component.children = children

    return component


def generate_carousel(
    items: list[str],
    visible_count: int = 1,
    auto_advance: bool = False
) -> A2UIComponent:
    """
    Generate a Carousel A2UI component for scrollable content display.

    Creates a horizontal carousel/slider for browsing through multiple items.
    Supports auto-advance and configurable number of visible items.

    Args:
        items: List of child component IDs to display in carousel
        visible_count: Number of items visible at once (1-4, default: 1)
        auto_advance: Whether carousel auto-advances (default: False)

    Returns:
        A2UIComponent configured as Carousel

    Raises:
        ValueError: If items is empty
        ValueError: If visible_count is not between 1 and 4
        ValueError: If items has fewer items than visible_count

    Examples:
        >>> # Single-item carousel (slideshow)
        >>> carousel = generate_carousel(
        ...     items=["image-1", "image-2", "image-3", "image-4"],
        ...     auto_advance=True
        ... )

        >>> # Multi-item carousel showing 3 at a time
        >>> carousel = generate_carousel(
        ...     items=["card-1", "card-2", "card-3", "card-4", "card-5", "card-6"],
        ...     visible_count=3
        ... )
    """
    # Validate items
    if not items:
        raise ValueError("Carousel requires at least 1 item")

    if not isinstance(items, list):
        raise ValueError(f"Carousel items must be a list, got {type(items).__name__}")

    # Validate visible_count
    if not isinstance(visible_count, int):
        raise ValueError(
            f"Carousel visible_count must be an integer, got {type(visible_count).__name__}"
        )

    if visible_count < 1 or visible_count > 4:
        raise ValueError(f"Carousel visible_count must be between 1 and 4, got {visible_count}")

    if len(items) < visible_count:
        raise ValueError(
            f"Carousel must have at least {visible_count} items to show {visible_count} visible. "
            f"Got {len(items)} items"
        )

    props = {
        "visibleCount": visible_count,
        "autoAdvance": auto_advance,
    }

    component = generate_component("a2ui.Carousel", props)
    component.children = items

    return component


def generate_sidebar(
    sidebar_content: list[str],
    main_content: list[str],
    sidebar_width: str = "30%"
) -> A2UIComponent:
    """
    Generate a Sidebar A2UI component for fixed sidebar + main content layout.

    Creates a two-panel layout with a fixed-width sidebar and flexible main
    content area. Commonly used for navigation, filters, or supplementary info.

    Args:
        sidebar_content: List of child component IDs for sidebar panel
        main_content: List of child component IDs for main content area
        sidebar_width: Width of sidebar (percentage, pixels, or CSS value, default: "30%")

    Returns:
        A2UIComponent configured as Sidebar

    Raises:
        ValueError: If sidebar_content or main_content is empty
        ValueError: If sidebar_width is invalid format

    Examples:
        >>> # Basic sidebar layout
        >>> sidebar_layout = generate_sidebar(
        ...     sidebar_content=["nav-1", "filters-1"],
        ...     main_content=["content-1", "content-2", "content-3"]
        ... )

        >>> # Sidebar with custom width
        >>> sidebar_layout = generate_sidebar(
        ...     sidebar_content=["toc-1", "related-1"],
        ...     main_content=["article-1"],
        ...     sidebar_width="250px"
        ... )
    """
    # Validate sidebar_content
    if not sidebar_content:
        raise ValueError("Sidebar requires at least 1 sidebar content item")

    if not isinstance(sidebar_content, list):
        raise ValueError(
            f"Sidebar sidebar_content must be a list, got {type(sidebar_content).__name__}"
        )

    # Validate main_content
    if not main_content:
        raise ValueError("Sidebar requires at least 1 main content item")

    if not isinstance(main_content, list):
        raise ValueError(
            f"Sidebar main_content must be a list, got {type(main_content).__name__}"
        )

    # Validate sidebar_width format
    if not sidebar_width or not sidebar_width.strip():
        raise ValueError("Sidebar sidebar_width cannot be empty")

    props = {
        "sidebarWidth": sidebar_width,
    }

    # Build children structure as dict with "sidebar" and "main" keys
    children = {
        "sidebar": sidebar_content,
        "main": main_content
    }

    component = generate_component("a2ui.Sidebar", props)
    component.children = children

    return component


# ============================================================================
# TAG & BADGE GENERATORS
# ============================================================================


def generate_tag(
    label: str,
    type: str = "default",
    icon: str | None = None,
    removable: bool = False
) -> A2UIComponent:
    """
    Generate a Tag A2UI component for labels and categorization.

    Creates a basic tag/label component for tagging, labeling, and categorizing
    content. Supports various visual styles, optional icons, and removable/dismissible
    functionality.

    Args:
        label: Text label for the tag
        type: Visual style variant (default, primary, success, warning, error, info)
        icon: Optional icon identifier to display with the tag
        removable: Whether the tag can be removed/dismissed (default: False)

    Returns:
        A2UIComponent configured as Tag

    Raises:
        ValueError: If label is empty
        ValueError: If type is not a valid tag type

    Examples:
        >>> # Basic default tag
        >>> tag = generate_tag(label="JavaScript")

        >>> # Primary tag with icon
        >>> tag = generate_tag(
        ...     label="Featured",
        ...     type="primary",
        ...     icon="star"
        ... )

        >>> # Success tag
        >>> tag = generate_tag(
        ...     label="Completed",
        ...     type="success",
        ...     icon="check"
        ... )

        >>> # Removable tag
        >>> tag = generate_tag(
        ...     label="Filter: Python",
        ...     type="info",
        ...     removable=True
        ... )

        >>> # Warning tag with icon
        >>> tag = generate_tag(
        ...     label="Deprecated",
        ...     type="warning",
        ...     icon="alert"
        ... )
    """
    # Validate label
    if not label or not label.strip():
        raise ValueError("Tag label cannot be empty")

    # Validate type
    valid_types = ["default", "primary", "success", "warning", "error", "info"]
    if type not in valid_types:
        raise ValueError(
            f"Tag type must be one of {valid_types}, got: {type}"
        )

    props = {
        "label": label.strip(),
        "type": type,
    }

    # Add optional icon
    if icon:
        props["icon"] = icon

    # Add removable flag if true
    if removable:
        props["removable"] = True

    return generate_component("a2ui.Tag", props)


def generate_badge(
    label: str,
    count: int,
    style: str = "default",
    size: str = "medium"
) -> A2UIComponent:
    """
    Generate a Badge A2UI component with count indicator.

    Creates a badge component that displays a label with a count/number indicator.
    Commonly used for notification counts, unread items, or numerical metrics
    associated with categories or filters.

    Args:
        label: Text label for the badge
        count: Numerical count to display
        style: Visual style variant (default, primary, success, warning, error)
        size: Size variant (small, medium, large)

    Returns:
        A2UIComponent configured as Badge

    Raises:
        ValueError: If label is empty
        ValueError: If count is negative
        ValueError: If style is not a valid badge style
        ValueError: If size is not a valid size

    Examples:
        >>> # Basic badge with count
        >>> badge = generate_badge(label="Notifications", count=5)

        >>> # Primary style small badge
        >>> badge = generate_badge(
        ...     label="Unread",
        ...     count=23,
        ...     style="primary",
        ...     size="small"
        ... )

        >>> # Warning badge
        >>> badge = generate_badge(
        ...     label="Pending",
        ...     count=3,
        ...     style="warning"
        ... )

        >>> # Large success badge
        >>> badge = generate_badge(
        ...     label="Completed",
        ...     count=100,
        ...     style="success",
        ...     size="large"
        ... )

        >>> # Error badge
        >>> badge = generate_badge(
        ...     label="Failed",
        ...     count=2,
        ...     style="error"
        ... )
    """
    # Validate label
    if not label or not label.strip():
        raise ValueError("Badge label cannot be empty")

    # Validate count
    if count < 0:
        raise ValueError(
            f"Badge count must be non-negative, got: {count}"
        )

    # Validate style
    valid_styles = ["default", "primary", "success", "warning", "error"]
    if style not in valid_styles:
        raise ValueError(
            f"Badge style must be one of {valid_styles}, got: {style}"
        )

    # Validate size
    valid_sizes = ["small", "medium", "large"]
    if size not in valid_sizes:
        raise ValueError(
            f"Badge size must be one of {valid_sizes}, got: {size}"
        )

    props = {
        "label": label.strip(),
        "count": count,
        "style": style,
        "size": size,
    }

    return generate_component("a2ui.Badge", props)


def generate_category_tag(
    name: str,
    color: str | None = None,
    icon: str | None = None
) -> A2UIComponent:
    """
    Generate a CategoryTag A2UI component for categorization.

    Creates a category tag component with optional custom color and icon.
    Used for content categorization, topic classification, and filtering.
    Supports semantic color naming or hex color codes.

    Args:
        name: Category name/label
        color: Optional color (semantic name or hex code, e.g., "blue", "#3B82F6")
        icon: Optional icon identifier to display with the category

    Returns:
        A2UIComponent configured as CategoryTag

    Raises:
        ValueError: If name is empty
        ValueError: If color format is invalid (when provided)

    Examples:
        >>> # Basic category tag
        >>> tag = generate_category_tag(name="Technology")

        >>> # Category with color
        >>> tag = generate_category_tag(
        ...     name="AI & ML",
        ...     color="blue"
        ... )

        >>> # Category with icon and color
        >>> tag = generate_category_tag(
        ...     name="Science",
        ...     color="purple",
        ...     icon="flask"
        ... )

        >>> # Category with hex color
        >>> tag = generate_category_tag(
        ...     name="Business",
        ...     color="#10B981"
        ... )

        >>> # Category with icon only
        >>> tag = generate_category_tag(
        ...     name="Education",
        ...     icon="book"
        ... )
    """
    # Validate name
    if not name or not name.strip():
        raise ValueError("CategoryTag name cannot be empty")

    # Validate color format if provided
    if color:
        color = color.strip()
        # Check if it's a hex color (starts with #)
        if color.startswith("#"):
            # Validate hex format (#RGB or #RRGGBB)
            if not re.match(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$', color):
                raise ValueError(
                    f"Invalid hex color format: {color}. "
                    "Use #RGB or #RRGGBB format (e.g., #3B82F6)"
                )
        # Otherwise assume it's a semantic color name (blue, red, green, etc.)
        # No further validation needed for semantic names

    props = {
        "name": name.strip(),
    }

    # Add optional color
    if color:
        props["color"] = color

    # Add optional icon
    if icon:
        props["icon"] = icon

    return generate_component("a2ui.CategoryTag", props)


def generate_status_indicator(
    status: str,
    label: str | None = None
) -> A2UIComponent:
    """
    Generate a StatusIndicator A2UI component for status display.

    Creates a status indicator badge showing system or item status with
    appropriate visual styling. Supports standard status types with
    semantic colors and optional custom labels.

    Args:
        status: Status type (success, warning, error, info, loading)
        label: Optional custom label (defaults to capitalized status)

    Returns:
        A2UIComponent configured as StatusIndicator

    Raises:
        ValueError: If status is not a valid status type

    Examples:
        >>> # Success status
        >>> indicator = generate_status_indicator(status="success")

        >>> # Success with custom label
        >>> indicator = generate_status_indicator(
        ...     status="success",
        ...     label="Deployment Complete"
        ... )

        >>> # Warning status
        >>> indicator = generate_status_indicator(
        ...     status="warning",
        ...     label="Maintenance Mode"
        ... )

        >>> # Error status
        >>> indicator = generate_status_indicator(
        ...     status="error",
        ...     label="Connection Failed"
        ... )

        >>> # Info status
        >>> indicator = generate_status_indicator(
        ...     status="info",
        ...     label="Processing"
        ... )

        >>> # Loading status
        >>> indicator = generate_status_indicator(
        ...     status="loading",
        ...     label="Fetching data..."
        ... )
    """
    # Validate status
    valid_statuses = ["success", "warning", "error", "info", "loading"]
    if status not in valid_statuses:
        raise ValueError(
            f"StatusIndicator status must be one of {valid_statuses}, got: {status}"
        )

    props = {
        "status": status,
    }

    # Add optional label
    if label is not None:
        if not label.strip():
            raise ValueError("StatusIndicator label cannot be empty when provided")
        props["label"] = label.strip()

    return generate_component("a2ui.StatusIndicator", props)


def generate_priority_badge(
    level: str,
    label: str | None = None
) -> A2UIComponent:
    """
    Generate a PriorityBadge A2UI component for priority levels.

    Creates a priority badge showing priority levels with appropriate
    visual styling and colors. Used for task management, issue tracking,
    and content prioritization.

    Args:
        level: Priority level (low, medium, high, critical)
        label: Optional custom label (defaults to capitalized level)

    Returns:
        A2UIComponent configured as PriorityBadge

    Raises:
        ValueError: If level is not a valid priority level

    Examples:
        >>> # Low priority
        >>> badge = generate_priority_badge(level="low")

        >>> # Medium priority with custom label
        >>> badge = generate_priority_badge(
        ...     level="medium",
        ...     label="Normal Priority"
        ... )

        >>> # High priority
        >>> badge = generate_priority_badge(
        ...     level="high",
        ...     label="Urgent"
        ... )

        >>> # Critical priority
        >>> badge = generate_priority_badge(
        ...     level="critical",
        ...     label="Critical - Act Now"
        ... )

        >>> # Low priority with custom label
        >>> badge = generate_priority_badge(
        ...     level="low",
        ...     label="Nice to Have"
        ... )
    """
    # Validate level
    valid_levels = ["low", "medium", "high", "critical"]
    if level not in valid_levels:
        raise ValueError(
            f"PriorityBadge level must be one of {valid_levels}, got: {level}"
        )

    props = {
        "level": level,
    }

    # Add optional label
    if label is not None:
        if not label.strip():
            raise ValueError("PriorityBadge label cannot be empty when provided")
        props["label"] = label.strip()

    return generate_component("a2ui.PriorityBadge", props)


def orchestrate_dashboard(markdown_content: str) -> list[A2UIComponent]:
    """
    Orchestrate complete dashboard generation pipeline from markdown to components.

    This is the main entry point for transforming markdown documents into
    A2UI dashboard components. It orchestrates the full pipeline:
    1. Parse markdown structure
    2. Analyze content (classification, entities, etc.)
    3. Select optimal layout
    4. Generate appropriate components based on content
    5. Apply variety constraints
    6. Return ordered component list

    The orchestrator ensures:
    - Minimum 4 different component types in output
    - No 3+ consecutive components of same type
    - Components match the selected layout and content type
    - Proper component nesting within layout containers

    Args:
        markdown_content: Raw markdown content to transform

    Returns:
        List of A2UIComponent instances ready for rendering

    Example:
        >>> markdown = "# AI Research\\n\\n## Key Findings\\n- Finding 1\\n- Finding 2"
        >>> components = orchestrate_dashboard(markdown)
        >>> len(components) >= 4
        True
        >>> # Components can be streamed via AG-UI or rendered directly
    """
    from content_analyzer import parse_markdown, ContentAnalysis, _classify_heuristic
    from layout_selector import _get_layout_from_document_type, _apply_rule_based_selection

    # Step 1: Parse markdown to extract structure
    parsed = parse_markdown(markdown_content)

    # Step 2: Build content analysis (synchronous version without LLM)
    entities = {
        'technologies': [],
        'tools': [],
        'languages': [],
        'concepts': []
    }

    content_lower = markdown_content.lower()

    # Simple entity extraction
    tech_patterns = ['React', 'Vue', 'Python', 'JavaScript', 'TypeScript', 'Docker', 'Kubernetes', 'AWS', 'Azure']
    for tech in tech_patterns:
        if tech.lower() in content_lower:
            entities['technologies'].append(tech)

    # Classify document type using heuristics
    document_type = _classify_heuristic(markdown_content, parsed)

    # Build ContentAnalysis
    content_analysis = ContentAnalysis(
        title=parsed['title'],
        document_type=document_type,
        sections=parsed['sections'],
        links=parsed['all_links'],
        youtube_links=parsed['youtube_links'],
        github_links=parsed['github_links'],
        code_blocks=parsed['code_blocks'],
        tables=parsed['tables'],
        entities=entities
    )

    # Step 3: Select optimal layout (synchronous, no LLM)
    layout_decision = _apply_rule_based_selection(content_analysis)
    if layout_decision is None:
        layout_decision = _get_layout_from_document_type(content_analysis)

    # Step 4: Generate components
    components = []
    component_types_used = set()

    def add_component_with_variety(component: A2UIComponent):
        """Add component while enforcing variety constraints."""
        component_type = component.type

        # Check for 3+ consecutive same type
        if len(components) >= 2:
            if (components[-1].type == component_type and
                components[-2].type == component_type):
                # Insert separator to break up consecutive types
                separator = generate_callout_card(
                    type="info",
                    title="Continue Reading",
                    content="More content below"
                )
                components.append(separator)
                component_types_used.add(separator.type)

        components.append(component)
        component_types_used.add(component_type)

    # Generate title/header
    if content_analysis.title:
        title_callout = generate_callout_card(
            type="info",
            title=content_analysis.title,
            content=f"Document type: {document_type.replace('_', ' ').title()}"
        )
        components.append(title_callout)
        component_types_used.add(title_callout.type)

    # Generate TLDR for long content
    if len(markdown_content) > 500:
        lines = [line.strip() for line in markdown_content.split('\n')
                if line.strip() and not line.startswith('#')]
        summary_text = ' '.join(lines[:3]) if lines else "Summary of document content"

        # Truncate to 300 chars to meet generate_tldr validation
        truncated_summary = summary_text[:300] if len(summary_text) > 300 else summary_text

        tldr = generate_tldr(content=truncated_summary, max_length=200)
        add_component_with_variety(tldr)

    # Generate components based on document type
    if document_type in ['tutorial', 'guide', 'technical_doc']:
        # Code blocks
        for idx, code_block in enumerate(content_analysis.code_blocks[:5]):
            code_content = code_block.get('content', '')
            if code_content and code_content.strip():  # Only generate if non-empty
                code_comp = generate_code_block(
                    code=code_content,
                    language=code_block.get('language', 'text')
                )
                add_component_with_variety(code_comp)

        # Step cards
        for idx, section in enumerate(content_analysis.sections[:3]):
            step = generate_step_card(
                step_number=idx + 1,
                title=section,
                description=f"Complete {section.lower()}"
            )
            add_component_with_variety(step)

    elif document_type == 'research':
        # Tables
        if content_analysis.tables:
            for table_data in content_analysis.tables[:2]:
                table = generate_data_table(
                    headers=table_data.get('headers', []),
                    rows=table_data.get('rows', [])
                )
                add_component_with_variety(table)

        # Stat cards
        import re
        numbers = re.findall(r'\b\d+[%]?\b', markdown_content)
        if len(numbers) >= 2:
            stat1 = generate_stat_card(
                title="Key Metric",
                value=numbers[0],
                change_type="positive" if '%' in numbers[0] else "neutral"
            )
            add_component_with_variety(stat1)

            stat2 = generate_stat_card(
                title="Secondary Metric",
                value=numbers[1] if len(numbers) > 1 else numbers[0]
            )
            add_component_with_variety(stat2)

    elif document_type == 'article':
        # Video cards
        for youtube_url in content_analysis.youtube_links[:2]:
            video = generate_video_card(
                video_url=youtube_url,
                title="Video Content",
                description="Related video content"
            )
            add_component_with_variety(video)

    # Add resources from links
    if content_analysis.github_links:
        for github_url in content_analysis.github_links[:2]:
            # Extract repo name from URL
            repo_parts = github_url.rstrip('/').split('/')
            repo_name = repo_parts[-1] if len(repo_parts) > 0 else "Repository"
            owner = repo_parts[-2] if len(repo_parts) > 1 else None
            repo = generate_repo_card(
                name=repo_name,
                owner=owner,
                repo_url=github_url
            )
            add_component_with_variety(repo)

    # Add general links
    if content_analysis.links:
        other_links = [link for link in content_analysis.links
                      if 'github.com' not in link and 'youtube.com' not in link]
        for link in other_links[:2]:
            link_card = generate_link_card(
                url=link,
                title=f"Resource: {link[:30]}..."
            )
            add_component_with_variety(link_card)

    # Add table of contents
    if len(content_analysis.sections) > 3:
        toc_items = [{"title": section, "anchor": f"#{section.lower().replace(' ', '-')}"}
                    for section in content_analysis.sections[:8]]
        toc = generate_table_of_contents(items=toc_items)
        add_component_with_variety(toc)

    # Add tags for technologies
    if entities.get('technologies'):
        for tag_text in entities['technologies'][:6]:
            tag = generate_tag(label=tag_text, type="primary")
            add_component_with_variety(tag)

    # Ensure minimum 4 different component types
    while len(component_types_used) < 4:
        if 'a2ui.KeyTakeaways' not in component_types_used:
            items = content_analysis.sections[:3] if content_analysis.sections else ["Key point 1", "Key point 2"]
            takeaways = generate_key_takeaways(items=items)
            components.append(takeaways)
            component_types_used.add(takeaways.type)
        elif 'a2ui.Badge' not in component_types_used:
            badge = generate_badge(label=document_type.title(), count=1)
            components.append(badge)
            component_types_used.add(badge.type)
        elif 'a2ui.BulletPoint' not in component_types_used:
            bullet = generate_bullet_point(text="Additional detail")
            components.append(bullet)
            component_types_used.add(bullet.type)
        else:
            # Add extra callout
            callout = generate_callout_card(
                type="info",
                title="Note",
                content="Important information"
            )
            components.append(callout)
            component_types_used.add(callout.type)
            break

    # Ensure minimum 4 components
    while len(components) < 4:
        filler = generate_callout_card(
            type="info",
            title=f"Section {len(components) + 1}",
            content="Content placeholder"
        )
        components.append(filler)
        component_types_used.add(filler.type)

    return components


# Export public API
__all__ = [
    "A2UIComponent",
    "generate_id",
    "reset_id_counter",
    "generate_component",
    "emit_components",
    "validate_component_props",
    "generate_components_batch",
    "VALID_COMPONENT_TYPES",
    # News generators
    "generate_headline_card",
    "generate_trend_indicator",
    "generate_timeline_event",
    "generate_news_ticker",
    # Media generators
    "extract_youtube_id",
    "generate_video_card",
    "generate_image_card",
    "generate_playlist_card",
    "generate_podcast_card",
    # Data generators
    "generate_stat_card",
    "generate_metric_row",
    "generate_progress_ring",
    "generate_comparison_bar",
    "generate_data_table",
    "generate_mini_chart",
    # List generators
    "generate_ranked_item",
    "generate_checklist_item",
    "generate_pro_con_item",
    "generate_bullet_point",
    # Resource generators
    "extract_domain",
    "extract_github_repo_info",
    "generate_link_card",
    "generate_tool_card",
    "generate_book_card",
    "generate_repo_card",
    # People generators
    "generate_profile_card",
    "generate_company_card",
    "generate_quote_card",
    "generate_expert_tip",
    # Summary generators
    "generate_tldr",
    "generate_key_takeaways",
    "generate_executive_summary",
    "generate_table_of_contents",
    # Instructional generators
    "detect_language",
    "generate_step_card",
    "generate_code_block",
    "generate_callout_card",
    "generate_command_card",
    # Comparison generators
    "generate_comparison_table",
    "generate_vs_card",
    "generate_feature_matrix",
    "generate_pricing_table",
    # Layout generators
    "generate_section",
    "generate_grid",
    "generate_columns",
    "generate_tabs",
    "generate_accordion",
    "generate_carousel",
    "generate_sidebar",
    # Tag generators
    "generate_tag",
    "generate_badge",
    "generate_category_tag",
    "generate_status_indicator",
    "generate_priority_badge",
    # Orchestrator
    "orchestrate_dashboard",
]
