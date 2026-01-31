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
]
