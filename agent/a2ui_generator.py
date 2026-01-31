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
    children: list[str] | dict[str, list[str]] | None = None
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

    Returns:
        A2UIComponent instance ready for emission

    Raises:
        ValueError: If component_type is not valid
        ValidationError: If props don't meet component requirements

    Examples:
        >>> component = generate_component(
        ...     "a2ui.StatCard",
        ...     {"value": "$196B", "label": "Market Size", "trend": "up"}
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
        children=children
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
]
