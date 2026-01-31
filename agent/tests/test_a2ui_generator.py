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
