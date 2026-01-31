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
    # List generators
    generate_ranked_item,
    generate_checklist_item,
    generate_pro_con_item,
    generate_bullet_point,
    # Resource generators
    extract_domain,
    extract_github_repo_info,
    generate_link_card,
    generate_tool_card,
    generate_book_card,
    generate_repo_card,
    # People generators
    generate_profile_card,
    generate_company_card,
    generate_quote_card,
    generate_expert_tip,
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


class TestRankedItemGenerator:
    """Test suite for generate_ranked_item function."""

    def test_basic_ranked_item(self):
        """Test creating a basic ranked item with minimum required fields."""
        reset_id_counter()
        item = generate_ranked_item(rank=1, title="GPT-4")

        assert item.type == "a2ui.RankedItem"
        assert item.id == "ranked-item-1"
        assert item.props["rank"] == 1
        assert item.props["title"] == "GPT-4"
        assert item.props["scoreMax"] == 10  # Default value
        assert "description" not in item.props
        assert "score" not in item.props
        assert "icon" not in item.props

    def test_ranked_item_with_all_fields(self):
        """Test ranked item with all optional fields."""
        item = generate_ranked_item(
            rank=1,
            title="Tesla Model 3",
            description="Best-selling electric vehicle worldwide",
            score=9.5,
            score_max=10,
            icon="trophy"
        )

        assert item.type == "a2ui.RankedItem"
        assert item.props["rank"] == 1
        assert item.props["title"] == "Tesla Model 3"
        assert item.props["description"] == "Best-selling electric vehicle worldwide"
        assert item.props["score"] == 9.5
        assert item.props["scoreMax"] == 10
        assert item.props["icon"] == "trophy"

    def test_ranked_item_different_ranks(self):
        """Test ranked items with various rank positions."""
        reset_id_counter()
        item1 = generate_ranked_item(rank=1, title="First Place")
        item2 = generate_ranked_item(rank=5, title="Fifth Place")
        item3 = generate_ranked_item(rank=100, title="Hundredth Place")

        assert item1.props["rank"] == 1
        assert item2.props["rank"] == 5
        assert item3.props["rank"] == 100

    def test_ranked_item_score_variations(self):
        """Test ranked item with different score values."""
        # No score
        item1 = generate_ranked_item(rank=1, title="No Score")
        assert "score" not in item1.props

        # Zero score
        item2 = generate_ranked_item(rank=2, title="Zero Score", score=0)
        assert item2.props["score"] == 0

        # Mid score
        item3 = generate_ranked_item(rank=3, title="Mid Score", score=5.5, score_max=10)
        assert item3.props["score"] == 5.5

        # Max score
        item4 = generate_ranked_item(rank=4, title="Max Score", score=10, score_max=10)
        assert item4.props["score"] == 10

    def test_ranked_item_custom_score_max(self):
        """Test ranked item with custom score_max values."""
        item1 = generate_ranked_item(rank=1, title="5 Stars", score=4.5, score_max=5)
        assert item1.props["score"] == 4.5
        assert item1.props["scoreMax"] == 5

        item2 = generate_ranked_item(rank=2, title="100 Points", score=87, score_max=100)
        assert item2.props["score"] == 87
        assert item2.props["scoreMax"] == 100

    def test_ranked_item_top_three_highlighting(self):
        """Test that top 3 ranks can be highlighted."""
        # This tests the data is correct for UI to highlight top items
        reset_id_counter()
        top1 = generate_ranked_item(rank=1, title="Gold", icon="trophy")
        top2 = generate_ranked_item(rank=2, title="Silver", icon="medal")
        top3 = generate_ranked_item(rank=3, title="Bronze", icon="medal")

        assert top1.props["rank"] == 1
        assert top2.props["rank"] == 2
        assert top3.props["rank"] == 3

    def test_ranked_item_invalid_rank(self):
        """Test that invalid rank values raise errors."""
        with pytest.raises(ValueError, match="Rank must be >= 1"):
            generate_ranked_item(rank=0, title="Invalid")

        with pytest.raises(ValueError, match="Rank must be >= 1"):
            generate_ranked_item(rank=-1, title="Invalid")

    def test_ranked_item_invalid_score(self):
        """Test that invalid scores raise errors."""
        with pytest.raises(ValueError, match="Score cannot be negative"):
            generate_ranked_item(rank=1, title="Test", score=-1)

        with pytest.raises(ValueError, match="cannot exceed score_max"):
            generate_ranked_item(rank=1, title="Test", score=11, score_max=10)

    def test_ranked_item_invalid_score_max(self):
        """Test that invalid score_max values raise errors."""
        with pytest.raises(ValueError, match="score_max must be positive"):
            generate_ranked_item(rank=1, title="Test", score_max=0)

        with pytest.raises(ValueError, match="score_max must be positive"):
            generate_ranked_item(rank=1, title="Test", score_max=-5)

    def test_ranked_item_json_serialization(self):
        """Test that ranked item can be serialized to JSON."""
        item = generate_ranked_item(
            rank=1,
            title="Test Item",
            description="Test description",
            score=8.5,
            score_max=10,
            icon="star"
        )

        json_str = json.dumps(item.model_dump(exclude_none=True))
        data = json.loads(json_str)

        assert data["type"] == "a2ui.RankedItem"
        assert data["props"]["rank"] == 1
        assert data["props"]["score"] == 8.5


class TestChecklistItemGenerator:
    """Test suite for generate_checklist_item function."""

    def test_basic_checklist_item(self):
        """Test creating a basic checklist item."""
        reset_id_counter()
        item = generate_checklist_item(text="Complete project proposal")

        assert item.type == "a2ui.ChecklistItem"
        assert item.id == "checklist-item-1"
        assert item.props["text"] == "Complete project proposal"
        assert item.props["checked"] is False
        assert "priority" not in item.props
        assert "dueDate" not in item.props

    def test_checklist_item_checked(self):
        """Test checked checklist item."""
        item = generate_checklist_item(text="Review PR #123", checked=True)

        assert item.props["text"] == "Review PR #123"
        assert item.props["checked"] is True

    def test_checklist_item_with_priority(self):
        """Test checklist items with different priority levels."""
        high = generate_checklist_item(text="Urgent task", priority="high")
        medium = generate_checklist_item(text="Normal task", priority="medium")
        low = generate_checklist_item(text="Low priority task", priority="low")

        assert high.props["priority"] == "high"
        assert medium.props["priority"] == "medium"
        assert low.props["priority"] == "low"

    def test_checklist_item_with_due_date(self):
        """Test checklist item with due date."""
        item = generate_checklist_item(
            text="Submit quarterly report",
            due_date="2026-02-15"
        )

        assert item.props["dueDate"] == "2026-02-15"

    def test_checklist_item_all_fields(self):
        """Test checklist item with all optional fields."""
        item = generate_checklist_item(
            text="Submit quarterly report",
            checked=False,
            priority="high",
            due_date="2026-02-15"
        )

        assert item.props["text"] == "Submit quarterly report"
        assert item.props["checked"] is False
        assert item.props["priority"] == "high"
        assert item.props["dueDate"] == "2026-02-15"

    def test_checklist_item_completed_with_metadata(self):
        """Test completed checklist item with all metadata."""
        item = generate_checklist_item(
            text="Update documentation",
            checked=True,
            priority="low",
            due_date="2026-01-30"
        )

        assert item.props["checked"] is True
        assert item.props["priority"] == "low"
        assert item.props["dueDate"] == "2026-01-30"

    def test_checklist_item_text_trimming(self):
        """Test that whitespace in text is trimmed."""
        item = generate_checklist_item(text="  Trimmed text  ")
        assert item.props["text"] == "Trimmed text"

    def test_checklist_item_empty_text(self):
        """Test that empty text raises error."""
        with pytest.raises(ValueError, match="text cannot be empty"):
            generate_checklist_item(text="")

        with pytest.raises(ValueError, match="text cannot be empty"):
            generate_checklist_item(text="   ")

    def test_checklist_item_invalid_priority(self):
        """Test that invalid priority values raise errors."""
        with pytest.raises(ValueError, match="Invalid priority"):
            generate_checklist_item(text="Task", priority="urgent")

        with pytest.raises(ValueError, match="Invalid priority"):
            generate_checklist_item(text="Task", priority="critical")

    def test_checklist_item_json_serialization(self):
        """Test that checklist item can be serialized to JSON."""
        item = generate_checklist_item(
            text="Test task",
            checked=True,
            priority="high",
            due_date="2026-02-01"
        )

        json_str = json.dumps(item.model_dump(exclude_none=True))
        data = json.loads(json_str)

        assert data["type"] == "a2ui.ChecklistItem"
        assert data["props"]["text"] == "Test task"
        assert data["props"]["checked"] is True


class TestProConItemGenerator:
    """Test suite for generate_pro_con_item function."""

    def test_basic_pro_con_item(self):
        """Test creating a basic pros/cons item."""
        reset_id_counter()
        item = generate_pro_con_item(
            title="Remote Work",
            pros=["Flexible schedule", "No commute"],
            cons=["Less interaction", "Isolation"]
        )

        assert item.type == "a2ui.ProConItem"
        assert item.id == "pro-con-item-1"
        assert item.props["title"] == "Remote Work"
        assert len(item.props["pros"]) == 2
        assert len(item.props["cons"]) == 2
        assert "verdict" not in item.props

    def test_pro_con_item_with_verdict(self):
        """Test pros/cons item with verdict."""
        item = generate_pro_con_item(
            title="Electric Vehicle",
            pros=["Lower running costs", "Environmentally friendly"],
            cons=["Higher upfront cost", "Limited charging"],
            verdict="Best for urban commuters with home charging"
        )

        assert item.props["verdict"] == "Best for urban commuters with home charging"

    def test_pro_con_item_single_items(self):
        """Test pros/cons with minimum items (1 each)."""
        item = generate_pro_con_item(
            title="Decision",
            pros=["One pro"],
            cons=["One con"]
        )

        assert len(item.props["pros"]) == 1
        assert len(item.props["cons"]) == 1

    def test_pro_con_item_max_items(self):
        """Test pros/cons with maximum items (10 each)."""
        pros = [f"Pro {i}" for i in range(1, 11)]
        cons = [f"Con {i}" for i in range(1, 11)]

        item = generate_pro_con_item(
            title="Detailed Analysis",
            pros=pros,
            cons=cons
        )

        assert len(item.props["pros"]) == 10
        assert len(item.props["cons"]) == 10

    def test_pro_con_item_realistic_analysis(self):
        """Test pros/cons with realistic content."""
        item = generate_pro_con_item(
            title="GraphQL vs REST",
            pros=[
                "Flexible queries",
                "Single endpoint",
                "Strong typing",
                "No over-fetching"
            ],
            cons=[
                "Steeper learning curve",
                "Query complexity",
                "Caching challenges"
            ],
            verdict="Choose GraphQL for complex data requirements"
        )

        assert item.props["title"] == "GraphQL vs REST"
        assert len(item.props["pros"]) == 4
        assert len(item.props["cons"]) == 3
        assert "verdict" in item.props

    def test_pro_con_item_unbalanced_lists(self):
        """Test pros/cons with different lengths (valid scenario)."""
        item = generate_pro_con_item(
            title="Product X",
            pros=["Great feature 1", "Great feature 2", "Great feature 3"],
            cons=["Minor issue"]
        )

        assert len(item.props["pros"]) == 3
        assert len(item.props["cons"]) == 1

    def test_pro_con_item_empty_title(self):
        """Test that empty title raises error."""
        with pytest.raises(ValueError, match="title cannot be empty"):
            generate_pro_con_item(title="", pros=["Pro"], cons=["Con"])

        with pytest.raises(ValueError, match="title cannot be empty"):
            generate_pro_con_item(title="   ", pros=["Pro"], cons=["Con"])

    def test_pro_con_item_empty_pros(self):
        """Test that empty pros list raises error."""
        with pytest.raises(ValueError, match="requires at least one pro"):
            generate_pro_con_item(title="Test", pros=[], cons=["Con"])

    def test_pro_con_item_empty_cons(self):
        """Test that empty cons list raises error."""
        with pytest.raises(ValueError, match="requires at least one con"):
            generate_pro_con_item(title="Test", pros=["Pro"], cons=[])

    def test_pro_con_item_too_many_pros(self):
        """Test that exceeding 10 pros raises error."""
        pros = [f"Pro {i}" for i in range(1, 12)]
        with pytest.raises(ValueError, match="supports up to 10 pros"):
            generate_pro_con_item(title="Test", pros=pros, cons=["Con"])

    def test_pro_con_item_too_many_cons(self):
        """Test that exceeding 10 cons raises error."""
        cons = [f"Con {i}" for i in range(1, 12)]
        with pytest.raises(ValueError, match="supports up to 10 cons"):
            generate_pro_con_item(title="Test", pros=["Pro"], cons=cons)

    def test_pro_con_item_json_serialization(self):
        """Test that pro/con item can be serialized to JSON."""
        item = generate_pro_con_item(
            title="Test Decision",
            pros=["Pro 1", "Pro 2"],
            cons=["Con 1", "Con 2"],
            verdict="Test verdict"
        )

        json_str = json.dumps(item.model_dump(exclude_none=True))
        data = json.loads(json_str)

        assert data["type"] == "a2ui.ProConItem"
        assert data["props"]["title"] == "Test Decision"
        assert len(data["props"]["pros"]) == 2
        assert len(data["props"]["cons"]) == 2


class TestBulletPointGenerator:
    """Test suite for generate_bullet_point function."""

    def test_basic_bullet_point(self):
        """Test creating a basic bullet point (level 0)."""
        reset_id_counter()
        bullet = generate_bullet_point(text="Main point")

        assert bullet.type == "a2ui.BulletPoint"
        assert bullet.id == "bullet-point-1"
        assert bullet.props["text"] == "Main point"
        assert bullet.props["level"] == 0
        assert bullet.props["highlight"] is False
        assert "icon" not in bullet.props

    def test_bullet_point_nested_levels(self):
        """Test bullet points with all nesting levels (0-3)."""
        reset_id_counter()
        level0 = generate_bullet_point(text="Root level", level=0)
        level1 = generate_bullet_point(text="Level 1 nested", level=1)
        level2 = generate_bullet_point(text="Level 2 nested", level=2)
        level3 = generate_bullet_point(text="Level 3 nested", level=3)

        assert level0.props["level"] == 0
        assert level1.props["level"] == 1
        assert level2.props["level"] == 2
        assert level3.props["level"] == 3

    def test_bullet_point_with_icon(self):
        """Test bullet point with custom icon."""
        bullet = generate_bullet_point(text="Icon bullet", icon="star")
        assert bullet.props["icon"] == "star"

        bullet2 = generate_bullet_point(text="Arrow bullet", icon="arrow", level=1)
        assert bullet2.props["icon"] == "arrow"

    def test_bullet_point_highlighted(self):
        """Test highlighted bullet point."""
        bullet = generate_bullet_point(
            text="Important takeaway",
            highlight=True
        )
        assert bullet.props["highlight"] is True

    def test_bullet_point_all_features(self):
        """Test bullet point with all optional features."""
        bullet = generate_bullet_point(
            text="Important nested point",
            level=2,
            icon="star",
            highlight=True
        )

        assert bullet.props["text"] == "Important nested point"
        assert bullet.props["level"] == 2
        assert bullet.props["icon"] == "star"
        assert bullet.props["highlight"] is True

    def test_bullet_point_various_icons(self):
        """Test bullet points with different icon types."""
        icons = ["circle", "square", "arrow", "star", "check"]
        for icon in icons:
            bullet = generate_bullet_point(text="Test", icon=icon)
            assert bullet.props["icon"] == icon

    def test_bullet_point_hierarchical_list(self):
        """Test creating a hierarchical list structure."""
        reset_id_counter()
        bullets = [
            generate_bullet_point("Main topic 1", level=0),
            generate_bullet_point("Subtopic 1.1", level=1),
            generate_bullet_point("Subtopic 1.2", level=1),
            generate_bullet_point("Detail 1.2.1", level=2),
            generate_bullet_point("Main topic 2", level=0),
            generate_bullet_point("Subtopic 2.1", level=1),
        ]

        assert bullets[0].props["level"] == 0
        assert bullets[1].props["level"] == 1
        assert bullets[3].props["level"] == 2

    def test_bullet_point_text_trimming(self):
        """Test that whitespace in text is trimmed."""
        bullet = generate_bullet_point(text="  Trimmed text  ")
        assert bullet.props["text"] == "Trimmed text"

    def test_bullet_point_empty_text(self):
        """Test that empty text raises error."""
        with pytest.raises(ValueError, match="text cannot be empty"):
            generate_bullet_point(text="")

        with pytest.raises(ValueError, match="text cannot be empty"):
            generate_bullet_point(text="   ")

    def test_bullet_point_invalid_level_negative(self):
        """Test that negative level raises error."""
        with pytest.raises(ValueError, match="Level must be between 0 and 3"):
            generate_bullet_point(text="Test", level=-1)

    def test_bullet_point_invalid_level_too_high(self):
        """Test that level > 3 raises error."""
        with pytest.raises(ValueError, match="Level must be between 0 and 3"):
            generate_bullet_point(text="Test", level=4)

        with pytest.raises(ValueError, match="Level must be between 0 and 3"):
            generate_bullet_point(text="Test", level=10)

    def test_bullet_point_json_serialization(self):
        """Test that bullet point can be serialized to JSON."""
        bullet = generate_bullet_point(
            text="Test bullet",
            level=2,
            icon="arrow",
            highlight=True
        )

        json_str = json.dumps(bullet.model_dump(exclude_none=True))
        data = json.loads(json_str)

        assert data["type"] == "a2ui.BulletPoint"
        assert data["props"]["text"] == "Test bullet"
        assert data["props"]["level"] == 2


class TestListIntegration:
    """Integration tests for list components."""

    def test_top_ai_models_ranking(self):
        """Test creating a complete top AI models ranking."""
        reset_id_counter()
        rankings = [
            generate_ranked_item(
                rank=1,
                title="GPT-4",
                description="Most advanced language model",
                score=9.5,
                icon="trophy"
            ),
            generate_ranked_item(
                rank=2,
                title="Claude 3",
                description="Strong reasoning capabilities",
                score=9.3,
                icon="medal"
            ),
            generate_ranked_item(
                rank=3,
                title="Gemini Pro",
                description="Multimodal capabilities",
                score=9.0,
                icon="medal"
            ),
            generate_ranked_item(
                rank=4,
                title="LLaMA 2",
                description="Open source leader",
                score=8.5
            ),
            generate_ranked_item(
                rank=5,
                title="Mistral",
                description="Efficient and powerful",
                score=8.2
            ),
        ]

        # Verify all components are correct type
        for item in rankings:
            assert item.type == "a2ui.RankedItem"

        # Verify rankings are sequential
        for i, item in enumerate(rankings, 1):
            assert item.props["rank"] == i

        # Verify top 3 have icons
        assert rankings[0].props["icon"] == "trophy"
        assert rankings[1].props["icon"] == "medal"
        assert rankings[2].props["icon"] == "medal"

    def test_project_checklist(self):
        """Test creating a complete project checklist."""
        reset_id_counter()
        checklist = [
            generate_checklist_item(
                text="Set up development environment",
                checked=True,
                priority="high"
            ),
            generate_checklist_item(
                text="Design database schema",
                checked=True,
                priority="high"
            ),
            generate_checklist_item(
                text="Implement authentication",
                checked=False,
                priority="high",
                due_date="2026-02-05"
            ),
            generate_checklist_item(
                text="Write API documentation",
                checked=False,
                priority="medium",
                due_date="2026-02-10"
            ),
            generate_checklist_item(
                text="Add code comments",
                checked=False,
                priority="low",
                due_date="2026-02-15"
            ),
        ]

        # Verify all components
        for item in checklist:
            assert item.type == "a2ui.ChecklistItem"

        # Verify completed items
        assert checklist[0].props["checked"] is True
        assert checklist[1].props["checked"] is True

        # Verify pending high priority items
        assert checklist[2].props["checked"] is False
        assert checklist[2].props["priority"] == "high"

    def test_product_decision_analysis(self):
        """Test creating a product decision with pros/cons."""
        reset_id_counter()
        analysis = generate_pro_con_item(
            title="Should we adopt GraphQL?",
            pros=[
                "Flexible data fetching reduces over-fetching",
                "Single endpoint simplifies API management",
                "Strong typing improves developer experience",
                "Built-in introspection and documentation",
                "Reduces number of API calls needed"
            ],
            cons=[
                "Steeper learning curve for team",
                "Query complexity can impact performance",
                "Caching is more complex than REST",
                "Requires new tooling and infrastructure",
            ],
            verdict="Recommended for new projects with complex data requirements. Consider gradual adoption for existing systems."
        )

        assert analysis.type == "a2ui.ProConItem"
        assert len(analysis.props["pros"]) == 5
        assert len(analysis.props["cons"]) == 4
        assert "verdict" in analysis.props

    def test_hierarchical_outline(self):
        """Test creating a hierarchical outline with bullets."""
        reset_id_counter()
        outline = [
            generate_bullet_point("Introduction", level=0, highlight=True),
            generate_bullet_point("Problem statement", level=1),
            generate_bullet_point("Current challenges", level=2),
            generate_bullet_point("Market opportunity", level=2),
            generate_bullet_point("Proposed solution", level=1),

            generate_bullet_point("Technical Architecture", level=0, highlight=True),
            generate_bullet_point("Frontend layer", level=1),
            generate_bullet_point("React components", level=2),
            generate_bullet_point("State management", level=2),
            generate_bullet_point("Backend layer", level=1),
            generate_bullet_point("API design", level=2),
            generate_bullet_point("Database schema", level=2),

            generate_bullet_point("Implementation Plan", level=0, highlight=True),
            generate_bullet_point("Phase 1: MVP", level=1),
            generate_bullet_point("Core features", level=2),
            generate_bullet_point("Basic UI", level=2),
            generate_bullet_point("Phase 2: Enhancement", level=1),
        ]

        # Verify structure
        assert len(outline) == 17

        # Verify level 0 items are highlighted
        level_0_items = [b for b in outline if b.props["level"] == 0]
        for item in level_0_items:
            assert item.props["highlight"] is True

        # Verify nesting levels are valid (0-3)
        for item in outline:
            assert 0 <= item.props["level"] <= 3

    def test_mixed_list_components(self):
        """Test combining multiple list component types."""
        reset_id_counter()

        # Create a ranked list
        top_frameworks = [
            generate_ranked_item(rank=1, title="React", score=9.2),
            generate_ranked_item(rank=2, title="Vue", score=8.8),
            generate_ranked_item(rank=3, title="Angular", score=8.5),
        ]

        # Create a pros/cons analysis
        react_analysis = generate_pro_con_item(
            title="React Framework",
            pros=["Large ecosystem", "Component reusability", "Strong community"],
            cons=["Learning curve", "Frequent updates"],
            verdict="Best for large-scale applications"
        )

        # Create a checklist
        learning_checklist = [
            generate_checklist_item("Learn JSX syntax", checked=True),
            generate_checklist_item("Understand hooks", checked=False, priority="high"),
            generate_checklist_item("Practice with projects", checked=False),
        ]

        # Create outline
        outline = [
            generate_bullet_point("Getting Started", level=0),
            generate_bullet_point("Install dependencies", level=1),
            generate_bullet_point("Create first component", level=1),
        ]

        # Verify all components
        assert len(top_frameworks) == 3
        assert react_analysis.type == "a2ui.ProConItem"
        assert len(learning_checklist) == 3
        assert len(outline) == 3

    def test_list_json_serialization_batch(self):
        """Test batch JSON serialization of list components."""
        reset_id_counter()

        components = [
            generate_ranked_item(rank=1, title="First"),
            generate_checklist_item(text="Task 1", checked=True),
            generate_pro_con_item(title="Decision", pros=["Pro"], cons=["Con"]),
            generate_bullet_point(text="Point 1", level=0),
        ]

        # Serialize all to JSON
        json_data = [json.loads(json.dumps(c.model_dump(exclude_none=True))) for c in components]

        assert len(json_data) == 4
        assert json_data[0]["type"] == "a2ui.RankedItem"
        assert json_data[1]["type"] == "a2ui.ChecklistItem"
        assert json_data[2]["type"] == "a2ui.ProConItem"
        assert json_data[3]["type"] == "a2ui.BulletPoint"


class TestResourceGenerators:
    """Test suite for resource component generators (LinkCard, ToolCard, BookCard, RepoCard)."""

    def test_extract_domain_basic(self):
        """Test basic domain extraction."""
        assert extract_domain("https://example.com/path") == "example.com"
        assert extract_domain("http://example.com") == "example.com"
        assert extract_domain("https://www.github.com/user/repo") == "github.com"

    def test_extract_domain_with_subdomain(self):
        """Test domain extraction with subdomains."""
        assert extract_domain("https://api.example.com/endpoint") == "api.example.com"
        assert extract_domain("https://subdomain.example.com:8080/page") == "subdomain.example.com"

    def test_extract_domain_removes_www(self):
        """Test that www. prefix is removed."""
        assert extract_domain("https://www.example.com") == "example.com"
        assert extract_domain("http://www.test.org/page") == "test.org"

    def test_extract_domain_invalid_url(self):
        """Test domain extraction with invalid URLs."""
        with pytest.raises(ValueError, match="URL must start with http"):
            extract_domain("example.com")

        with pytest.raises(ValueError, match="URL cannot be empty"):
            extract_domain("")

        with pytest.raises(ValueError, match="Could not extract domain"):
            extract_domain("http://")

    def test_extract_github_repo_info_from_url(self):
        """Test GitHub repo info extraction from URLs."""
        result = extract_github_repo_info("https://github.com/facebook/react")
        assert result["owner"] == "facebook"
        assert result["repo"] == "react"
        assert result["url"] == "https://github.com/facebook/react"

    def test_extract_github_repo_info_from_owner_repo(self):
        """Test GitHub repo info extraction from owner/repo format."""
        result = extract_github_repo_info("torvalds/linux")
        assert result["owner"] == "torvalds"
        assert result["repo"] == "linux"
        assert result["url"] == "https://github.com/torvalds/linux"

    def test_extract_github_repo_info_various_formats(self):
        """Test various GitHub URL formats."""
        # Without https://
        result = extract_github_repo_info("github.com/microsoft/vscode")
        assert result["owner"] == "microsoft"
        assert result["repo"] == "vscode"

        # With .git suffix
        result = extract_github_repo_info("https://github.com/tensorflow/tensorflow.git")
        assert result["owner"] == "tensorflow"
        assert result["repo"] == "tensorflow"

    def test_extract_github_repo_info_invalid(self):
        """Test GitHub repo info extraction with invalid input."""
        with pytest.raises(ValueError, match="Invalid GitHub URL"):
            extract_github_repo_info("not-a-github-url")

        with pytest.raises(ValueError, match="cannot be empty"):
            extract_github_repo_info("")

    def test_generate_link_card_basic(self):
        """Test basic link card generation."""
        reset_id_counter()
        card = generate_link_card(
            title="React Documentation",
            url="https://react.dev/learn"
        )

        assert card.type == "a2ui.LinkCard"
        assert card.props["title"] == "React Documentation"
        assert card.props["url"] == "https://react.dev/learn"
        assert card.props["domain"] == "react.dev"

    def test_generate_link_card_with_all_fields(self):
        """Test link card with all optional fields."""
        reset_id_counter()
        card = generate_link_card(
            title="Introduction to Machine Learning",
            url="https://example.com/ml-intro",
            description="Comprehensive guide to ML fundamentals",
            domain="example.com",
            image_url="https://example.com/ml-preview.jpg",
            tags=["machine-learning", "tutorial", "beginner"]
        )

        assert card.type == "a2ui.LinkCard"
        assert card.props["title"] == "Introduction to Machine Learning"
        assert card.props["url"] == "https://example.com/ml-intro"
        assert card.props["description"] == "Comprehensive guide to ML fundamentals"
        assert card.props["domain"] == "example.com"
        assert card.props["imageUrl"] == "https://example.com/ml-preview.jpg"
        assert card.props["tags"] == ["machine-learning", "tutorial", "beginner"]

    def test_generate_link_card_auto_domain_extraction(self):
        """Test automatic domain extraction in link cards."""
        card = generate_link_card(
            title="GitHub",
            url="https://www.github.com/features"
        )

        assert card.props["domain"] == "github.com"  # www. removed

    def test_generate_link_card_invalid_url(self):
        """Test link card with invalid URL."""
        with pytest.raises(ValueError, match="URL must start with http"):
            generate_link_card(
                title="Test",
                url="example.com"
            )

    def test_generate_link_card_too_many_tags(self):
        """Test link card with too many tags."""
        with pytest.raises(ValueError, match="supports up to 5 tags"):
            generate_link_card(
                title="Test",
                url="https://example.com",
                tags=["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"]
            )

    def test_generate_tool_card_basic(self):
        """Test basic tool card generation."""
        reset_id_counter()
        card = generate_tool_card(
            name="VS Code",
            description="Free code editor from Microsoft",
            url="https://code.visualstudio.com"
        )

        assert card.type == "a2ui.ToolCard"
        assert card.props["name"] == "VS Code"
        assert card.props["description"] == "Free code editor from Microsoft"
        assert card.props["url"] == "https://code.visualstudio.com"

    def test_generate_tool_card_with_all_fields(self):
        """Test tool card with all optional fields."""
        reset_id_counter()
        card = generate_tool_card(
            name="Figma",
            description="Collaborative interface design tool",
            url="https://www.figma.com",
            category="design",
            pricing="freemium",
            icon_url="https://www.figma.com/favicon.ico",
            features=["Real-time collaboration", "Prototyping", "Design systems"]
        )

        assert card.type == "a2ui.ToolCard"
        assert card.props["name"] == "Figma"
        assert card.props["description"] == "Collaborative interface design tool"
        assert card.props["url"] == "https://www.figma.com"
        assert card.props["category"] == "design"
        assert card.props["pricing"] == "freemium"
        assert card.props["iconUrl"] == "https://www.figma.com/favicon.ico"
        assert card.props["features"] == ["Real-time collaboration", "Prototyping", "Design systems"]

    def test_generate_tool_card_invalid_pricing(self):
        """Test tool card with invalid pricing value."""
        with pytest.raises(ValueError, match="Invalid pricing"):
            generate_tool_card(
                name="Test Tool",
                description="Test",
                url="https://example.com",
                pricing="expensive"
            )

    def test_generate_tool_card_too_many_features(self):
        """Test tool card with too many features."""
        with pytest.raises(ValueError, match="supports up to 5 features"):
            generate_tool_card(
                name="Test Tool",
                description="Test",
                url="https://example.com",
                features=["f1", "f2", "f3", "f4", "f5", "f6"]
            )

    def test_generate_book_card_basic(self):
        """Test basic book card generation."""
        reset_id_counter()
        card = generate_book_card(
            title="Clean Code",
            author="Robert C. Martin"
        )

        assert card.type == "a2ui.BookCard"
        assert card.props["title"] == "Clean Code"
        assert card.props["author"] == "Robert C. Martin"

    def test_generate_book_card_with_all_fields(self):
        """Test book card with all optional fields."""
        reset_id_counter()
        card = generate_book_card(
            title="The Pragmatic Programmer",
            author="Andrew Hunt, David Thomas",
            year=2019,
            isbn="978-0-13-595705-9",
            url="https://pragprog.com/titles/tpp20/",
            cover_image_url="https://pragprog.com/titles/tpp20/tpp20.jpg",
            rating=4.5,
            description="Your journey to mastery"
        )

        assert card.type == "a2ui.BookCard"
        assert card.props["title"] == "The Pragmatic Programmer"
        assert card.props["author"] == "Andrew Hunt, David Thomas"
        assert card.props["year"] == 2019
        assert card.props["isbn"] == "978-0-13-595705-9"
        assert card.props["url"] == "https://pragprog.com/titles/tpp20/"
        assert card.props["coverImageUrl"] == "https://pragprog.com/titles/tpp20/tpp20.jpg"
        assert card.props["rating"] == 4.5
        assert card.props["description"] == "Your journey to mastery"

    def test_generate_book_card_isbn_validation(self):
        """Test ISBN validation in book cards."""
        # Valid ISBN-10
        card = generate_book_card(
            title="Test Book",
            author="Test Author",
            isbn="0-13-595705-9"
        )
        assert card.props["isbn"] == "0-13-595705-9"

        # Valid ISBN-13
        card = generate_book_card(
            title="Test Book",
            author="Test Author",
            isbn="9780135957059"
        )
        assert card.props["isbn"] == "9780135957059"

        # Invalid ISBN (wrong length)
        with pytest.raises(ValueError, match="Invalid ISBN format"):
            generate_book_card(
                title="Test Book",
                author="Test Author",
                isbn="12345"
            )

        # Invalid ISBN (non-digits)
        with pytest.raises(ValueError, match="Invalid ISBN format"):
            generate_book_card(
                title="Test Book",
                author="Test Author",
                isbn="ABC-1234567890"
            )

    def test_generate_book_card_rating_validation(self):
        """Test rating validation in book cards."""
        # Valid rating
        card = generate_book_card(
            title="Test Book",
            author="Test Author",
            rating=4.5
        )
        assert card.props["rating"] == 4.5

        # Rating too high
        with pytest.raises(ValueError, match="Rating must be between 0 and 5"):
            generate_book_card(
                title="Test Book",
                author="Test Author",
                rating=6.0
            )

        # Negative rating
        with pytest.raises(ValueError, match="Rating must be between 0 and 5"):
            generate_book_card(
                title="Test Book",
                author="Test Author",
                rating=-1.0
            )

    def test_generate_repo_card_from_url(self):
        """Test repo card generation from GitHub URL."""
        reset_id_counter()
        card = generate_repo_card(
            name="react",
            repo_url="https://github.com/facebook/react"
        )

        assert card.type == "a2ui.RepoCard"
        assert card.props["name"] == "react"
        assert card.props["owner"] == "facebook"
        assert card.props["repoUrl"] == "https://github.com/facebook/react"

    def test_generate_repo_card_from_owner_name(self):
        """Test repo card generation from owner and name."""
        reset_id_counter()
        card = generate_repo_card(
            name="tensorflow",
            owner="tensorflow"
        )

        assert card.type == "a2ui.RepoCard"
        assert card.props["name"] == "tensorflow"
        assert card.props["owner"] == "tensorflow"
        assert card.props["repoUrl"] == "https://github.com/tensorflow/tensorflow"

    def test_generate_repo_card_with_all_fields(self):
        """Test repo card with all optional fields."""
        reset_id_counter()
        card = generate_repo_card(
            name="vscode",
            owner="microsoft",
            description="Visual Studio Code",
            language="TypeScript",
            stars=150000,
            fork_count=26000,
            topics=["editor", "typescript", "electron"]
        )

        assert card.type == "a2ui.RepoCard"
        assert card.props["name"] == "vscode"
        assert card.props["owner"] == "microsoft"
        assert card.props["description"] == "Visual Studio Code"
        assert card.props["language"] == "TypeScript"
        assert card.props["stars"] == 150000
        assert card.props["forkCount"] == 26000
        assert card.props["topics"] == ["editor", "typescript", "electron"]

    def test_generate_repo_card_owner_repo_format(self):
        """Test repo card with owner/repo format in URL."""
        card = generate_repo_card(
            name="linux",
            repo_url="torvalds/linux"
        )

        assert card.props["owner"] == "torvalds"
        assert card.props["repoUrl"] == "https://github.com/torvalds/linux"

    def test_generate_repo_card_missing_required_info(self):
        """Test repo card with missing required information."""
        with pytest.raises(ValueError, match="requires either repo_url or both owner and name"):
            generate_repo_card(name="test-repo")

    def test_generate_repo_card_negative_stats(self):
        """Test repo card with negative stats."""
        with pytest.raises(ValueError, match="Star count cannot be negative"):
            generate_repo_card(
                name="test",
                owner="test",
                stars=-100
            )

        with pytest.raises(ValueError, match="Fork count cannot be negative"):
            generate_repo_card(
                name="test",
                owner="test",
                fork_count=-50
            )

    def test_generate_repo_card_too_many_topics(self):
        """Test repo card with too many topics."""
        with pytest.raises(ValueError, match="supports up to 5 topics"):
            generate_repo_card(
                name="test",
                owner="test",
                topics=["t1", "t2", "t3", "t4", "t5", "t6"]
            )

    def test_resource_integration_mixed_collection(self):
        """Test integration: create a mixed resource collection."""
        reset_id_counter()

        # Create a collection of different resource types
        resources = [
            generate_link_card(
                title="React Documentation",
                url="https://react.dev",
                description="Official React documentation",
                tags=["react", "javascript", "docs"]
            ),
            generate_tool_card(
                name="VS Code",
                description="Code editor",
                url="https://code.visualstudio.com",
                category="ide",
                pricing="free"
            ),
            generate_book_card(
                title="Clean Code",
                author="Robert C. Martin",
                rating=4.5
            ),
            generate_repo_card(
                name="react",
                repo_url="https://github.com/facebook/react",
                description="A JavaScript library for building user interfaces",
                language="JavaScript",
                stars=220000
            ),
        ]

        # Verify all components created correctly
        assert len(resources) == 4
        assert resources[0].type == "a2ui.LinkCard"
        assert resources[1].type == "a2ui.ToolCard"
        assert resources[2].type == "a2ui.BookCard"
        assert resources[3].type == "a2ui.RepoCard"

        # Verify unique IDs
        ids = [r.id for r in resources]
        assert len(ids) == len(set(ids))  # All unique

    def test_resource_json_serialization(self):
        """Test JSON serialization of all resource components."""
        reset_id_counter()

        link = generate_link_card("Test Link", "https://example.com")
        tool = generate_tool_card("Test Tool", "Description", "https://example.com")
        book = generate_book_card("Test Book", "Test Author")
        repo = generate_repo_card("test-repo", owner="test-owner")

        # Serialize to JSON
        link_json = json.loads(json.dumps(link.model_dump(exclude_none=True)))
        tool_json = json.loads(json.dumps(tool.model_dump(exclude_none=True)))
        book_json = json.loads(json.dumps(book.model_dump(exclude_none=True)))
        repo_json = json.loads(json.dumps(repo.model_dump(exclude_none=True)))

        # Verify types in JSON
        assert link_json["type"] == "a2ui.LinkCard"
        assert tool_json["type"] == "a2ui.ToolCard"
        assert book_json["type"] == "a2ui.BookCard"
        assert repo_json["type"] == "a2ui.RepoCard"

    def test_resource_learning_path(self):
        """Test integration: create a complete learning resource path."""
        reset_id_counter()

        learning_resources = {
            "documentation": generate_link_card(
                title="TypeScript Handbook",
                url="https://www.typescriptlang.org/docs/",
                description="Official TypeScript documentation",
                tags=["typescript", "documentation", "reference"]
            ),
            "tutorial": generate_link_card(
                title="TypeScript Deep Dive",
                url="https://basarat.gitbook.io/typescript/",
                description="Complete TypeScript guide",
                tags=["typescript", "tutorial", "book"]
            ),
            "book": generate_book_card(
                title="Programming TypeScript",
                author="Boris Cherny",
                year=2019,
                rating=4.3,
                description="Making Your JavaScript Applications Scale"
            ),
            "repository": generate_repo_card(
                name="typescript",
                owner="microsoft",
                description="TypeScript is a superset of JavaScript",
                language="TypeScript",
                stars=95000,
                topics=["typescript", "javascript", "compiler"]
            ),
            "tool": generate_tool_card(
                name="TS Playground",
                description="Online TypeScript compiler and sandbox",
                url="https://www.typescriptlang.org/play",
                category="ide",
                pricing="free",
                features=["Instant compilation", "Share code", "Type checking"]
            ),
        }

        # Verify complete learning path
        assert len(learning_resources) == 5
        assert learning_resources["documentation"].props["title"] == "TypeScript Handbook"
        assert learning_resources["book"].props["author"] == "Boris Cherny"
        assert learning_resources["repository"].props["stars"] == 95000
        assert learning_resources["tool"].props["pricing"] == "free"

    def test_resource_tech_stack_collection(self):
        """Test integration: create a tech stack resource collection."""
        reset_id_counter()

        tech_stack = [
            # Frontend tools
            generate_tool_card(
                name="React",
                description="JavaScript library for building UIs",
                url="https://react.dev",
                category="frontend",
                pricing="free"
            ),
            generate_repo_card(
                name="react",
                owner="facebook",
                language="JavaScript",
                stars=220000
            ),
            # Backend tools
            generate_tool_card(
                name="Node.js",
                description="JavaScript runtime",
                url="https://nodejs.org",
                category="backend",
                pricing="free"
            ),
            generate_link_card(
                title="Node.js Best Practices",
                url="https://github.com/goldbergyoni/nodebestpractices",
                description="Comprehensive guide to Node.js best practices",
                tags=["nodejs", "best-practices", "guide"]
            ),
            # Learning resources
            generate_book_card(
                title="You Don't Know JS",
                author="Kyle Simpson",
                rating=4.7,
                description="Book series on JavaScript"
            ),
        ]

        # Verify tech stack
        assert len(tech_stack) == 5
        assert sum(1 for r in tech_stack if r.type == "a2ui.ToolCard") == 2
        assert sum(1 for r in tech_stack if r.type == "a2ui.RepoCard") == 1
        assert sum(1 for r in tech_stack if r.type == "a2ui.LinkCard") == 1
        assert sum(1 for r in tech_stack if r.type == "a2ui.BookCard") == 1

    def test_resource_batch_generation(self):
        """Test batch generation of resource components."""
        reset_id_counter()

        # Create multiple resources in batch style
        repos = [
            generate_repo_card(name="react", owner="facebook", stars=220000),
            generate_repo_card(name="vue", owner="vuejs", stars=205000),
            generate_repo_card(name="angular", repo_url="angular/angular", stars=92000),
        ]

        books = [
            generate_book_card("Clean Code", "Robert C. Martin", rating=4.5),
            generate_book_card("The Pragmatic Programmer", "Hunt & Thomas", rating=4.4),
            generate_book_card("Design Patterns", "Gang of Four", rating=4.6),
        ]

        # Verify batch creation
        assert len(repos) == 3
        assert len(books) == 3
        assert all(r.type == "a2ui.RepoCard" for r in repos)
        assert all(b.type == "a2ui.BookCard" for b in books)

        # Verify stars are sorted
        repo_stars = [r.props["stars"] for r in repos]
        assert repo_stars == [220000, 205000, 92000]


class TestPeopleComponentGenerators:
    """Test suite for people component generators (ProfileCard, CompanyCard, QuoteCard, ExpertTip)."""

    # ProfileCard Tests

    def test_generate_profile_card_basic(self):
        """Test generating a basic profile card with required fields only."""
        reset_id_counter()

        card = generate_profile_card(
            name="Jane Smith",
            title="AI Researcher"
        )

        assert card.type == "a2ui.ProfileCard"
        assert card.id == "profile-card-1"
        assert card.props["name"] == "Jane Smith"
        assert card.props["title"] == "AI Researcher"
        assert "bio" not in card.props
        assert "avatarUrl" not in card.props
        assert "contact" not in card.props
        assert "socialLinks" not in card.props

    def test_generate_profile_card_with_bio_and_avatar(self):
        """Test generating a profile card with bio and avatar."""
        reset_id_counter()

        card = generate_profile_card(
            name="Dr. John Doe",
            title="Chief Technology Officer",
            bio="20+ years building scalable systems",
            avatar_url="https://example.com/avatar.jpg"
        )

        assert card.type == "a2ui.ProfileCard"
        assert card.props["name"] == "Dr. John Doe"
        assert card.props["title"] == "Chief Technology Officer"
        assert card.props["bio"] == "20+ years building scalable systems"
        assert card.props["avatarUrl"] == "https://example.com/avatar.jpg"

    def test_generate_profile_card_with_contact(self):
        """Test generating a profile card with contact information."""
        reset_id_counter()

        card = generate_profile_card(
            name="Alice Johnson",
            title="Senior Engineer",
            contact={
                "email": "alice@example.com",
                "phone": "+1-555-0100",
                "location": "San Francisco, CA"
            }
        )

        assert card.type == "a2ui.ProfileCard"
        assert card.props["contact"]["email"] == "alice@example.com"
        assert card.props["contact"]["phone"] == "+1-555-0100"
        assert card.props["contact"]["location"] == "San Francisco, CA"

    def test_generate_profile_card_with_social_links(self):
        """Test generating a profile card with social media links."""
        reset_id_counter()

        social_links = [
            {"platform": "twitter", "url": "https://twitter.com/johndoe"},
            {"platform": "linkedin", "url": "https://linkedin.com/in/johndoe"},
            {"platform": "github", "url": "https://github.com/johndoe"}
        ]

        card = generate_profile_card(
            name="John Doe",
            title="Software Developer",
            social_links=social_links
        )

        assert card.type == "a2ui.ProfileCard"
        assert len(card.props["socialLinks"]) == 3
        assert card.props["socialLinks"][0]["platform"] == "twitter"
        assert card.props["socialLinks"][0]["url"] == "https://twitter.com/johndoe"
        assert card.props["socialLinks"][1]["platform"] == "linkedin"
        assert card.props["socialLinks"][2]["platform"] == "github"

    def test_generate_profile_card_all_features(self):
        """Test generating a profile card with all features."""
        reset_id_counter()

        card = generate_profile_card(
            name="Dr. Sarah Chen",
            title="Machine Learning Researcher",
            bio="Expert in NLP and computer vision with 15 years experience",
            avatar_url="https://example.com/sarah.jpg",
            contact={
                "email": "sarah@university.edu",
                "location": "Cambridge, MA"
            },
            social_links=[
                {"platform": "twitter", "url": "https://twitter.com/sarahchen"},
                {"platform": "linkedin", "url": "https://linkedin.com/in/sarahchen"},
                {"platform": "github", "url": "https://github.com/sarahchen"},
                {"platform": "website", "url": "https://sarahchen.com"}
            ]
        )

        assert card.type == "a2ui.ProfileCard"
        assert card.props["name"] == "Dr. Sarah Chen"
        assert card.props["title"] == "Machine Learning Researcher"
        assert "bio" in card.props
        assert "avatarUrl" in card.props
        assert "contact" in card.props
        assert len(card.props["socialLinks"]) == 4

    def test_generate_profile_card_invalid_email(self):
        """Test that invalid email format raises error."""
        with pytest.raises(ValueError, match="Invalid email format"):
            generate_profile_card(
                name="Test User",
                title="Developer",
                contact={"email": "invalid-email"}
            )

    def test_generate_profile_card_too_many_social_links(self):
        """Test that more than 5 social links raises error."""
        social_links = [
            {"platform": f"platform{i}", "url": f"https://example.com/{i}"}
            for i in range(6)
        ]

        with pytest.raises(ValueError, match="supports up to 5 social links"):
            generate_profile_card(
                name="Test User",
                title="Developer",
                social_links=social_links
            )

    def test_generate_profile_card_missing_social_link_keys(self):
        """Test that social links without required keys raise error."""
        # Missing 'platform'
        with pytest.raises(ValueError, match="missing required key: 'platform'"):
            generate_profile_card(
                name="Test User",
                title="Developer",
                social_links=[{"url": "https://example.com"}]
            )

        # Missing 'url'
        with pytest.raises(ValueError, match="missing required key: 'url'"):
            generate_profile_card(
                name="Test User",
                title="Developer",
                social_links=[{"platform": "twitter"}]
            )

    def test_generate_profile_card_empty_name(self):
        """Test that empty name raises error."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            generate_profile_card(name="", title="Developer")

    def test_generate_profile_card_empty_title(self):
        """Test that empty title raises error."""
        with pytest.raises(ValueError, match="title cannot be empty"):
            generate_profile_card(name="Test User", title="")

    # CompanyCard Tests

    def test_generate_company_card_basic(self):
        """Test generating a basic company card with required fields only."""
        reset_id_counter()

        card = generate_company_card(
            name="Acme Corp",
            description="Leading provider of innovative solutions"
        )

        assert card.type == "a2ui.CompanyCard"
        assert card.id == "company-card-1"
        assert card.props["name"] == "Acme Corp"
        assert card.props["description"] == "Leading provider of innovative solutions"
        assert "logoUrl" not in card.props
        assert "website" not in card.props
        assert "headquarters" not in card.props
        assert "foundedYear" not in card.props
        assert "employeeCount" not in card.props
        assert "industries" not in card.props

    def test_generate_company_card_with_website(self):
        """Test generating a company card with website URL."""
        reset_id_counter()

        card = generate_company_card(
            name="TechStart Inc.",
            description="AI-powered analytics platform",
            website="https://techstart.com"
        )

        assert card.type == "a2ui.CompanyCard"
        assert card.props["website"] == "https://techstart.com"

    def test_generate_company_card_all_features(self):
        """Test generating a company card with all features."""
        reset_id_counter()

        card = generate_company_card(
            name="Innovation Labs",
            description="Building the future of AI",
            logo_url="https://example.com/logo.png",
            website="https://innovationlabs.com",
            headquarters="San Francisco, CA",
            founded_year=2015,
            employee_count="100-500",
            industries=["Technology", "Artificial Intelligence", "Analytics"]
        )

        assert card.type == "a2ui.CompanyCard"
        assert card.props["name"] == "Innovation Labs"
        assert card.props["description"] == "Building the future of AI"
        assert card.props["logoUrl"] == "https://example.com/logo.png"
        assert card.props["website"] == "https://innovationlabs.com"
        assert card.props["headquarters"] == "San Francisco, CA"
        assert card.props["foundedYear"] == 2015
        assert card.props["employeeCount"] == "100-500"
        assert len(card.props["industries"]) == 3
        assert "Technology" in card.props["industries"]

    def test_generate_company_card_invalid_website_url(self):
        """Test that invalid website URL format raises error."""
        with pytest.raises(ValueError, match="must start with http:// or https://"):
            generate_company_card(
                name="Test Corp",
                description="Test company",
                website="invalid-url"
            )

    def test_generate_company_card_invalid_founded_year(self):
        """Test that invalid founded year raises error."""
        # Year too early
        with pytest.raises(ValueError, match="must be between 1800 and"):
            generate_company_card(
                name="Test Corp",
                description="Test company",
                founded_year=1700
            )

        # Year in future
        with pytest.raises(ValueError, match="must be between 1800 and"):
            generate_company_card(
                name="Test Corp",
                description="Test company",
                founded_year=2100
            )

    def test_generate_company_card_too_many_industries(self):
        """Test that more than 5 industries raises error."""
        industries = [f"Industry {i}" for i in range(6)]

        with pytest.raises(ValueError, match="supports up to 5 industries"):
            generate_company_card(
                name="Test Corp",
                description="Test company",
                industries=industries
            )

    def test_generate_company_card_empty_name(self):
        """Test that empty name raises error."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            generate_company_card(name="", description="Test company")

    def test_generate_company_card_empty_description(self):
        """Test that empty description raises error."""
        with pytest.raises(ValueError, match="description cannot be empty"):
            generate_company_card(name="Test Corp", description="")

    # QuoteCard Tests

    def test_generate_quote_card_basic(self):
        """Test generating a basic quote card with required fields only."""
        reset_id_counter()

        card = generate_quote_card(
            text="The best way to predict the future is to invent it.",
            author="Alan Kay"
        )

        assert card.type == "a2ui.QuoteCard"
        assert card.id == "quote-card-1"
        assert card.props["text"] == "The best way to predict the future is to invent it."
        assert card.props["author"] == "Alan Kay"
        assert card.props["highlight"] == False
        assert "source" not in card.props

    def test_generate_quote_card_with_source(self):
        """Test generating a quote card with source."""
        reset_id_counter()

        card = generate_quote_card(
            text="Stay hungry, stay foolish.",
            author="Steve Jobs",
            source="Stanford Commencement Speech, 2005"
        )

        assert card.type == "a2ui.QuoteCard"
        assert card.props["text"] == "Stay hungry, stay foolish."
        assert card.props["author"] == "Steve Jobs"
        assert card.props["source"] == "Stanford Commencement Speech, 2005"

    def test_generate_quote_card_highlighted(self):
        """Test generating a highlighted quote card."""
        reset_id_counter()

        card = generate_quote_card(
            text="Innovation distinguishes between a leader and a follower.",
            author="Steve Jobs",
            highlight=True
        )

        assert card.type == "a2ui.QuoteCard"
        assert card.props["highlight"] == True

    def test_generate_quote_card_long_quote(self):
        """Test generating a quote card with long text (under 500 chars)."""
        reset_id_counter()

        long_text = "A" * 400  # 400 characters

        card = generate_quote_card(
            text=long_text,
            author="Test Author"
        )

        assert card.type == "a2ui.QuoteCard"
        assert len(card.props["text"]) == 400

    def test_generate_quote_card_empty_text(self):
        """Test that empty text raises error."""
        with pytest.raises(ValueError, match="text cannot be empty"):
            generate_quote_card(text="", author="Test Author")

    def test_generate_quote_card_text_too_long(self):
        """Test that text exceeding 500 characters raises error."""
        long_text = "A" * 501  # 501 characters

        with pytest.raises(ValueError, match="must be 500 characters or less"):
            generate_quote_card(text=long_text, author="Test Author")

    def test_generate_quote_card_empty_author(self):
        """Test that empty author raises error."""
        with pytest.raises(ValueError, match="author cannot be empty"):
            generate_quote_card(text="Test quote", author="")

    # ExpertTip Tests

    def test_generate_expert_tip_basic(self):
        """Test generating a basic expert tip with required fields only."""
        reset_id_counter()

        tip = generate_expert_tip(
            title="Use Async/Await",
            content="Always use async/await instead of callbacks for cleaner code"
        )

        assert tip.type == "a2ui.ExpertTip"
        assert tip.id == "expert-tip-1"
        assert tip.props["title"] == "Use Async/Await"
        assert tip.props["content"] == "Always use async/await instead of callbacks for cleaner code"
        assert "expertName" not in tip.props
        assert "difficulty" not in tip.props
        assert "category" not in tip.props

    def test_generate_expert_tip_with_expert_name(self):
        """Test generating an expert tip with expert name."""
        reset_id_counter()

        tip = generate_expert_tip(
            title="Optimize React Performance",
            content="Use React.memo() to prevent unnecessary re-renders",
            expert_name="Sarah Johnson"
        )

        assert tip.type == "a2ui.ExpertTip"
        assert tip.props["expertName"] == "Sarah Johnson"

    def test_generate_expert_tip_with_difficulty_beginner(self):
        """Test generating a beginner expert tip."""
        reset_id_counter()

        tip = generate_expert_tip(
            title="Git Commit Messages",
            content="Write clear, descriptive commit messages in present tense",
            difficulty="beginner"
        )

        assert tip.type == "a2ui.ExpertTip"
        assert tip.props["difficulty"] == "beginner"

    def test_generate_expert_tip_with_difficulty_intermediate(self):
        """Test generating an intermediate expert tip."""
        reset_id_counter()

        tip = generate_expert_tip(
            title="Database Indexing",
            content="Create indexes on columns used in WHERE clauses",
            difficulty="intermediate"
        )

        assert tip.type == "a2ui.ExpertTip"
        assert tip.props["difficulty"] == "intermediate"

    def test_generate_expert_tip_with_difficulty_advanced(self):
        """Test generating an advanced expert tip."""
        reset_id_counter()

        tip = generate_expert_tip(
            title="Distributed Systems",
            content="Use eventual consistency for high availability",
            difficulty="advanced"
        )

        assert tip.type == "a2ui.ExpertTip"
        assert tip.props["difficulty"] == "advanced"

    def test_generate_expert_tip_with_category(self):
        """Test generating an expert tip with category."""
        reset_id_counter()

        tip = generate_expert_tip(
            title="Design System",
            content="Establish a consistent design system early",
            category="design"
        )

        assert tip.type == "a2ui.ExpertTip"
        assert tip.props["category"] == "design"

    def test_generate_expert_tip_all_features(self):
        """Test generating an expert tip with all features."""
        reset_id_counter()

        tip = generate_expert_tip(
            title="Microservices Architecture",
            content="Use API gateways to manage service communication",
            expert_name="John Smith",
            difficulty="advanced",
            category="development"
        )

        assert tip.type == "a2ui.ExpertTip"
        assert tip.props["title"] == "Microservices Architecture"
        assert tip.props["content"] == "Use API gateways to manage service communication"
        assert tip.props["expertName"] == "John Smith"
        assert tip.props["difficulty"] == "advanced"
        assert tip.props["category"] == "development"

    def test_generate_expert_tip_invalid_difficulty(self):
        """Test that invalid difficulty raises error."""
        with pytest.raises(ValueError, match="Invalid difficulty"):
            generate_expert_tip(
                title="Test Tip",
                content="Test content",
                difficulty="expert"  # Invalid, should be beginner/intermediate/advanced
            )

    def test_generate_expert_tip_empty_title(self):
        """Test that empty title raises error."""
        with pytest.raises(ValueError, match="title cannot be empty"):
            generate_expert_tip(title="", content="Test content")

    def test_generate_expert_tip_empty_content(self):
        """Test that empty content raises error."""
        with pytest.raises(ValueError, match="content cannot be empty"):
            generate_expert_tip(title="Test Tip", content="")

    # Integration Tests

    def test_people_integration_team_page(self):
        """Test integration: generating a team page with profiles."""
        reset_id_counter()

        team = [
            generate_profile_card(
                name="Alice Chen",
                title="CEO & Founder",
                bio="Serial entrepreneur with 3 successful exits",
                avatar_url="https://example.com/alice.jpg",
                social_links=[
                    {"platform": "linkedin", "url": "https://linkedin.com/in/alicechen"},
                    {"platform": "twitter", "url": "https://twitter.com/alicechen"}
                ]
            ),
            generate_profile_card(
                name="Bob Martinez",
                title="CTO",
                bio="Former Google engineer, AI expert",
                avatar_url="https://example.com/bob.jpg",
                contact={"email": "bob@company.com"}
            ),
            generate_profile_card(
                name="Carol Kim",
                title="Head of Design",
                bio="Award-winning product designer"
            )
        ]

        # Verify team structure
        assert len(team) == 3
        assert all(p.type == "a2ui.ProfileCard" for p in team)
        assert team[0].props["name"] == "Alice Chen"
        assert team[1].props["name"] == "Bob Martinez"
        assert team[2].props["name"] == "Carol Kim"
        assert "socialLinks" in team[0].props
        assert "contact" in team[1].props

    def test_people_integration_testimonials_page(self):
        """Test integration: generating a testimonials page with quotes."""
        reset_id_counter()

        testimonials = [
            generate_quote_card(
                text="This product transformed our workflow completely. Highly recommended!",
                author="Jane Smith",
                source="TechCrunch Review",
                highlight=True
            ),
            generate_quote_card(
                text="Best decision we made this year. The ROI was immediate.",
                author="John Doe",
                source="CEO, Acme Corp"
            ),
            generate_quote_card(
                text="Outstanding support team and incredible features.",
                author="Sarah Johnson",
                source="Product Hunt"
            )
        ]

        # Verify testimonials
        assert len(testimonials) == 3
        assert all(q.type == "a2ui.QuoteCard" for q in testimonials)
        assert testimonials[0].props["highlight"] == True
        assert testimonials[1].props["highlight"] == False
        assert all("author" in q.props for q in testimonials)
        assert all("source" in q.props for q in testimonials)

    def test_people_integration_company_directory(self):
        """Test integration: generating a company directory."""
        reset_id_counter()

        companies = [
            generate_company_card(
                name="TechCorp Inc.",
                description="Leading AI solutions provider",
                website="https://techcorp.com",
                headquarters="San Francisco, CA",
                founded_year=2015,
                employee_count="500-1000",
                industries=["Technology", "AI", "Cloud Computing"]
            ),
            generate_company_card(
                name="DataSystems Ltd.",
                description="Enterprise data analytics platform",
                founded_year=2018,
                employee_count="100-500",
                industries=["Analytics", "Big Data"]
            ),
            generate_company_card(
                name="CloudStart",
                description="Startup focused on cloud infrastructure"
            )
        ]

        # Verify company directory
        assert len(companies) == 3
        assert all(c.type == "a2ui.CompanyCard" for c in companies)
        assert companies[0].props["foundedYear"] == 2015
        assert companies[1].props["foundedYear"] == 2018
        assert "industries" in companies[0].props
        assert len(companies[0].props["industries"]) == 3

    def test_people_integration_expert_tips_page(self):
        """Test integration: generating an expert tips page."""
        reset_id_counter()

        tips = [
            generate_expert_tip(
                title="Version Control Best Practices",
                content="Always create feature branches and use pull requests",
                expert_name="Alice Chen",
                difficulty="beginner",
                category="development"
            ),
            generate_expert_tip(
                title="API Design Principles",
                content="Use RESTful conventions and versioning from the start",
                expert_name="Bob Martinez",
                difficulty="intermediate",
                category="development"
            ),
            generate_expert_tip(
                title="System Architecture Patterns",
                content="Consider event-driven architecture for scalability",
                expert_name="Carol Kim",
                difficulty="advanced",
                category="architecture"
            )
        ]

        # Verify tips structure
        assert len(tips) == 3
        assert all(t.type == "a2ui.ExpertTip" for t in tips)
        assert tips[0].props["difficulty"] == "beginner"
        assert tips[1].props["difficulty"] == "intermediate"
        assert tips[2].props["difficulty"] == "advanced"
        assert all("expertName" in t.props for t in tips)
        assert all("category" in t.props for t in tips)

    def test_people_integration_mixed_content(self):
        """Test integration: mixing people components with other components."""
        reset_id_counter()

        content = [
            # Profile of expert
            generate_profile_card(
                name="Dr. Emily Zhang",
                title="AI Research Scientist",
                bio="Leading researcher in machine learning",
                social_links=[
                    {"platform": "linkedin", "url": "https://linkedin.com/in/emilyzhang"}
                ]
            ),
            # Quote from expert
            generate_quote_card(
                text="AI will transform every industry in the next decade.",
                author="Dr. Emily Zhang",
                highlight=True
            ),
            # Expert tip from same person
            generate_expert_tip(
                title="Getting Started with ML",
                content="Focus on understanding the fundamentals before diving into frameworks",
                expert_name="Dr. Emily Zhang",
                difficulty="beginner",
                category="machine-learning"
            ),
            # Company where expert works
            generate_company_card(
                name="AI Research Labs",
                description="Cutting-edge AI research organization",
                website="https://airesearchlabs.com",
                industries=["Research", "AI", "Technology"]
            )
        ]

        # Verify mixed content
        assert len(content) == 4
        assert content[0].type == "a2ui.ProfileCard"
        assert content[1].type == "a2ui.QuoteCard"
        assert content[2].type == "a2ui.ExpertTip"
        assert content[3].type == "a2ui.CompanyCard"

        # Verify expert consistency
        assert content[0].props["name"] == "Dr. Emily Zhang"
        assert content[1].props["author"] == "Dr. Emily Zhang"
        assert content[2].props["expertName"] == "Dr. Emily Zhang"

    def test_people_batch_generation(self):
        """Test batch generation of people components."""
        reset_id_counter()

        # Generate batch of profiles
        profiles = [
            generate_profile_card(f"Person {i}", f"Title {i}")
            for i in range(1, 6)
        ]

        # Generate batch of quotes
        quotes = [
            generate_quote_card(f"Quote text {i}", f"Author {i}")
            for i in range(1, 4)
        ]

        # Verify batch creation
        assert len(profiles) == 5
        assert len(quotes) == 3
        assert all(p.type == "a2ui.ProfileCard" for p in profiles)
        assert all(q.type == "a2ui.QuoteCard" for q in quotes)

        # Verify sequential IDs
        profile_ids = [p.id for p in profiles]
        assert profile_ids == [
            "profile-card-1", "profile-card-2", "profile-card-3",
            "profile-card-4", "profile-card-5"
        ]
