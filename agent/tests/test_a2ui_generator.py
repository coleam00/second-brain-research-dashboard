"""
Tests for A2UI Generator Module.

Comprehensive test suite for a2ui_generator.py covering:
- A2UIComponent model validation
- ID generation and uniqueness
- Component generation functions
- Component emission to AG-UI format
- Error handling for invalid types
- Batch component generation
"""

import pytest
import json
from pydantic import ValidationError
from a2ui_generator import (
    A2UIComponent,
    generate_id,
    reset_id_counter,
    generate_component,
    emit_components,
    validate_component_props,
    generate_components_batch,
    VALID_COMPONENT_TYPES,
    # News generators
    generate_headline_card,
    generate_trend_indicator,
    generate_timeline_event,
    generate_news_ticker,
    # Media generators
    extract_youtube_id,
    generate_video_card,
    generate_image_card,
    generate_playlist_card,
    generate_podcast_card,
    # Data generators
    generate_stat_card,
    generate_metric_row,
    generate_progress_ring,
    generate_comparison_bar,
    generate_data_table,
    generate_mini_chart,
)


class TestA2UIComponentModel:
    """Test suite for A2UIComponent Pydantic model."""

    def test_valid_component_creation(self):
        """Test creating a valid A2UI component."""
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

        assert component.type == "a2ui.StatCard"
        assert component.id == "stat-1"
        assert component.props["value"] == "$196B"
        assert component.props["label"] == "AI Market Size"
        assert component.children is None

    def test_component_with_children(self):
        """Test creating a component with children (layout component)."""
        component = A2UIComponent(
            type="a2ui.Section",
            id="section-1",
            props={"title": "Overview"},
            children=["stat-1", "stat-2", "video-1"]
        )

        assert component.type == "a2ui.Section"
        assert component.children == ["stat-1", "stat-2", "video-1"]

    def test_component_with_nested_children(self):
        """Test creating a component with nested children structure (Tabs/Accordion)."""
        component = A2UIComponent(
            type="a2ui.Tabs",
            id="tabs-1",
            props={
                "tabs": [
                    {"id": "overview", "label": "Overview"},
                    {"id": "details", "label": "Details"}
                ]
            },
            children={
                "overview": ["summary-1"],
                "details": ["table-1", "chart-1"]
            }
        )

        assert component.type == "a2ui.Tabs"
        assert isinstance(component.children, dict)
        assert component.children["overview"] == ["summary-1"]
        assert component.children["details"] == ["table-1", "chart-1"]

    def test_invalid_component_type_format(self):
        """Test that component type must start with 'a2ui.'"""
        with pytest.raises(ValidationError) as exc_info:
            A2UIComponent(
                type="StatCard",  # Missing "a2ui." prefix
                id="stat-1",
                props={"value": "100"}
            )

        # Check that validation error occurred for the type field
        assert "type" in str(exc_info.value)
        assert "pattern" in str(exc_info.value).lower()

    def test_invalid_component_type_pattern(self):
        """Test that component type must follow PascalCase after 'a2ui.'"""
        with pytest.raises(ValidationError):
            A2UIComponent(
                type="a2ui.stat_card",  # Should be PascalCase
                id="stat-1",
                props={"value": "100"}
            )

    def test_empty_id_validation(self):
        """Test that component ID cannot be empty."""
        with pytest.raises(ValidationError) as exc_info:
            A2UIComponent(
                type="a2ui.StatCard",
                id="",
                props={"value": "100"}
            )

        assert "cannot be empty" in str(exc_info.value)

    def test_component_serialization(self):
        """Test that component can be serialized to dict/JSON."""
        component = A2UIComponent(
            type="a2ui.VideoCard",
            id="video-1",
            props={
                "videoId": "dQw4w9WgXcQ",
                "platform": "youtube",
                "title": "Demo Video"
            }
        )

        # Serialize to dict
        component_dict = component.model_dump()
        assert component_dict["type"] == "a2ui.VideoCard"
        assert component_dict["id"] == "video-1"
        assert component_dict["props"]["videoId"] == "dQw4w9WgXcQ"

        # Serialize to JSON
        json_str = component.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["type"] == "a2ui.VideoCard"

    def test_component_exclude_none(self):
        """Test that None values can be excluded from serialization."""
        component = A2UIComponent(
            type="a2ui.StatCard",
            id="stat-1",
            props={"value": "100"}
        )

        # Exclude None values (children should not be in output)
        component_dict = component.model_dump(exclude_none=True)
        assert "children" not in component_dict


class TestGenerateID:
    """Test suite for generate_id() function."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_generate_id_with_prefix(self):
        """Test ID generation with custom prefix."""
        id1 = generate_id("a2ui.StatCard", prefix="stat")
        id2 = generate_id("a2ui.StatCard", prefix="stat")
        id3 = generate_id("a2ui.VideoCard", prefix="video")

        assert id1 == "stat-1"
        assert id2 == "stat-2"
        assert id3 == "video-3"

    def test_generate_id_without_prefix(self):
        """Test ID generation without prefix (extracts from component type)."""
        id1 = generate_id("a2ui.StatCard")
        id2 = generate_id("a2ui.VideoCard")
        id3 = generate_id("a2ui.HeadlineCard")

        assert id1 == "stat-card-1"
        assert id2 == "video-card-2"
        assert id3 == "headline-card-3"

    def test_generate_id_pascal_to_kebab(self):
        """Test PascalCase to kebab-case conversion."""
        reset_id_counter()

        id1 = generate_id("a2ui.TLDR")
        id2 = generate_id("a2ui.ExecutiveSummary")
        id3 = generate_id("a2ui.TableOfContents")

        assert id1 == "t-l-d-r-1"
        assert id2 == "executive-summary-2"
        assert id3 == "table-of-contents-3"

    def test_id_uniqueness(self):
        """Test that generated IDs are unique."""
        ids = set()
        for i in range(100):
            new_id = generate_id("a2ui.StatCard", prefix="stat")
            assert new_id not in ids
            ids.add(new_id)

        assert len(ids) == 100

    def test_reset_id_counter(self):
        """Test that reset_id_counter() resets the counter."""
        id1 = generate_id("a2ui.StatCard", prefix="stat")
        assert id1 == "stat-1"

        id2 = generate_id("a2ui.StatCard", prefix="stat")
        assert id2 == "stat-2"

        reset_id_counter()

        id3 = generate_id("a2ui.StatCard", prefix="stat")
        assert id3 == "stat-1"  # Counter reset


class TestGenerateComponent:
    """Test suite for generate_component() function."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_generate_valid_component(self):
        """Test generating a valid component."""
        component = generate_component(
            "a2ui.StatCard",
            props={"value": "$196B", "label": "Market Size", "trend": "up"}
        )

        assert isinstance(component, A2UIComponent)
        assert component.type == "a2ui.StatCard"
        assert component.id == "stat-card-1"
        assert component.props["value"] == "$196B"

    def test_generate_component_with_custom_id(self):
        """Test generating component with custom ID."""
        component = generate_component(
            "a2ui.VideoCard",
            props={"videoId": "abc123", "platform": "youtube"},
            component_id="custom-video-1"
        )

        assert component.id == "custom-video-1"

    def test_generate_component_with_children(self):
        """Test generating layout component with children."""
        component = generate_component(
            "a2ui.Section",
            props={"title": "Overview"},
            children=["stat-1", "stat-2"]
        )

        assert component.children == ["stat-1", "stat-2"]

    def test_generate_component_invalid_type(self):
        """Test that invalid component type raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            generate_component(
                "a2ui.InvalidComponent",
                props={"value": "test"}
            )

        assert "Invalid component type" in str(exc_info.value)
        assert "a2ui.InvalidComponent" in str(exc_info.value)

    def test_generate_component_auto_id_generation(self):
        """Test that components get sequential auto-generated IDs."""
        c1 = generate_component("a2ui.StatCard", props={"value": "1"})
        c2 = generate_component("a2ui.StatCard", props={"value": "2"})
        c3 = generate_component("a2ui.VideoCard", props={"videoId": "123", "platform": "youtube"})

        assert c1.id == "stat-card-1"
        assert c2.id == "stat-card-2"
        assert c3.id == "video-card-3"


class TestEmitComponents:
    """Test suite for emit_components() async function."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    @pytest.mark.asyncio
    async def test_emit_components_ag_ui_format(self):
        """Test emitting components in AG-UI SSE format."""
        components = [
            generate_component("a2ui.StatCard", props={"value": "100", "label": "Users"}),
            generate_component("a2ui.StatCard", props={"value": "50", "label": "Active"}),
        ]

        events = []
        async for event in emit_components(components, stream_format="ag-ui"):
            events.append(event)

        assert len(events) == 2
        assert events[0].startswith("data: ")
        assert events[0].endswith("\n\n")

        # Parse the JSON from the event
        json_str = events[0].replace("data: ", "").strip()
        data = json.loads(json_str)
        assert data["type"] == "a2ui.StatCard"
        assert data["id"] == "stat-card-1"
        assert data["props"]["value"] == "100"

    @pytest.mark.asyncio
    async def test_emit_components_json_format(self):
        """Test emitting components in plain JSON format."""
        components = [
            generate_component("a2ui.VideoCard", props={"videoId": "abc123", "platform": "youtube"}),
        ]

        events = []
        async for event in emit_components(components, stream_format="json"):
            events.append(event)

        assert len(events) == 1
        assert not event.startswith("data: ")  # No SSE formatting

        data = json.loads(events[0])
        assert data["type"] == "a2ui.VideoCard"
        assert data["props"]["videoId"] == "abc123"

    @pytest.mark.asyncio
    async def test_emit_components_invalid_format(self):
        """Test that invalid stream format raises ValueError."""
        components = [
            generate_component("a2ui.StatCard", props={"value": "100", "label": "Test"}),
        ]

        with pytest.raises(ValueError) as exc_info:
            async for event in emit_components(components, stream_format="invalid"):
                pass

        assert "Unknown stream format" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_emit_empty_components_list(self):
        """Test emitting empty list of components."""
        events = []
        async for event in emit_components([]):
            events.append(event)

        assert len(events) == 0

    @pytest.mark.asyncio
    async def test_emit_components_exclude_none(self):
        """Test that None values are excluded from emitted JSON."""
        component = generate_component(
            "a2ui.StatCard",
            props={"value": "100", "label": "Test"}
        )

        events = []
        async for event in emit_components([component]):
            events.append(event)

        json_str = events[0].replace("data: ", "").strip()
        data = json.loads(json_str)

        # children field should not be present (it's None)
        assert "children" not in data


class TestValidateComponentProps:
    """Test suite for validate_component_props() function."""

    def test_validate_stat_card_props(self):
        """Test validation of StatCard required props."""
        # Valid props
        assert validate_component_props(
            "a2ui.StatCard",
            {"value": "100", "label": "Users", "trend": "up"}
        ) is True

        # Missing required prop
        with pytest.raises(ValueError) as exc_info:
            validate_component_props("a2ui.StatCard", {"value": "100"})

        assert "missing required props" in str(exc_info.value)
        assert "label" in str(exc_info.value)

    def test_validate_video_card_props(self):
        """Test validation of VideoCard required props."""
        # Valid props
        assert validate_component_props(
            "a2ui.VideoCard",
            {"videoId": "abc123", "platform": "youtube", "title": "Demo"}
        ) is True

        # Missing required props
        with pytest.raises(ValueError) as exc_info:
            validate_component_props("a2ui.VideoCard", {"title": "Demo"})

        assert "videoId" in str(exc_info.value) or "platform" in str(exc_info.value)

    def test_validate_unknown_component_type(self):
        """Test validation of component type without required props defined."""
        # Should pass - no validation rules for this type
        assert validate_component_props(
            "a2ui.CustomComponent",
            {"any": "props"}
        ) is True


class TestGenerateComponentsBatch:
    """Test suite for generate_components_batch() function."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_batch_generation(self):
        """Test generating multiple components in batch."""
        specs = [
            ("a2ui.StatCard", {"value": "100", "label": "Users"}),
            ("a2ui.StatCard", {"value": "50", "label": "Active"}),
            ("a2ui.VideoCard", {"videoId": "abc123", "platform": "youtube"}),
        ]

        components = generate_components_batch(specs)

        assert len(components) == 3
        assert components[0].type == "a2ui.StatCard"
        assert components[0].id == "stat-card-1"
        assert components[1].type == "a2ui.StatCard"
        assert components[1].id == "stat-card-2"
        assert components[2].type == "a2ui.VideoCard"
        assert components[2].id == "video-card-3"

    def test_batch_generation_empty_list(self):
        """Test batch generation with empty list."""
        components = generate_components_batch([])
        assert len(components) == 0

    def test_batch_generation_invalid_type(self):
        """Test that batch generation raises error for invalid type."""
        specs = [
            ("a2ui.StatCard", {"value": "100", "label": "Users"}),
            ("a2ui.InvalidType", {"value": "test"}),
        ]

        with pytest.raises(ValueError):
            generate_components_batch(specs)


class TestComponentTypeRegistry:
    """Test suite for VALID_COMPONENT_TYPES registry."""

    def test_all_categories_present(self):
        """Test that all component categories are registered."""
        # Check for presence of components from each category
        categories = {
            "news": "a2ui.HeadlineCard",
            "media": "a2ui.VideoCard",
            "data": "a2ui.StatCard",
            "lists": "a2ui.RankedItem",
            "resources": "a2ui.LinkCard",
            "people": "a2ui.ProfileCard",
            "summary": "a2ui.TLDR",
            "comparison": "a2ui.ComparisonTable",
            "instructional": "a2ui.CodeBlock",
            "layout": "a2ui.Section",
            "tags": "a2ui.TagCloud",
        }

        for category, component_type in categories.items():
            assert component_type in VALID_COMPONENT_TYPES, f"Missing {category} component: {component_type}"

    def test_component_count(self):
        """Test that we have all expected component types."""
        # Based on app_spec.txt, we should have 40+ components
        assert len(VALID_COMPONENT_TYPES) >= 40


class TestIntegration:
    """Integration tests for complete component generation workflow."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    @pytest.mark.asyncio
    async def test_full_workflow(self):
        """Test complete workflow from generation to emission."""
        # Step 1: Generate components
        components = [
            generate_component("a2ui.TLDR", props={
                "summary": "This is a test document",
                "bulletPoints": ["Point 1", "Point 2"]
            }),
            generate_component("a2ui.StatCard", props={
                "value": "$196B",
                "label": "Market Size",
                "trend": "up"
            }),
            generate_component("a2ui.VideoCard", props={
                "videoId": "dQw4w9WgXcQ",
                "platform": "youtube",
                "title": "Demo Video"
            }),
        ]

        # Step 2: Validate components
        assert len(components) == 3
        assert all(isinstance(c, A2UIComponent) for c in components)

        # Step 3: Emit components
        events = []
        async for event in emit_components(components):
            events.append(event)

        # Step 4: Verify emission
        assert len(events) == 3

        # Parse first event
        json_str = events[0].replace("data: ", "").strip()
        data = json.loads(json_str)
        assert data["type"] == "a2ui.TLDR"
        assert "bulletPoints" in data["props"]

    def test_component_id_uniqueness_across_types(self):
        """Test that IDs remain unique across different component types."""
        components = []
        for _ in range(10):
            components.append(generate_component("a2ui.StatCard", props={"value": "1", "label": "Test"}))
            components.append(generate_component("a2ui.VideoCard", props={"videoId": "123", "platform": "youtube"}))
            components.append(generate_component("a2ui.Section", props={"title": "Test"}))

        ids = [c.id for c in components]
        assert len(ids) == len(set(ids))  # All IDs are unique


class TestNewsGenerators:
    """Test suite for news component generators."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_generate_headline_card_basic(self):
        """Test generating HeadlineCard with required fields."""
        card = generate_headline_card(
            title="AI Breakthrough Announced",
            summary="Major advancement in natural language processing",
            source="Tech Daily",
            published_at="2026-01-30T10:00:00Z"
        )

        assert isinstance(card, A2UIComponent)
        assert card.type == "a2ui.HeadlineCard"
        assert card.props["title"] == "AI Breakthrough Announced"
        assert card.props["summary"] == "Major advancement in natural language processing"
        assert card.props["source"] == "Tech Daily"
        assert card.props["publishedAt"] == "2026-01-30T10:00:00Z"
        assert card.props["sentiment"] == "neutral"  # Default value
        assert "imageUrl" not in card.props  # Optional field not included

    def test_generate_headline_card_with_sentiment(self):
        """Test HeadlineCard with different sentiment values."""
        positive_card = generate_headline_card(
            title="Market Soars",
            summary="Record highs reached",
            source="Financial Times",
            published_at="2026-01-30T10:00:00Z",
            sentiment="positive"
        )
        assert positive_card.props["sentiment"] == "positive"

        negative_card = generate_headline_card(
            title="Crisis Deepens",
            summary="Concerns mount",
            source="News Corp",
            published_at="2026-01-30T10:00:00Z",
            sentiment="negative"
        )
        assert negative_card.props["sentiment"] == "negative"

    def test_generate_headline_card_with_image(self):
        """Test HeadlineCard with optional image URL."""
        card = generate_headline_card(
            title="Test Article",
            summary="Test summary",
            source="Test Source",
            published_at="2026-01-30T10:00:00Z",
            image_url="https://example.com/image.jpg"
        )

        assert card.props["imageUrl"] == "https://example.com/image.jpg"

    def test_generate_headline_card_json_serialization(self):
        """Test HeadlineCard serializes to valid JSON."""
        card = generate_headline_card(
            title="Test",
            summary="Summary",
            source="Source",
            published_at="2026-01-30T10:00:00Z"
        )

        card_dict = card.model_dump(exclude_none=True)
        json_str = json.dumps(card_dict)
        parsed = json.loads(json_str)

        assert parsed["type"] == "a2ui.HeadlineCard"
        assert parsed["props"]["title"] == "Test"

    def test_generate_trend_indicator_basic(self):
        """Test generating TrendIndicator with required fields."""
        indicator = generate_trend_indicator(
            label="Market Cap",
            value=2.5,
            trend="up",
            change=12.3
        )

        assert isinstance(indicator, A2UIComponent)
        assert indicator.type == "a2ui.TrendIndicator"
        assert indicator.props["label"] == "Market Cap"
        assert indicator.props["value"] == 2.5
        assert indicator.props["trend"] == "up"
        assert indicator.props["change"] == 12.3
        assert "unit" not in indicator.props  # Optional field not included

    def test_generate_trend_indicator_all_trends(self):
        """Test TrendIndicator with all valid trend values."""
        up_trend = generate_trend_indicator(
            label="Growth", value=100, trend="up", change=5.5
        )
        assert up_trend.props["trend"] == "up"

        down_trend = generate_trend_indicator(
            label="Decline", value=90, trend="down", change=-5.5
        )
        assert down_trend.props["trend"] == "down"

        stable_trend = generate_trend_indicator(
            label="Stable", value=100, trend="stable", change=0.1
        )
        assert stable_trend.props["trend"] == "stable"

    def test_generate_trend_indicator_with_unit(self):
        """Test TrendIndicator with various units."""
        percent_trend = generate_trend_indicator(
            label="Growth Rate", value=5.5, trend="up", change=2.3, unit="%"
        )
        assert percent_trend.props["unit"] == "%"

        points_trend = generate_trend_indicator(
            label="Score", value=85, trend="up", change=10, unit="points"
        )
        assert points_trend.props["unit"] == "points"

        currency_trend = generate_trend_indicator(
            label="Price", value=100.50, trend="down", change=-5.25, unit="USD"
        )
        assert currency_trend.props["unit"] == "USD"

    def test_generate_trend_indicator_invalid_trend(self):
        """Test TrendIndicator raises error for invalid trend."""
        with pytest.raises(ValueError) as exc_info:
            generate_trend_indicator(
                label="Test", value=100, trend="sideways", change=0
            )

        error_msg = str(exc_info.value).lower()
        assert "invalid trend value" in error_msg
        assert "sideways" in error_msg
        assert "up" in error_msg and "down" in error_msg and "stable" in error_msg

    def test_generate_timeline_event_basic(self):
        """Test generating TimelineEvent with required fields."""
        event = generate_timeline_event(
            title="Product Launch",
            timestamp="2026-01-15T09:00:00Z",
            content="New AI model released to public"
        )

        assert isinstance(event, A2UIComponent)
        assert event.type == "a2ui.TimelineEvent"
        assert event.props["title"] == "Product Launch"
        assert event.props["timestamp"] == "2026-01-15T09:00:00Z"
        assert event.props["content"] == "New AI model released to public"
        assert event.props["eventType"] == "article"  # Default value
        assert "icon" not in event.props  # Optional field not included

    def test_generate_timeline_event_all_types(self):
        """Test TimelineEvent with all valid event types."""
        article_event = generate_timeline_event(
            title="Article", timestamp="2026-01-30T10:00:00Z",
            content="Content", event_type="article"
        )
        assert article_event.props["eventType"] == "article"

        announcement_event = generate_timeline_event(
            title="Announcement", timestamp="2026-01-30T10:00:00Z",
            content="Content", event_type="announcement"
        )
        assert announcement_event.props["eventType"] == "announcement"

        milestone_event = generate_timeline_event(
            title="Milestone", timestamp="2026-01-30T10:00:00Z",
            content="Content", event_type="milestone"
        )
        assert milestone_event.props["eventType"] == "milestone"

        update_event = generate_timeline_event(
            title="Update", timestamp="2026-01-30T10:00:00Z",
            content="Content", event_type="update"
        )
        assert update_event.props["eventType"] == "update"

    def test_generate_timeline_event_with_icon(self):
        """Test TimelineEvent with optional icon."""
        event = generate_timeline_event(
            title="Launch",
            timestamp="2026-01-30T10:00:00Z",
            content="Product launched",
            icon="rocket"
        )

        assert event.props["icon"] == "rocket"

    def test_generate_timeline_event_invalid_type(self):
        """Test TimelineEvent raises error for invalid event type."""
        with pytest.raises(ValueError) as exc_info:
            generate_timeline_event(
                title="Test",
                timestamp="2026-01-30T10:00:00Z",
                content="Content",
                event_type="invalid_type"
            )

        assert "Invalid event_type" in str(exc_info.value)
        assert "invalid_type" in str(exc_info.value)

    def test_generate_news_ticker_basic(self):
        """Test generating NewsTicker with multiple items."""
        items = [
            {
                "text": "Markets up 2% on strong earnings",
                "url": "https://example.com/market-news",
                "timestamp": "2026-01-30T10:00:00Z"
            },
            {
                "text": "New AI regulation proposed",
                "url": "https://example.com/ai-regulation",
                "timestamp": "2026-01-30T09:30:00Z"
            }
        ]

        ticker = generate_news_ticker(items)

        assert isinstance(ticker, A2UIComponent)
        assert ticker.type == "a2ui.NewsTicker"
        assert len(ticker.props["items"]) == 2
        assert ticker.props["items"][0]["text"] == "Markets up 2% on strong earnings"
        assert ticker.props["items"][1]["url"] == "https://example.com/ai-regulation"

    def test_generate_news_ticker_single_item(self):
        """Test NewsTicker with single item."""
        items = [
            {
                "text": "Breaking news",
                "url": "https://example.com/breaking",
                "timestamp": "2026-01-30T10:00:00Z"
            }
        ]

        ticker = generate_news_ticker(items)
        assert len(ticker.props["items"]) == 1

    def test_generate_news_ticker_max_items(self):
        """Test NewsTicker with maximum 10 items."""
        items = [
            {
                "text": f"News item {i}",
                "url": f"https://example.com/news-{i}",
                "timestamp": "2026-01-30T10:00:00Z"
            }
            for i in range(10)
        ]

        ticker = generate_news_ticker(items)
        assert len(ticker.props["items"]) == 10

    def test_generate_news_ticker_too_many_items(self):
        """Test NewsTicker raises error for more than 10 items."""
        items = [
            {
                "text": f"News item {i}",
                "url": f"https://example.com/news-{i}",
                "timestamp": "2026-01-30T10:00:00Z"
            }
            for i in range(11)
        ]

        with pytest.raises(ValueError) as exc_info:
            generate_news_ticker(items)

        assert "supports up to 10 items" in str(exc_info.value)
        assert "11" in str(exc_info.value)

    def test_generate_news_ticker_empty_list(self):
        """Test NewsTicker raises error for empty items list."""
        with pytest.raises(ValueError) as exc_info:
            generate_news_ticker([])

        assert "requires at least one item" in str(exc_info.value)

    def test_generate_news_ticker_missing_required_keys(self):
        """Test NewsTicker raises error when items missing required keys."""
        # Missing 'url' key
        items = [
            {
                "text": "News item",
                "timestamp": "2026-01-30T10:00:00Z"
            }
        ]

        with pytest.raises(ValueError) as exc_info:
            generate_news_ticker(items)

        assert "missing required keys" in str(exc_info.value)
        assert "url" in str(exc_info.value)

        # Missing 'timestamp' key
        items = [
            {
                "text": "News item",
                "url": "https://example.com/news"
            }
        ]

        with pytest.raises(ValueError) as exc_info:
            generate_news_ticker(items)

        assert "missing required keys" in str(exc_info.value)
        assert "timestamp" in str(exc_info.value)


class TestNewsGeneratorsIntegration:
    """Integration tests for news component generators."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_news_workflow_headline_to_timeline(self):
        """Test creating a news workflow with headline and timeline."""
        # Create headline card
        headline = generate_headline_card(
            title="Major AI Announcement",
            summary="Company unveils new language model",
            source="TechCrunch",
            published_at="2026-01-30T10:00:00Z",
            sentiment="positive"
        )

        # Create timeline events for the story
        events = [
            generate_timeline_event(
                title="Initial Announcement",
                timestamp="2026-01-30T10:00:00Z",
                content="CEO announces new model",
                event_type="announcement"
            ),
            generate_timeline_event(
                title="Technical Details Released",
                timestamp="2026-01-30T11:00:00Z",
                content="Research paper published",
                event_type="article"
            ),
            generate_timeline_event(
                title="Public Beta Launch",
                timestamp="2026-01-30T14:00:00Z",
                content="Beta access opened to users",
                event_type="milestone"
            )
        ]

        # Verify all components generated correctly
        assert headline.type == "a2ui.HeadlineCard"
        assert all(e.type == "a2ui.TimelineEvent" for e in events)
        assert len(events) == 3

        # Verify IDs are unique
        all_ids = [headline.id] + [e.id for e in events]
        assert len(all_ids) == len(set(all_ids))

    def test_news_workflow_with_trends_and_ticker(self):
        """Test complete news dashboard with trends and ticker."""
        # Create trend indicators
        trends = [
            generate_trend_indicator(
                label="Stock Price", value=150.25, trend="up", change=5.2, unit="%"
            ),
            generate_trend_indicator(
                label="Market Cap", value=2.5, trend="up", change=0.3, unit="T USD"
            ),
            generate_trend_indicator(
                label="Trading Volume", value=85, trend="down", change=-12.5, unit="%"
            )
        ]

        # Create news ticker
        ticker = generate_news_ticker([
            {
                "text": "Breaking: New product launched",
                "url": "https://example.com/product",
                "timestamp": "2026-01-30T10:00:00Z"
            },
            {
                "text": "Markets react positively",
                "url": "https://example.com/markets",
                "timestamp": "2026-01-30T10:15:00Z"
            }
        ])

        # Verify components
        assert all(t.type == "a2ui.TrendIndicator" for t in trends)
        assert ticker.type == "a2ui.NewsTicker"
        assert len(ticker.props["items"]) == 2

        # Verify all IDs unique
        all_components = trends + [ticker]
        all_ids = [c.id for c in all_components]
        assert len(all_ids) == len(set(all_ids))

    @pytest.mark.asyncio
    async def test_news_components_emission(self):
        """Test emitting news components in AG-UI format."""
        components = [
            generate_headline_card(
                title="Test Article",
                summary="Test summary",
                source="Test Source",
                published_at="2026-01-30T10:00:00Z"
            ),
            generate_trend_indicator(
                label="Test Metric", value=100, trend="up", change=10
            ),
            generate_timeline_event(
                title="Test Event",
                timestamp="2026-01-30T10:00:00Z",
                content="Test content"
            )
        ]

        events = []
        async for event in emit_components(components):
            events.append(event)

        assert len(events) == 3

        # Parse and verify first event (HeadlineCard)
        json_str = events[0].replace("data: ", "").strip()
        data = json.loads(json_str)
        assert data["type"] == "a2ui.HeadlineCard"
        assert data["props"]["title"] == "Test Article"

        # Parse and verify second event (TrendIndicator)
        json_str = events[1].replace("data: ", "").strip()
        data = json.loads(json_str)
        assert data["type"] == "a2ui.TrendIndicator"
        assert data["props"]["trend"] == "up"

        # Parse and verify third event (TimelineEvent)
        json_str = events[2].replace("data: ", "").strip()
        data = json.loads(json_str)
        assert data["type"] == "a2ui.TimelineEvent"
        assert data["props"]["eventType"] == "article"


class TestExtractYoutubeId:
    """Test suite for extract_youtube_id() utility function."""

    def test_extract_from_watch_url(self):
        """Test extracting video ID from youtube.com/watch?v= URL."""
        video_id = extract_youtube_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert video_id == "dQw4w9WgXcQ"

    def test_extract_from_short_url(self):
        """Test extracting video ID from youtu.be short URL."""
        video_id = extract_youtube_id("https://youtu.be/dQw4w9WgXcQ")
        assert video_id == "dQw4w9WgXcQ"

    def test_extract_from_embed_url(self):
        """Test extracting video ID from youtube.com/embed/ URL."""
        video_id = extract_youtube_id("https://www.youtube.com/embed/dQw4w9WgXcQ")
        assert video_id == "dQw4w9WgXcQ"

    def test_extract_from_v_url(self):
        """Test extracting video ID from youtube.com/v/ URL."""
        video_id = extract_youtube_id("https://www.youtube.com/v/dQw4w9WgXcQ")
        assert video_id == "dQw4w9WgXcQ"

    def test_extract_without_www(self):
        """Test extracting from URL without www."""
        video_id = extract_youtube_id("https://youtube.com/watch?v=dQw4w9WgXcQ")
        assert video_id == "dQw4w9WgXcQ"

    def test_extract_with_http(self):
        """Test extracting from http (not https) URL."""
        video_id = extract_youtube_id("http://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert video_id == "dQw4w9WgXcQ"

    def test_extract_with_additional_params(self):
        """Test extracting from URL with additional query parameters."""
        video_id = extract_youtube_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=30s&list=PLtest")
        assert video_id == "dQw4w9WgXcQ"

    def test_extract_from_invalid_url(self):
        """Test that invalid URLs return None."""
        assert extract_youtube_id("https://example.com/video") is None
        assert extract_youtube_id("not a url") is None
        assert extract_youtube_id("https://vimeo.com/123456") is None

    def test_extract_from_empty_string(self):
        """Test that empty string returns None."""
        assert extract_youtube_id("") is None

    def test_extract_from_none(self):
        """Test that None returns None."""
        assert extract_youtube_id(None) is None


class TestMediaGenerators:
    """Test suite for media component generators."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    # VideoCard Tests

    def test_generate_video_card_with_video_id(self):
        """Test generating VideoCard with direct video_id."""
        card = generate_video_card(
            title="Introduction to AI",
            description="Learn the basics of artificial intelligence",
            video_id="dQw4w9WgXcQ",
            duration="10:30"
        )

        assert isinstance(card, A2UIComponent)
        assert card.type == "a2ui.VideoCard"
        assert card.props["title"] == "Introduction to AI"
        assert card.props["description"] == "Learn the basics of artificial intelligence"
        assert card.props["videoId"] == "dQw4w9WgXcQ"
        assert card.props["platform"] == "youtube"
        assert card.props["duration"] == "10:30"
        assert "thumbnailUrl" not in card.props  # Optional field not included

    def test_generate_video_card_with_youtube_url(self):
        """Test generating VideoCard with YouTube URL (auto-extracts ID)."""
        card = generate_video_card(
            title="Tutorial",
            description="Step-by-step guide",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        )

        assert card.type == "a2ui.VideoCard"
        assert card.props["videoId"] == "dQw4w9WgXcQ"
        assert card.props["platform"] == "youtube"
        assert "videoUrl" not in card.props  # Should use videoId instead

    def test_generate_video_card_with_generic_url(self):
        """Test generating VideoCard with generic (non-YouTube) video URL."""
        card = generate_video_card(
            title="Product Demo",
            description="Our latest product in action",
            video_url="https://example.com/video.mp4",
            thumbnail_url="https://example.com/thumb.jpg"
        )

        assert card.type == "a2ui.VideoCard"
        assert card.props["videoUrl"] == "https://example.com/video.mp4"
        assert card.props["thumbnailUrl"] == "https://example.com/thumb.jpg"
        assert "videoId" not in card.props  # Not a YouTube video
        assert "platform" not in card.props  # Generic video

    def test_generate_video_card_with_thumbnail(self):
        """Test VideoCard with optional thumbnail."""
        card = generate_video_card(
            title="Test Video",
            description="Test",
            video_id="abc123",
            thumbnail_url="https://example.com/thumb.jpg"
        )

        assert card.props["thumbnailUrl"] == "https://example.com/thumb.jpg"

    def test_generate_video_card_missing_both_id_and_url(self):
        """Test VideoCard raises error when neither video_id nor video_url provided."""
        with pytest.raises(ValueError) as exc_info:
            generate_video_card(
                title="Test",
                description="Test"
            )

        assert "requires either video_id or video_url" in str(exc_info.value)

    def test_generate_video_card_json_serialization(self):
        """Test VideoCard serializes to valid JSON."""
        card = generate_video_card(
            title="Test",
            description="Test",
            video_id="abc123"
        )

        card_dict = card.model_dump(exclude_none=True)
        json_str = json.dumps(card_dict)
        parsed = json.loads(json_str)

        assert parsed["type"] == "a2ui.VideoCard"
        assert parsed["props"]["videoId"] == "abc123"

    # ImageCard Tests

    def test_generate_image_card_basic(self):
        """Test generating ImageCard with required fields."""
        card = generate_image_card(
            title="Beautiful Sunset",
            image_url="https://example.com/sunset.jpg"
        )

        assert isinstance(card, A2UIComponent)
        assert card.type == "a2ui.ImageCard"
        assert card.props["title"] == "Beautiful Sunset"
        assert card.props["imageUrl"] == "https://example.com/sunset.jpg"
        assert "altText" not in card.props  # Optional field not included
        assert "caption" not in card.props
        assert "credit" not in card.props

    def test_generate_image_card_with_all_fields(self):
        """Test generating ImageCard with all optional fields."""
        card = generate_image_card(
            title="Mountain Landscape",
            image_url="https://example.com/mountain.jpg",
            alt_text="Snow-capped mountain peaks at sunrise",
            caption="The view from base camp at 4,000m elevation",
            credit="Photo by Jane Smith"
        )

        assert card.props["title"] == "Mountain Landscape"
        assert card.props["imageUrl"] == "https://example.com/mountain.jpg"
        assert card.props["altText"] == "Snow-capped mountain peaks at sunrise"
        assert card.props["caption"] == "The view from base camp at 4,000m elevation"
        assert card.props["credit"] == "Photo by Jane Smith"

    def test_generate_image_card_empty_url(self):
        """Test ImageCard raises error for empty image_url."""
        with pytest.raises(ValueError) as exc_info:
            generate_image_card(
                title="Test",
                image_url=""
            )

        assert "requires a valid image_url" in str(exc_info.value)

    def test_generate_image_card_invalid_url_format(self):
        """Test ImageCard raises error for invalid URL format."""
        with pytest.raises(ValueError) as exc_info:
            generate_image_card(
                title="Test",
                image_url="not-a-url"
            )

        assert "must be a valid URL" in str(exc_info.value)
        assert "http://" in str(exc_info.value) or "https://" in str(exc_info.value)

    def test_generate_image_card_json_serialization(self):
        """Test ImageCard serializes to valid JSON."""
        card = generate_image_card(
            title="Test",
            image_url="https://example.com/test.jpg",
            alt_text="Test image"
        )

        card_dict = card.model_dump(exclude_none=True)
        json_str = json.dumps(card_dict)
        parsed = json.loads(json_str)

        assert parsed["type"] == "a2ui.ImageCard"
        assert parsed["props"]["altText"] == "Test image"

    # PlaylistCard Tests

    def test_generate_playlist_card_youtube(self):
        """Test generating PlaylistCard for YouTube."""
        items = [
            {"title": "Introduction", "videoId": "abc123", "duration": "10:30"},
            {"title": "Deep Learning", "videoId": "def456", "duration": "15:45"}
        ]

        card = generate_playlist_card(
            title="AI Tutorial Series",
            description="Complete guide to machine learning",
            items=items,
            platform="youtube"
        )

        assert isinstance(card, A2UIComponent)
        assert card.type == "a2ui.PlaylistCard"
        assert card.props["title"] == "AI Tutorial Series"
        assert card.props["description"] == "Complete guide to machine learning"
        assert card.props["platform"] == "youtube"
        assert len(card.props["items"]) == 2
        assert card.props["items"][0]["title"] == "Introduction"
        assert card.props["items"][0]["videoId"] == "abc123"
        assert card.props["items"][1]["duration"] == "15:45"

    def test_generate_playlist_card_spotify(self):
        """Test generating PlaylistCard for Spotify."""
        items = [
            {"title": "Track 1", "url": "https://spotify.com/track/1"},
            {"title": "Track 2", "url": "https://spotify.com/track/2"}
        ]

        card = generate_playlist_card(
            title="Focus Music",
            description="Music for deep work",
            items=items,
            platform="spotify"
        )

        assert card.props["platform"] == "spotify"
        assert card.props["items"][0]["url"] == "https://spotify.com/track/1"

    def test_generate_playlist_card_custom_platform(self):
        """Test generating PlaylistCard with custom platform."""
        items = [
            {"title": "Item 1", "url": "https://example.com/1"}
        ]

        card = generate_playlist_card(
            title="Custom Playlist",
            description="Custom content",
            items=items,
            platform="custom"
        )

        assert card.props["platform"] == "custom"

    def test_generate_playlist_card_max_items(self):
        """Test PlaylistCard with maximum 20 items."""
        items = [
            {"title": f"Item {i}", "url": f"https://example.com/{i}"}
            for i in range(20)
        ]

        card = generate_playlist_card(
            title="Max Playlist",
            description="20 items",
            items=items
        )

        assert len(card.props["items"]) == 20

    def test_generate_playlist_card_too_many_items(self):
        """Test PlaylistCard raises error for more than 20 items."""
        items = [
            {"title": f"Item {i}", "url": f"https://example.com/{i}"}
            for i in range(21)
        ]

        with pytest.raises(ValueError) as exc_info:
            generate_playlist_card(
                title="Too Many",
                description="Test",
                items=items
            )

        assert "supports up to 20 items" in str(exc_info.value)
        assert "21" in str(exc_info.value)

    def test_generate_playlist_card_empty_items(self):
        """Test PlaylistCard raises error for empty items list."""
        with pytest.raises(ValueError) as exc_info:
            generate_playlist_card(
                title="Empty",
                description="Test",
                items=[]
            )

        assert "requires at least one item" in str(exc_info.value)

    def test_generate_playlist_card_missing_title_in_item(self):
        """Test PlaylistCard raises error when item missing title."""
        items = [
            {"url": "https://example.com/1"}  # Missing title
        ]

        with pytest.raises(ValueError) as exc_info:
            generate_playlist_card(
                title="Test",
                description="Test",
                items=items
            )

        assert "missing required key: 'title'" in str(exc_info.value)

    def test_generate_playlist_card_missing_url_and_video_id(self):
        """Test PlaylistCard raises error when item has neither url nor videoId."""
        items = [
            {"title": "Test"}  # Missing both url and videoId
        ]

        with pytest.raises(ValueError) as exc_info:
            generate_playlist_card(
                title="Test",
                description="Test",
                items=items
            )

        assert "must have either 'url' or 'videoId'" in str(exc_info.value)

    def test_generate_playlist_card_invalid_platform(self):
        """Test PlaylistCard raises error for invalid platform."""
        items = [{"title": "Test", "url": "https://example.com"}]

        with pytest.raises(ValueError) as exc_info:
            generate_playlist_card(
                title="Test",
                description="Test",
                items=items,
                platform="invalid"
            )

        assert "Invalid platform" in str(exc_info.value)
        assert "youtube" in str(exc_info.value)
        assert "spotify" in str(exc_info.value)

    # PodcastCard Tests

    def test_generate_podcast_card_basic(self):
        """Test generating PodcastCard with required fields."""
        card = generate_podcast_card(
            title="Tech Talk",
            description="Weekly tech discussions",
            episode_title="AI Revolution",
            audio_url="https://example.com/episode-5.mp3",
            duration=45
        )

        assert isinstance(card, A2UIComponent)
        assert card.type == "a2ui.PodcastCard"
        assert card.props["title"] == "Tech Talk"
        assert card.props["description"] == "Weekly tech discussions"
        assert card.props["episodeTitle"] == "AI Revolution"
        assert card.props["audioUrl"] == "https://example.com/episode-5.mp3"
        assert card.props["duration"] == 45
        assert "episodeNumber" not in card.props  # Optional field not included
        assert "platform" not in card.props

    def test_generate_podcast_card_with_all_fields(self):
        """Test generating PodcastCard with all optional fields."""
        card = generate_podcast_card(
            title="The AI Podcast",
            description="Exploring artificial intelligence",
            episode_title="Deep Learning Fundamentals",
            audio_url="https://example.com/episode.mp3",
            duration=60,
            episode_number=10,
            platform="spotify"
        )

        assert card.props["episodeNumber"] == 10
        assert card.props["platform"] == "spotify"

    def test_generate_podcast_card_all_platforms(self):
        """Test PodcastCard with all valid platforms."""
        platforms = ["spotify", "apple", "rss", "custom"]

        for platform in platforms:
            card = generate_podcast_card(
                title="Test",
                description="Test",
                episode_title="Test Episode",
                audio_url="https://example.com/test.mp3",
                duration=30,
                platform=platform
            )
            assert card.props["platform"] == platform

    def test_generate_podcast_card_empty_audio_url(self):
        """Test PodcastCard raises error for empty audio_url."""
        with pytest.raises(ValueError) as exc_info:
            generate_podcast_card(
                title="Test",
                description="Test",
                episode_title="Test",
                audio_url="",
                duration=30
            )

        assert "requires a valid audio_url" in str(exc_info.value)

    def test_generate_podcast_card_invalid_duration(self):
        """Test PodcastCard raises error for invalid duration."""
        with pytest.raises(ValueError) as exc_info:
            generate_podcast_card(
                title="Test",
                description="Test",
                episode_title="Test",
                audio_url="https://example.com/test.mp3",
                duration=0
            )

        assert "Duration must be positive" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            generate_podcast_card(
                title="Test",
                description="Test",
                episode_title="Test",
                audio_url="https://example.com/test.mp3",
                duration=-5
            )

        assert "Duration must be positive" in str(exc_info.value)

    def test_generate_podcast_card_invalid_platform(self):
        """Test PodcastCard raises error for invalid platform."""
        with pytest.raises(ValueError) as exc_info:
            generate_podcast_card(
                title="Test",
                description="Test",
                episode_title="Test",
                audio_url="https://example.com/test.mp3",
                duration=30,
                platform="invalid"
            )

        assert "Invalid platform" in str(exc_info.value)
        assert "spotify" in str(exc_info.value)
        assert "apple" in str(exc_info.value)

    def test_generate_podcast_card_json_serialization(self):
        """Test PodcastCard serializes to valid JSON."""
        card = generate_podcast_card(
            title="Test",
            description="Test",
            episode_title="Test Episode",
            audio_url="https://example.com/test.mp3",
            duration=30,
            episode_number=5
        )

        card_dict = card.model_dump(exclude_none=True)
        json_str = json.dumps(card_dict)
        parsed = json.loads(json_str)

        assert parsed["type"] == "a2ui.PodcastCard"
        assert parsed["props"]["episodeNumber"] == 5


class TestMediaGeneratorsIntegration:
    """Integration tests for media component generators."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_media_workflow_complete(self):
        """Test complete media workflow with all media types."""
        # Create video card
        video = generate_video_card(
            title="Tutorial Video",
            description="Learn the basics",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            duration="10:30"
        )

        # Create image card
        image = generate_image_card(
            title="Diagram",
            image_url="https://example.com/diagram.jpg",
            alt_text="System architecture diagram",
            caption="Overview of the system"
        )

        # Create playlist
        playlist = generate_playlist_card(
            title="Complete Course",
            description="Full video series",
            items=[
                {"title": "Part 1", "videoId": "abc123", "duration": "15:00"},
                {"title": "Part 2", "videoId": "def456", "duration": "20:00"}
            ]
        )

        # Create podcast
        podcast = generate_podcast_card(
            title="Tech Podcast",
            description="Weekly tech news",
            episode_title="Latest Updates",
            audio_url="https://example.com/episode.mp3",
            duration=45,
            episode_number=10
        )

        # Verify all components
        assert video.type == "a2ui.VideoCard"
        assert image.type == "a2ui.ImageCard"
        assert playlist.type == "a2ui.PlaylistCard"
        assert podcast.type == "a2ui.PodcastCard"

        # Verify unique IDs
        all_ids = [video.id, image.id, playlist.id, podcast.id]
        assert len(all_ids) == len(set(all_ids))

    def test_media_youtube_url_variations(self):
        """Test VideoCard handles various YouTube URL formats."""
        urls = [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://www.youtube.com/embed/dQw4w9WgXcQ",
            "http://www.youtube.com/watch?v=dQw4w9WgXcQ",
        ]

        for url in urls:
            card = generate_video_card(
                title="Test",
                description="Test",
                video_url=url
            )
            assert card.props["videoId"] == "dQw4w9WgXcQ"
            assert card.props["platform"] == "youtube"

    @pytest.mark.asyncio
    async def test_media_components_emission(self):
        """Test emitting media components in AG-UI format."""
        components = [
            generate_video_card(
                title="Video",
                description="Test video",
                video_id="abc123"
            ),
            generate_image_card(
                title="Image",
                image_url="https://example.com/image.jpg"
            ),
            generate_podcast_card(
                title="Podcast",
                description="Test podcast",
                episode_title="Episode 1",
                audio_url="https://example.com/audio.mp3",
                duration=30
            )
        ]

        events = []
        async for event in emit_components(components):
            events.append(event)

        assert len(events) == 3

        # Parse and verify VideoCard
        json_str = events[0].replace("data: ", "").strip()
        data = json.loads(json_str)
        assert data["type"] == "a2ui.VideoCard"
        assert data["props"]["videoId"] == "abc123"

        # Parse and verify ImageCard
        json_str = events[1].replace("data: ", "").strip()
        data = json.loads(json_str)
        assert data["type"] == "a2ui.ImageCard"
        assert data["props"]["imageUrl"] == "https://example.com/image.jpg"

        # Parse and verify PodcastCard
        json_str = events[2].replace("data: ", "").strip()
        data = json.loads(json_str)
        assert data["type"] == "a2ui.PodcastCard"
        assert data["props"]["duration"] == 30

    def test_media_rich_content_scenario(self):
        """Test realistic scenario with media-rich content."""
        # Simulate a course page with multiple media types
        components = []

        # Header video
        components.append(generate_video_card(
            title="Course Introduction",
            description="Welcome to the course",
            video_url="https://www.youtube.com/watch?v=intro123",
            thumbnail_url="https://example.com/intro-thumb.jpg",
            duration="5:00"
        ))

        # Reference images
        for i in range(3):
            components.append(generate_image_card(
                title=f"Diagram {i+1}",
                image_url=f"https://example.com/diagram-{i+1}.jpg",
                alt_text=f"Diagram showing step {i+1}",
                caption=f"Step {i+1}: Key concepts"
            ))

        # Video playlist
        components.append(generate_playlist_card(
            title="Video Lectures",
            description="Complete video series",
            items=[
                {"title": f"Lecture {i}", "videoId": f"lec{i}", "duration": f"{15+i*5}:00"}
                for i in range(1, 6)
            ],
            platform="youtube"
        ))

        # Podcast episodes
        for i in range(2):
            components.append(generate_podcast_card(
                title="Course Podcast",
                description="Deep dives into topics",
                episode_title=f"Episode {i+1}: Advanced Topics",
                audio_url=f"https://example.com/episode-{i+1}.mp3",
                duration=60 + i*15,
                episode_number=i+1,
                platform="spotify"
            ))

        # Verify counts
        assert len(components) == 1 + 3 + 1 + 2  # 1 video + 3 images + 1 playlist + 2 podcasts
        assert len([c for c in components if c.type == "a2ui.VideoCard"]) == 1
        assert len([c for c in components if c.type == "a2ui.ImageCard"]) == 3
        assert len([c for c in components if c.type == "a2ui.PlaylistCard"]) == 1
        assert len([c for c in components if c.type == "a2ui.PodcastCard"]) == 2

        # Verify all IDs unique
        all_ids = [c.id for c in components]
        assert len(all_ids) == len(set(all_ids))


class TestDataGenerators:
    """Test suite for data component generators."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    # StatCard Tests

    def test_generate_stat_card_basic(self):
        """Test generating StatCard with required fields only."""
        card = generate_stat_card(
            title="Total Users",
            value="1,234"
        )

        assert isinstance(card, A2UIComponent)
        assert card.type == "a2ui.StatCard"
        assert card.props["title"] == "Total Users"
        assert card.props["value"] == "1,234"
        assert card.props["changeType"] == "neutral"
        assert card.props["highlight"] is False
        assert "unit" not in card.props
        assert "change" not in card.props

    def test_generate_stat_card_with_all_fields(self):
        """Test generating StatCard with all optional fields."""
        card = generate_stat_card(
            title="Revenue",
            value="$5.2M",
            unit="USD",
            change=12.5,
            change_type="positive",
            highlight=True
        )

        assert card.props["title"] == "Revenue"
        assert card.props["value"] == "$5.2M"
        assert card.props["unit"] == "USD"
        assert card.props["change"] == 12.5
        assert card.props["changeType"] == "positive"
        assert card.props["highlight"] is True

    def test_generate_stat_card_all_change_types(self):
        """Test StatCard with all valid change types."""
        positive_card = generate_stat_card(
            title="Growth", value="100", change=5.5, change_type="positive"
        )
        assert positive_card.props["changeType"] == "positive"

        negative_card = generate_stat_card(
            title="Decline", value="90", change=-5.5, change_type="negative"
        )
        assert negative_card.props["changeType"] == "negative"

        neutral_card = generate_stat_card(
            title="Stable", value="100", change=0.1, change_type="neutral"
        )
        assert neutral_card.props["changeType"] == "neutral"

    def test_generate_stat_card_invalid_change_type(self):
        """Test StatCard raises error for invalid change_type."""
        with pytest.raises(ValueError) as exc_info:
            generate_stat_card(
                title="Test", value="100", change_type="invalid"
            )

        assert "Invalid change_type" in str(exc_info.value)
        assert "invalid" in str(exc_info.value)

    def test_generate_stat_card_negative_change_positive_type(self):
        """Test StatCard can have negative change with positive type (e.g., lower error rate)."""
        card = generate_stat_card(
            title="Error Rate",
            value="2.3",
            unit="%",
            change=-0.5,
            change_type="positive"  # Lower is better
        )

        assert card.props["change"] == -0.5
        assert card.props["changeType"] == "positive"

    def test_generate_stat_card_json_serialization(self):
        """Test StatCard serializes to valid JSON."""
        card = generate_stat_card(
            title="Test", value="100", unit="%", change=5.0, highlight=True
        )

        card_dict = card.model_dump(exclude_none=True)
        json_str = json.dumps(card_dict)
        parsed = json.loads(json_str)

        assert parsed["type"] == "a2ui.StatCard"
        assert parsed["props"]["highlight"] is True

    # MetricRow Tests

    def test_generate_metric_row_basic(self):
        """Test generating MetricRow with required fields."""
        row = generate_metric_row(
            label="CPU Usage",
            value="45"
        )

        assert isinstance(row, A2UIComponent)
        assert row.type == "a2ui.MetricRow"
        assert row.props["label"] == "CPU Usage"
        assert row.props["value"] == "45"
        assert "unit" not in row.props
        assert "status" not in row.props

    def test_generate_metric_row_with_all_fields(self):
        """Test generating MetricRow with all optional fields."""
        row = generate_metric_row(
            label="Response Time",
            value="125",
            unit="ms",
            status="good"
        )

        assert row.props["label"] == "Response Time"
        assert row.props["value"] == "125"
        assert row.props["unit"] == "ms"
        assert row.props["status"] == "good"

    def test_generate_metric_row_all_statuses(self):
        """Test MetricRow with all valid status values."""
        statuses = ["good", "warning", "critical", "neutral"]

        for status in statuses:
            row = generate_metric_row(
                label="Test Metric",
                value="100",
                status=status
            )
            assert row.props["status"] == status

    def test_generate_metric_row_invalid_status(self):
        """Test MetricRow raises error for invalid status."""
        with pytest.raises(ValueError) as exc_info:
            generate_metric_row(
                label="Test", value="100", status="invalid"
            )

        assert "Invalid status" in str(exc_info.value)
        assert "invalid" in str(exc_info.value)

    def test_generate_metric_row_json_serialization(self):
        """Test MetricRow serializes to valid JSON."""
        row = generate_metric_row(
            label="Memory", value="85", unit="%", status="warning"
        )

        card_dict = row.model_dump(exclude_none=True)
        json_str = json.dumps(card_dict)
        parsed = json.loads(json_str)

        assert parsed["type"] == "a2ui.MetricRow"
        assert parsed["props"]["status"] == "warning"

    # ProgressRing Tests

    def test_generate_progress_ring_basic(self):
        """Test generating ProgressRing with required fields."""
        ring = generate_progress_ring(
            label="Course Progress",
            current=75
        )

        assert isinstance(ring, A2UIComponent)
        assert ring.type == "a2ui.ProgressRing"
        assert ring.props["label"] == "Course Progress"
        assert ring.props["current"] == 75
        assert ring.props["maximum"] == 100
        assert ring.props["color"] == "blue"
        assert "unit" not in ring.props

    def test_generate_progress_ring_with_all_fields(self):
        """Test generating ProgressRing with all optional fields."""
        ring = generate_progress_ring(
            label="Storage Used",
            current=45.2,
            maximum=100,
            unit="GB",
            color="green"
        )

        assert ring.props["label"] == "Storage Used"
        assert ring.props["current"] == 45.2
        assert ring.props["maximum"] == 100
        assert ring.props["unit"] == "GB"
        assert ring.props["color"] == "green"

    def test_generate_progress_ring_all_colors(self):
        """Test ProgressRing with all valid colors."""
        colors = ["blue", "green", "red", "yellow", "purple", "gray"]

        for color in colors:
            ring = generate_progress_ring(
                label="Test", current=50, color=color
            )
            assert ring.props["color"] == color

    def test_generate_progress_ring_invalid_color(self):
        """Test ProgressRing raises error for invalid color."""
        with pytest.raises(ValueError) as exc_info:
            generate_progress_ring(
                label="Test", current=50, color="pink"
            )

        assert "Invalid color" in str(exc_info.value)
        assert "pink" in str(exc_info.value)

    def test_generate_progress_ring_edge_cases(self):
        """Test ProgressRing with edge case values (0%, 100%, >100%)."""
        # 0% progress
        ring_zero = generate_progress_ring(
            label="Not Started", current=0, maximum=100
        )
        assert ring_zero.props["current"] == 0

        # 100% progress
        ring_full = generate_progress_ring(
            label="Complete", current=100, maximum=100
        )
        assert ring_full.props["current"] == 100

        # Over 100%
        ring_over = generate_progress_ring(
            label="Exceeded", current=120, maximum=100
        )
        assert ring_over.props["current"] == 120

    def test_generate_progress_ring_custom_maximum(self):
        """Test ProgressRing with custom maximum value."""
        ring = generate_progress_ring(
            label="Tasks", current=8, maximum=10, unit="tasks"
        )

        assert ring.props["current"] == 8
        assert ring.props["maximum"] == 10

    def test_generate_progress_ring_negative_current(self):
        """Test ProgressRing raises error for negative current."""
        with pytest.raises(ValueError) as exc_info:
            generate_progress_ring(
                label="Test", current=-5
            )

        assert "cannot be negative" in str(exc_info.value)

    def test_generate_progress_ring_invalid_maximum(self):
        """Test ProgressRing raises error for invalid maximum."""
        with pytest.raises(ValueError) as exc_info:
            generate_progress_ring(
                label="Test", current=50, maximum=0
            )

        assert "must be positive" in str(exc_info.value)

    # ComparisonBar Tests

    def test_generate_comparison_bar_basic(self):
        """Test generating ComparisonBar with basic items."""
        items = [
            {"label": "Chrome", "value": 65.5},
            {"label": "Safari", "value": 18.2},
            {"label": "Firefox", "value": 8.1}
        ]

        bar = generate_comparison_bar(
            label="Browser Market Share",
            items=items
        )

        assert isinstance(bar, A2UIComponent)
        assert bar.type == "a2ui.ComparisonBar"
        assert bar.props["label"] == "Browser Market Share"
        assert len(bar.props["items"]) == 3
        assert bar.props["items"][0]["label"] == "Chrome"
        assert bar.props["items"][0]["value"] == 65.5
        assert bar.props["maxValue"] == 65.5  # Auto-calculated

    def test_generate_comparison_bar_with_colors(self):
        """Test ComparisonBar with custom colors."""
        items = [
            {"label": "Chrome", "value": 65.5, "color": "green"},
            {"label": "Safari", "value": 18.2, "color": "blue"},
            {"label": "Firefox", "value": 8.1, "color": "orange"}
        ]

        bar = generate_comparison_bar(
            label="Browser Share",
            items=items
        )

        assert bar.props["items"][0]["color"] == "green"
        assert bar.props["items"][1]["color"] == "blue"
        assert bar.props["items"][2]["color"] == "orange"

    def test_generate_comparison_bar_custom_max(self):
        """Test ComparisonBar with custom max_value."""
        items = [
            {"label": "A", "value": 50},
            {"label": "B", "value": 30}
        ]

        bar = generate_comparison_bar(
            label="Test",
            items=items,
            max_value=100
        )

        assert bar.props["maxValue"] == 100

    def test_generate_comparison_bar_auto_max(self):
        """Test ComparisonBar auto-calculates max from items."""
        items = [
            {"label": "A", "value": 92},
            {"label": "B", "value": 88},
            {"label": "C", "value": 95}
        ]

        bar = generate_comparison_bar(
            label="Test",
            items=items
        )

        assert bar.props["maxValue"] == 95  # Auto-calculated from max value

    def test_generate_comparison_bar_max_items(self):
        """Test ComparisonBar with maximum 10 items."""
        items = [
            {"label": f"Item {i}", "value": i * 10}
            for i in range(10)
        ]

        bar = generate_comparison_bar(
            label="Test",
            items=items
        )

        assert len(bar.props["items"]) == 10

    def test_generate_comparison_bar_too_many_items(self):
        """Test ComparisonBar raises error for more than 10 items."""
        items = [
            {"label": f"Item {i}", "value": i * 10}
            for i in range(11)
        ]

        with pytest.raises(ValueError) as exc_info:
            generate_comparison_bar(
                label="Test",
                items=items
            )

        assert "supports up to 10 items" in str(exc_info.value)
        assert "11" in str(exc_info.value)

    def test_generate_comparison_bar_empty_items(self):
        """Test ComparisonBar raises error for empty items list."""
        with pytest.raises(ValueError) as exc_info:
            generate_comparison_bar(
                label="Test",
                items=[]
            )

        assert "requires at least one item" in str(exc_info.value)

    def test_generate_comparison_bar_missing_label(self):
        """Test ComparisonBar raises error when item missing label."""
        items = [
            {"value": 100}  # Missing label
        ]

        with pytest.raises(ValueError) as exc_info:
            generate_comparison_bar(
                label="Test",
                items=items
            )

        assert "missing required key: 'label'" in str(exc_info.value)

    def test_generate_comparison_bar_missing_value(self):
        """Test ComparisonBar raises error when item missing value."""
        items = [
            {"label": "Test"}  # Missing value
        ]

        with pytest.raises(ValueError) as exc_info:
            generate_comparison_bar(
                label="Test",
                items=items
            )

        assert "missing required key: 'value'" in str(exc_info.value)

    def test_generate_comparison_bar_invalid_value_type(self):
        """Test ComparisonBar raises error for non-numeric value."""
        items = [
            {"label": "Test", "value": "not a number"}
        ]

        with pytest.raises(ValueError) as exc_info:
            generate_comparison_bar(
                label="Test",
                items=items
            )

        assert "must be a number" in str(exc_info.value)

    # DataTable Tests

    def test_generate_data_table_basic(self):
        """Test generating DataTable with required fields."""
        table = generate_data_table(
            headers=["Name", "Age", "City"],
            rows=[
                ["Alice", 28, "New York"],
                ["Bob", 34, "San Francisco"],
                ["Charlie", 23, "Boston"]
            ]
        )

        assert isinstance(table, A2UIComponent)
        assert table.type == "a2ui.DataTable"
        assert table.props["headers"] == ["Name", "Age", "City"]
        assert len(table.props["rows"]) == 3
        assert table.props["rows"][0] == ["Alice", 28, "New York"]
        assert table.props["sortable"] is False
        assert table.props["filterable"] is False
        assert table.props["striped"] is True

    def test_generate_data_table_with_all_options(self):
        """Test generating DataTable with all options enabled."""
        table = generate_data_table(
            headers=["Product", "Price", "Stock", "Status"],
            rows=[
                ["Widget A", "$29.99", 150, "In Stock"],
                ["Widget B", "$39.99", 0, "Out of Stock"]
            ],
            sortable=True,
            filterable=True,
            striped=False
        )

        assert table.props["sortable"] is True
        assert table.props["filterable"] is True
        assert table.props["striped"] is False

    def test_generate_data_table_max_rows(self):
        """Test DataTable with maximum 50 rows."""
        rows = [[f"Item {i}", i, f"Value {i}"] for i in range(50)]

        table = generate_data_table(
            headers=["Name", "ID", "Value"],
            rows=rows
        )

        assert len(table.props["rows"]) == 50

    def test_generate_data_table_too_many_rows(self):
        """Test DataTable raises error for more than 50 rows."""
        rows = [[f"Item {i}", i, f"Value {i}"] for i in range(51)]

        with pytest.raises(ValueError) as exc_info:
            generate_data_table(
                headers=["Name", "ID", "Value"],
                rows=rows
            )

        assert "supports up to 50 rows" in str(exc_info.value)
        assert "51" in str(exc_info.value)

    def test_generate_data_table_empty_headers(self):
        """Test DataTable raises error for empty headers."""
        with pytest.raises(ValueError) as exc_info:
            generate_data_table(
                headers=[],
                rows=[["data"]]
            )

        assert "requires at least one header" in str(exc_info.value)

    def test_generate_data_table_empty_rows(self):
        """Test DataTable raises error for empty rows."""
        with pytest.raises(ValueError) as exc_info:
            generate_data_table(
                headers=["Name"],
                rows=[]
            )

        assert "requires at least one row" in str(exc_info.value)

    def test_generate_data_table_mismatched_row_length(self):
        """Test DataTable raises error when row length doesn't match headers."""
        with pytest.raises(ValueError) as exc_info:
            generate_data_table(
                headers=["Name", "Age", "City"],
                rows=[
                    ["Alice", 28, "New York"],
                    ["Bob", 34]  # Missing city
                ]
            )

        assert "has 2 cells, but expected 3" in str(exc_info.value)

    def test_generate_data_table_various_data_types(self):
        """Test DataTable supports various data types in cells."""
        table = generate_data_table(
            headers=["String", "Int", "Float", "Bool", "None"],
            rows=[
                ["text", 42, 3.14, True, None],
                ["more", 100, 2.71, False, None]
            ]
        )

        assert table.props["rows"][0][0] == "text"
        assert table.props["rows"][0][1] == 42
        assert table.props["rows"][0][2] == 3.14
        assert table.props["rows"][0][3] is True
        assert table.props["rows"][0][4] is None

    # MiniChart Tests

    def test_generate_mini_chart_basic(self):
        """Test generating MiniChart with required fields."""
        chart = generate_mini_chart(
            chart_type="line",
            data_points=[10, 12, 15, 14, 18, 22, 25]
        )

        assert isinstance(chart, A2UIComponent)
        assert chart.type == "a2ui.MiniChart"
        assert chart.props["chartType"] == "line"
        assert chart.props["dataPoints"] == [10, 12, 15, 14, 18, 22, 25]
        assert "labels" not in chart.props
        assert "title" not in chart.props

    def test_generate_mini_chart_with_all_fields(self):
        """Test generating MiniChart with all optional fields."""
        chart = generate_mini_chart(
            chart_type="bar",
            data_points=[45, 62, 38, 55, 70],
            labels=["Q1", "Q2", "Q3", "Q4", "Q5"],
            title="Quarterly Revenue"
        )

        assert chart.props["chartType"] == "bar"
        assert chart.props["dataPoints"] == [45, 62, 38, 55, 70]
        assert chart.props["labels"] == ["Q1", "Q2", "Q3", "Q4", "Q5"]
        assert chart.props["title"] == "Quarterly Revenue"

    def test_generate_mini_chart_all_types(self):
        """Test MiniChart with all valid chart types."""
        chart_types = ["line", "bar", "area", "pie", "donut"]
        data_points = [10, 20, 30, 40, 50]

        for chart_type in chart_types:
            chart = generate_mini_chart(
                chart_type=chart_type,
                data_points=data_points
            )
            assert chart.props["chartType"] == chart_type

    def test_generate_mini_chart_invalid_type(self):
        """Test MiniChart raises error for invalid chart type."""
        with pytest.raises(ValueError) as exc_info:
            generate_mini_chart(
                chart_type="scatter",
                data_points=[10, 20, 30, 40, 50]
            )

        assert "Invalid chart_type" in str(exc_info.value)
        assert "scatter" in str(exc_info.value)

    def test_generate_mini_chart_minimum_data_points(self):
        """Test MiniChart with minimum 5 data points."""
        chart = generate_mini_chart(
            chart_type="line",
            data_points=[10, 20, 30, 40, 50]
        )

        assert len(chart.props["dataPoints"]) == 5

    def test_generate_mini_chart_too_few_data_points(self):
        """Test MiniChart raises error for fewer than 5 data points."""
        with pytest.raises(ValueError) as exc_info:
            generate_mini_chart(
                chart_type="line",
                data_points=[10, 20, 30, 40]
            )

        assert "requires at least 5 data points" in str(exc_info.value)
        assert "4" in str(exc_info.value)

    def test_generate_mini_chart_maximum_data_points(self):
        """Test MiniChart with maximum 100 data points."""
        data_points = list(range(100))

        chart = generate_mini_chart(
            chart_type="line",
            data_points=data_points
        )

        assert len(chart.props["dataPoints"]) == 100

    def test_generate_mini_chart_too_many_data_points(self):
        """Test MiniChart raises error for more than 100 data points."""
        data_points = list(range(101))

        with pytest.raises(ValueError) as exc_info:
            generate_mini_chart(
                chart_type="line",
                data_points=data_points
            )

        assert "supports up to 100 data points" in str(exc_info.value)
        assert "101" in str(exc_info.value)

    def test_generate_mini_chart_labels_mismatch(self):
        """Test MiniChart raises error when labels length doesn't match data points."""
        with pytest.raises(ValueError) as exc_info:
            generate_mini_chart(
                chart_type="bar",
                data_points=[10, 20, 30, 40, 50],
                labels=["A", "B", "C"]  # Only 3 labels for 5 data points
            )

        assert "Labels length (3) must match data_points length (5)" in str(exc_info.value)

    def test_generate_mini_chart_invalid_data_type(self):
        """Test MiniChart raises error for non-numeric data points."""
        with pytest.raises(ValueError) as exc_info:
            generate_mini_chart(
                chart_type="line",
                data_points=[10, 20, "not a number", 40, 50]
            )

        assert "must be a number" in str(exc_info.value)

    def test_generate_mini_chart_float_data_points(self):
        """Test MiniChart supports float data points."""
        chart = generate_mini_chart(
            chart_type="line",
            data_points=[10.5, 12.3, 15.7, 14.2, 18.9]
        )

        assert chart.props["dataPoints"][0] == 10.5
        assert chart.props["dataPoints"][4] == 18.9


class TestDataGeneratorsIntegration:
    """Integration tests for data component generators."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_data_integration_complete_dashboard(self):
        """Test creating a complete data dashboard with all data components."""
        components = []

        # Stat cards for KPIs
        components.append(generate_stat_card(
            title="Total Revenue",
            value="$1.2M",
            unit="USD",
            change=15.3,
            change_type="positive",
            highlight=True
        ))

        components.append(generate_stat_card(
            title="Active Users",
            value="45,231",
            unit="users",
            change=8.7,
            change_type="positive"
        ))

        components.append(generate_stat_card(
            title="Error Rate",
            value="0.3",
            unit="%",
            change=-0.2,
            change_type="positive"  # Lower is better
        ))

        # Metric rows for system health
        components.append(generate_metric_row(
            label="CPU Usage",
            value="45",
            unit="%",
            status="good"
        ))

        components.append(generate_metric_row(
            label="Memory Usage",
            value="78",
            unit="%",
            status="warning"
        ))

        components.append(generate_metric_row(
            label="Disk I/O",
            value="125",
            unit="MB/s",
            status="good"
        ))

        # Progress rings for goals
        components.append(generate_progress_ring(
            label="Q1 Sales Goal",
            current=85,
            maximum=100,
            unit="%",
            color="green"
        ))

        components.append(generate_progress_ring(
            label="Storage Used",
            current=67.5,
            maximum=100,
            unit="GB",
            color="blue"
        ))

        # Comparison bar for market share
        components.append(generate_comparison_bar(
            label="Browser Market Share",
            items=[
                {"label": "Chrome", "value": 65.5, "color": "green"},
                {"label": "Safari", "value": 18.2, "color": "blue"},
                {"label": "Firefox", "value": 8.1, "color": "orange"},
                {"label": "Edge", "value": 5.8, "color": "teal"}
            ]
        ))

        # Data table for top products
        components.append(generate_data_table(
            headers=["Product", "Sales", "Revenue", "Status"],
            rows=[
                ["Widget A", "1,234", "$45,678", "In Stock"],
                ["Widget B", "987", "$38,901", "Low Stock"],
                ["Widget C", "2,345", "$89,012", "In Stock"]
            ],
            sortable=True,
            filterable=True
        ))

        # Mini charts for trends
        components.append(generate_mini_chart(
            chart_type="line",
            data_points=[10, 12, 15, 14, 18, 22, 25, 28, 30],
            labels=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
            title="Monthly Revenue Trend"
        ))

        components.append(generate_mini_chart(
            chart_type="bar",
            data_points=[45, 62, 38, 55, 70],
            labels=["Q1", "Q2", "Q3", "Q4", "Q5"],
            title="Quarterly Performance"
        ))

        # Verify all components created
        # Count: 3 StatCards + 3 MetricRows + 2 ProgressRings + 1 ComparisonBar + 1 DataTable + 2 MiniCharts = 12
        assert len(components) == 12
        assert len([c for c in components if c.type == "a2ui.StatCard"]) == 3
        assert len([c for c in components if c.type == "a2ui.MetricRow"]) == 3
        assert len([c for c in components if c.type == "a2ui.ProgressRing"]) == 2
        assert len([c for c in components if c.type == "a2ui.ComparisonBar"]) == 1
        assert len([c for c in components if c.type == "a2ui.DataTable"]) == 1
        assert len([c for c in components if c.type == "a2ui.MiniChart"]) == 2

        # Verify all IDs unique
        all_ids = [c.id for c in components]
        assert len(all_ids) == len(set(all_ids))

    def test_data_integration_statistics_content(self):
        """Test data generators with realistic statistical data."""
        # AI market statistics scenario
        components = []

        # Market size stat
        components.append(generate_stat_card(
            title="AI Market Size",
            value="$196B",
            change=23.4,
            change_type="positive",
            highlight=True
        ))

        # Growth metrics
        components.append(generate_metric_row(
            label="YoY Growth",
            value="23.4",
            unit="%",
            status="good"
        ))

        # Regional comparison
        components.append(generate_comparison_bar(
            label="Market Share by Region",
            items=[
                {"label": "North America", "value": 45.2},
                {"label": "Europe", "value": 28.5},
                {"label": "Asia Pacific", "value": 20.1},
                {"label": "Rest of World", "value": 6.2}
            ],
            max_value=100
        ))

        # Technology breakdown
        components.append(generate_mini_chart(
            chart_type="pie",
            data_points=[35, 25, 20, 12, 8],
            labels=["ML/DL", "NLP", "Computer Vision", "Robotics", "Other"],
            title="AI Technology Distribution"
        ))

        # Company rankings
        components.append(generate_data_table(
            headers=["Company", "Market Cap", "AI Revenue", "Growth"],
            rows=[
                ["OpenAI", "$86B", "$2.0B", "+150%"],
                ["Anthropic", "$18B", "$0.5B", "+200%"],
                ["Google DeepMind", "N/A", "$10B", "+45%"],
                ["Microsoft AI", "N/A", "$15B", "+60%"]
            ],
            sortable=True
        ))

        # Verify realistic data
        assert components[0].props["value"] == "$196B"
        assert components[1].props["value"] == "23.4"
        assert len(components[2].props["items"]) == 4
        assert components[3].props["chartType"] == "pie"
        assert len(components[4].props["rows"]) == 4

    @pytest.mark.asyncio
    async def test_data_components_emission(self):
        """Test emitting data components in AG-UI format."""
        components = [
            generate_stat_card(
                title="Users", value="1,234", change=5.0, change_type="positive"
            ),
            generate_metric_row(
                label="CPU", value="45", unit="%", status="good"
            ),
            generate_progress_ring(
                label="Progress", current=75, color="green"
            ),
            generate_comparison_bar(
                label="Comparison",
                items=[
                    {"label": "A", "value": 100},
                    {"label": "B", "value": 80}
                ]
            ),
            generate_data_table(
                headers=["Name", "Value"],
                rows=[["Test", 100]]
            ),
            generate_mini_chart(
                chart_type="line",
                data_points=[10, 20, 30, 40, 50]
            )
        ]

        events = []
        async for event in emit_components(components):
            events.append(event)

        assert len(events) == 6

        # Parse and verify each component type
        for i, expected_type in enumerate([
            "a2ui.StatCard",
            "a2ui.MetricRow",
            "a2ui.ProgressRing",
            "a2ui.ComparisonBar",
            "a2ui.DataTable",
            "a2ui.MiniChart"
        ]):
            json_str = events[i].replace("data: ", "").strip()
            data = json.loads(json_str)
            assert data["type"] == expected_type

    def test_data_workflow_mixed_components(self):
        """Test realistic workflow mixing data components with other types."""
        # Create a research report with data visualizations
        components = []

        # Headline
        components.append(generate_headline_card(
            title="AI Market Analysis 2026",
            summary="Comprehensive analysis of the AI market",
            source="Research Institute",
            published_at="2026-01-30T10:00:00Z"
        ))

        # Key stats
        components.append(generate_stat_card(
            title="Market Size", value="$196B", change=23.4, change_type="positive", highlight=True
        ))

        components.append(generate_stat_card(
            title="Companies", value="15,000+", change=1200, change_type="positive"
        ))

        # Trend chart
        components.append(generate_mini_chart(
            chart_type="line",
            data_points=[50, 65, 85, 110, 145, 196],
            labels=["2021", "2022", "2023", "2024", "2025", "2026"],
            title="Market Growth (Billions USD)"
        ))

        # Regional breakdown
        components.append(generate_comparison_bar(
            label="Market by Region",
            items=[
                {"label": "North America", "value": 88.5},
                {"label": "Europe", "value": 55.9},
                {"label": "Asia Pacific", "value": 39.4}
            ]
        ))

        # Detailed table
        components.append(generate_data_table(
            headers=["Segment", "2025", "2026", "Growth"],
            rows=[
                ["ML/DL", "$68B", "$85B", "+25%"],
                ["NLP", "$49B", "$65B", "+33%"],
                ["Computer Vision", "$39B", "$46B", "+18%"]
            ],
            sortable=True,
            striped=True
        ))

        # Verify mixed types
        assert components[0].type == "a2ui.HeadlineCard"
        assert components[1].type == "a2ui.StatCard"
        assert components[3].type == "a2ui.MiniChart"
        assert components[4].type == "a2ui.ComparisonBar"
        assert components[5].type == "a2ui.DataTable"
