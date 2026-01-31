"""
Tests for A2UI Layout Generator Module.

Comprehensive test suite for layout component generators covering:
- Section container generation
- Grid layout generation
- Column layout generation
- Tabs interface generation
- Accordion collapsible generation
- Carousel slider generation
- Sidebar layout generation
- Layout nesting and integration
"""

import pytest
from a2ui_generator import (
    reset_id_counter,
    generate_section,
    generate_grid,
    generate_columns,
    generate_tabs,
    generate_accordion,
    generate_carousel,
    generate_sidebar,
)


class TestLayoutGenerators:
    """Test suite for layout component generators."""

    # ========================================================================
    # Section Generator Tests
    # ========================================================================

    def test_generate_section_basic(self):
        """Test basic section generation."""
        reset_id_counter()

        section = generate_section(
            title="Key Metrics",
            content=["stat-1", "stat-2", "stat-3"]
        )

        assert section.type == "a2ui.Section"
        assert section.props["title"] == "Key Metrics"
        assert section.children == ["stat-1", "stat-2", "stat-3"]
        assert "footer" not in section.props
        assert "style" not in section.props

    def test_generate_section_with_footer(self):
        """Test section with footer."""
        reset_id_counter()

        section = generate_section(
            title="Recent Activity",
            content=["event-1", "event-2"],
            footer="Updated 5 minutes ago"
        )

        assert section.type == "a2ui.Section"
        assert section.props["footer"] == "Updated 5 minutes ago"

    def test_generate_section_with_style(self):
        """Test section with style variants."""
        reset_id_counter()

        # Test each valid style
        for style in ["default", "bordered", "elevated", "subtle"]:
            section = generate_section(
                title="Test Section",
                content=["item-1"],
                style=style
            )
            assert section.props["style"] == style

    def test_generate_section_empty_title(self):
        """Test section with empty title raises error."""
        with pytest.raises(ValueError, match="Section title cannot be empty"):
            generate_section(title="", content=["item-1"])

        with pytest.raises(ValueError, match="Section title cannot be empty"):
            generate_section(title="   ", content=["item-1"])

    def test_generate_section_empty_content(self):
        """Test section with empty content raises error."""
        with pytest.raises(ValueError, match="Section requires at least 1 content item"):
            generate_section(title="Test", content=[])

    def test_generate_section_invalid_content_type(self):
        """Test section with non-list content raises error."""
        with pytest.raises(ValueError, match="Section content must be a list"):
            generate_section(title="Test", content="item-1")

    def test_generate_section_invalid_style(self):
        """Test section with invalid style raises error."""
        with pytest.raises(ValueError, match="Section style must be one of"):
            generate_section(title="Test", content=["item-1"], style="invalid")

    # ========================================================================
    # Grid Generator Tests
    # ========================================================================

    def test_generate_grid_basic(self):
        """Test basic grid generation."""
        reset_id_counter()

        grid = generate_grid(
            columns=3,
            items=["card-1", "card-2", "card-3", "card-4", "card-5", "card-6"]
        )

        assert grid.type == "a2ui.Grid"
        assert grid.props["columns"] == 3
        assert grid.children == ["card-1", "card-2", "card-3", "card-4", "card-5", "card-6"]
        assert "gap" not in grid.props
        assert "align" not in grid.props

    def test_generate_grid_with_gap(self):
        """Test grid with gap specification."""
        reset_id_counter()

        # Test predefined gap sizes
        for gap in ["sm", "md", "lg"]:
            grid = generate_grid(columns=2, items=["a", "b"], gap=gap)
            assert grid.props["gap"] == gap

        # Test custom CSS gap
        grid = generate_grid(columns=2, items=["a", "b"], gap="2rem")
        assert grid.props["gap"] == "2rem"

    def test_generate_grid_with_align(self):
        """Test grid with alignment options."""
        reset_id_counter()

        for align in ["start", "center", "end", "stretch"]:
            grid = generate_grid(columns=2, items=["a", "b"], align=align)
            assert grid.props["align"] == align

    def test_generate_grid_column_range(self):
        """Test grid with various column counts."""
        reset_id_counter()

        # Test valid range (1-6)
        for cols in range(1, 7):
            grid = generate_grid(columns=cols, items=["a", "b", "c"])
            assert grid.props["columns"] == cols

    def test_generate_grid_invalid_columns(self):
        """Test grid with invalid column count."""
        with pytest.raises(ValueError, match="Grid columns must be between 1 and 6"):
            generate_grid(columns=0, items=["a", "b"])

        with pytest.raises(ValueError, match="Grid columns must be between 1 and 6"):
            generate_grid(columns=7, items=["a", "b"])

        with pytest.raises(ValueError, match="Grid columns must be an integer"):
            generate_grid(columns="3", items=["a", "b"])

    def test_generate_grid_empty_items(self):
        """Test grid with empty items raises error."""
        with pytest.raises(ValueError, match="Grid requires at least 1 item"):
            generate_grid(columns=2, items=[])

    def test_generate_grid_invalid_items_type(self):
        """Test grid with non-list items raises error."""
        with pytest.raises(ValueError, match="Grid items must be a list"):
            generate_grid(columns=2, items="item-1")

    def test_generate_grid_invalid_align(self):
        """Test grid with invalid alignment raises error."""
        with pytest.raises(ValueError, match="Grid align must be one of"):
            generate_grid(columns=2, items=["a", "b"], align="invalid")

    # ========================================================================
    # Columns Generator Tests
    # ========================================================================

    def test_generate_columns_basic(self):
        """Test basic columns generation."""
        reset_id_counter()

        cols = generate_columns(
            widths=["50%", "50%"],
            items=["main-content", "sidebar-content"]
        )

        assert cols.type == "a2ui.Columns"
        assert cols.props["widths"] == ["50%", "50%"]
        assert cols.children == ["main-content", "sidebar-content"]
        assert "gap" not in cols.props

    def test_generate_columns_fractional_widths(self):
        """Test columns with fractional widths."""
        reset_id_counter()

        cols = generate_columns(
            widths=["2fr", "1fr", "1fr"],
            items=["content-1", "content-2", "content-3"]
        )

        assert cols.props["widths"] == ["2fr", "1fr", "1fr"]
        assert len(cols.children) == 3

    def test_generate_columns_mixed_widths(self):
        """Test columns with mixed width units."""
        reset_id_counter()

        cols = generate_columns(
            widths=["300px", "auto"],
            items=["sidebar", "main"],
            gap="lg"
        )

        assert cols.props["widths"] == ["300px", "auto"]
        assert cols.props["gap"] == "lg"

    def test_generate_columns_with_gap(self):
        """Test columns with gap specification."""
        reset_id_counter()

        cols = generate_columns(
            widths=["1fr", "1fr"],
            items=["a", "b"],
            gap="md"
        )

        assert cols.props["gap"] == "md"

    def test_generate_columns_mismatched_lengths(self):
        """Test columns with mismatched widths and items lengths."""
        with pytest.raises(ValueError, match="Columns widths and items must have same length"):
            generate_columns(
                widths=["50%", "50%"],
                items=["content-1"]  # Only 1 item for 2 widths
            )

        with pytest.raises(ValueError, match="Columns widths and items must have same length"):
            generate_columns(
                widths=["50%"],
                items=["content-1", "content-2"]  # 2 items for 1 width
            )

    def test_generate_columns_empty_widths(self):
        """Test columns with empty widths raises error."""
        with pytest.raises(ValueError, match="Columns requires at least 1 width specification"):
            generate_columns(widths=[], items=[])

    def test_generate_columns_too_many_columns(self):
        """Test columns with more than 4 columns raises error."""
        with pytest.raises(ValueError, match="Columns supports up to 4 columns"):
            generate_columns(
                widths=["1fr", "1fr", "1fr", "1fr", "1fr"],
                items=["a", "b", "c", "d", "e"]
            )

    def test_generate_columns_invalid_widths_type(self):
        """Test columns with non-list widths raises error."""
        with pytest.raises(ValueError, match="Columns widths must be a list"):
            generate_columns(widths="50%", items=["a"])

    def test_generate_columns_invalid_items_type(self):
        """Test columns with non-list items raises error."""
        with pytest.raises(ValueError, match="Columns items must be a list"):
            generate_columns(widths=["50%", "50%"], items="content-1")

    # ========================================================================
    # Tabs Generator Tests
    # ========================================================================

    def test_generate_tabs_basic(self):
        """Test basic tabs generation."""
        reset_id_counter()

        tabs = generate_tabs(
            tabs_data=[
                {"label": "Overview", "content": ["summary-1", "stats-1"]},
                {"label": "Details", "content": ["table-1", "chart-1"]},
                {"label": "History", "content": ["timeline-1"]}
            ]
        )

        assert tabs.type == "a2ui.Tabs"
        assert len(tabs.props["tabs"]) == 3
        assert tabs.props["tabs"][0]["label"] == "Overview"
        assert tabs.props["tabs"][1]["label"] == "Details"
        assert tabs.props["activeTab"] == 0
        assert tabs.children["0"] == ["summary-1", "stats-1"]
        assert tabs.children["1"] == ["table-1", "chart-1"]
        assert tabs.children["2"] == ["timeline-1"]

    def test_generate_tabs_custom_active_tab(self):
        """Test tabs with custom active tab."""
        reset_id_counter()

        tabs = generate_tabs(
            tabs_data=[
                {"label": "All", "content": ["list-all"]},
                {"label": "Active", "content": ["list-active"]},
                {"label": "Completed", "content": ["list-completed"]}
            ],
            active_tab=1
        )

        assert tabs.props["activeTab"] == 1

    def test_generate_tabs_single_tab(self):
        """Test tabs with single tab."""
        reset_id_counter()

        tabs = generate_tabs(
            tabs_data=[
                {"label": "Main", "content": ["content-1"]}
            ]
        )

        assert len(tabs.props["tabs"]) == 1
        assert tabs.props["activeTab"] == 0

    def test_generate_tabs_empty_tabs_data(self):
        """Test tabs with empty tabs_data raises error."""
        with pytest.raises(ValueError, match="Tabs requires at least 1 tab"):
            generate_tabs(tabs_data=[])

    def test_generate_tabs_too_many_tabs(self):
        """Test tabs with more than 8 tabs raises error."""
        tabs_data = [{"label": f"Tab {i}", "content": [f"content-{i}"]} for i in range(9)]

        with pytest.raises(ValueError, match="Tabs supports up to 8 tabs"):
            generate_tabs(tabs_data=tabs_data)

    def test_generate_tabs_missing_label(self):
        """Test tabs with missing label raises error."""
        with pytest.raises(ValueError, match="Tab 0 must have 'label' field"):
            generate_tabs(
                tabs_data=[
                    {"content": ["content-1"]}  # Missing label
                ]
            )

    def test_generate_tabs_missing_content(self):
        """Test tabs with missing content raises error."""
        with pytest.raises(ValueError, match="Tab 0 must have 'content' field"):
            generate_tabs(
                tabs_data=[
                    {"label": "Tab 1"}  # Missing content
                ]
            )

    def test_generate_tabs_invalid_content_type(self):
        """Test tabs with non-list content raises error."""
        with pytest.raises(ValueError, match="Tab 0 content must be a list"):
            generate_tabs(
                tabs_data=[
                    {"label": "Tab 1", "content": "content-1"}  # String instead of list
                ]
            )

    def test_generate_tabs_invalid_active_tab(self):
        """Test tabs with invalid active_tab raises error."""
        tabs_data = [
            {"label": "Tab 1", "content": ["content-1"]},
            {"label": "Tab 2", "content": ["content-2"]}
        ]

        with pytest.raises(ValueError, match="Tabs active_tab must be between 0 and 1"):
            generate_tabs(tabs_data=tabs_data, active_tab=2)

        with pytest.raises(ValueError, match="Tabs active_tab must be between 0 and 1"):
            generate_tabs(tabs_data=tabs_data, active_tab=-1)

    def test_generate_tabs_invalid_tabs_data_type(self):
        """Test tabs with non-list tabs_data raises error."""
        with pytest.raises(ValueError, match="Tabs tabs_data must be a list"):
            generate_tabs(tabs_data="not a list")

    # ========================================================================
    # Accordion Generator Tests
    # ========================================================================

    def test_generate_accordion_basic(self):
        """Test basic accordion generation."""
        reset_id_counter()

        accordion = generate_accordion(
            items=[
                {"title": "Getting Started", "content": ["step-1", "step-2", "step-3"]},
                {"title": "Advanced Features", "content": ["feature-1", "feature-2"]},
                {"title": "Troubleshooting", "content": ["faq-1", "faq-2"]}
            ]
        )

        assert accordion.type == "a2ui.Accordion"
        assert len(accordion.props["items"]) == 3
        assert accordion.props["items"][0]["title"] == "Getting Started"
        assert accordion.props["allowMultiple"] is False
        assert accordion.children["0"] == ["step-1", "step-2", "step-3"]
        assert accordion.children["1"] == ["feature-1", "feature-2"]
        assert accordion.children["2"] == ["faq-1", "faq-2"]

    def test_generate_accordion_allow_multiple(self):
        """Test accordion with allow_multiple enabled."""
        reset_id_counter()

        accordion = generate_accordion(
            items=[
                {"title": "Section 1", "content": ["content-1"]},
                {"title": "Section 2", "content": ["content-2"]}
            ],
            allow_multiple=True
        )

        assert accordion.props["allowMultiple"] is True

    def test_generate_accordion_single_item(self):
        """Test accordion with single item."""
        reset_id_counter()

        accordion = generate_accordion(
            items=[
                {"title": "Main Section", "content": ["content-1", "content-2"]}
            ]
        )

        assert len(accordion.props["items"]) == 1
        assert accordion.children["0"] == ["content-1", "content-2"]

    def test_generate_accordion_empty_items(self):
        """Test accordion with empty items raises error."""
        with pytest.raises(ValueError, match="Accordion requires at least 1 item"):
            generate_accordion(items=[])

    def test_generate_accordion_too_many_items(self):
        """Test accordion with more than 10 items raises error."""
        items = [{"title": f"Section {i}", "content": [f"content-{i}"]} for i in range(11)]

        with pytest.raises(ValueError, match="Accordion supports up to 10 items"):
            generate_accordion(items=items)

    def test_generate_accordion_missing_title(self):
        """Test accordion with missing title raises error."""
        with pytest.raises(ValueError, match="Accordion item 0 must have 'title' field"):
            generate_accordion(
                items=[
                    {"content": ["content-1"]}  # Missing title
                ]
            )

    def test_generate_accordion_missing_content(self):
        """Test accordion with missing content raises error."""
        with pytest.raises(ValueError, match="Accordion item 0 must have 'content' field"):
            generate_accordion(
                items=[
                    {"title": "Section 1"}  # Missing content
                ]
            )

    def test_generate_accordion_invalid_content_type(self):
        """Test accordion with non-list content raises error."""
        with pytest.raises(ValueError, match="Accordion item 0 content must be a list"):
            generate_accordion(
                items=[
                    {"title": "Section 1", "content": "content-1"}  # String instead of list
                ]
            )

    def test_generate_accordion_invalid_items_type(self):
        """Test accordion with non-list items raises error."""
        with pytest.raises(ValueError, match="Accordion items must be a list"):
            generate_accordion(items="not a list")

    # ========================================================================
    # Carousel Generator Tests
    # ========================================================================

    def test_generate_carousel_basic(self):
        """Test basic carousel generation."""
        reset_id_counter()

        carousel = generate_carousel(
            items=["image-1", "image-2", "image-3", "image-4"]
        )

        assert carousel.type == "a2ui.Carousel"
        assert carousel.props["visibleCount"] == 1
        assert carousel.props["autoAdvance"] is False
        assert carousel.children == ["image-1", "image-2", "image-3", "image-4"]

    def test_generate_carousel_with_auto_advance(self):
        """Test carousel with auto-advance enabled."""
        reset_id_counter()

        carousel = generate_carousel(
            items=["slide-1", "slide-2", "slide-3"],
            auto_advance=True
        )

        assert carousel.props["autoAdvance"] is True

    def test_generate_carousel_multiple_visible(self):
        """Test carousel with multiple visible items."""
        reset_id_counter()

        for visible in range(1, 5):
            items = [f"item-{i}" for i in range(visible + 2)]  # Ensure enough items
            carousel = generate_carousel(items=items, visible_count=visible)
            assert carousel.props["visibleCount"] == visible

    def test_generate_carousel_empty_items(self):
        """Test carousel with empty items raises error."""
        with pytest.raises(ValueError, match="Carousel requires at least 1 item"):
            generate_carousel(items=[])

    def test_generate_carousel_invalid_visible_count(self):
        """Test carousel with invalid visible_count raises error."""
        items = ["a", "b", "c", "d"]

        with pytest.raises(ValueError, match="Carousel visible_count must be between 1 and 4"):
            generate_carousel(items=items, visible_count=0)

        with pytest.raises(ValueError, match="Carousel visible_count must be between 1 and 4"):
            generate_carousel(items=items, visible_count=5)

        with pytest.raises(ValueError, match="Carousel visible_count must be an integer"):
            generate_carousel(items=items, visible_count="2")

    def test_generate_carousel_insufficient_items(self):
        """Test carousel with fewer items than visible_count raises error."""
        with pytest.raises(ValueError, match="Carousel must have at least 3 items to show 3 visible"):
            generate_carousel(items=["a", "b"], visible_count=3)

    def test_generate_carousel_invalid_items_type(self):
        """Test carousel with non-list items raises error."""
        with pytest.raises(ValueError, match="Carousel items must be a list"):
            generate_carousel(items="item-1")

    # ========================================================================
    # Sidebar Generator Tests
    # ========================================================================

    def test_generate_sidebar_basic(self):
        """Test basic sidebar generation."""
        reset_id_counter()

        sidebar = generate_sidebar(
            sidebar_content=["nav-1", "filters-1"],
            main_content=["content-1", "content-2", "content-3"]
        )

        assert sidebar.type == "a2ui.Sidebar"
        assert sidebar.props["sidebarWidth"] == "30%"
        assert sidebar.children["sidebar"] == ["nav-1", "filters-1"]
        assert sidebar.children["main"] == ["content-1", "content-2", "content-3"]

    def test_generate_sidebar_custom_width(self):
        """Test sidebar with custom width."""
        reset_id_counter()

        # Test percentage width
        sidebar = generate_sidebar(
            sidebar_content=["toc-1"],
            main_content=["article-1"],
            sidebar_width="25%"
        )
        assert sidebar.props["sidebarWidth"] == "25%"

        # Test pixel width
        sidebar = generate_sidebar(
            sidebar_content=["toc-1"],
            main_content=["article-1"],
            sidebar_width="250px"
        )
        assert sidebar.props["sidebarWidth"] == "250px"

        # Test CSS value
        sidebar = generate_sidebar(
            sidebar_content=["toc-1"],
            main_content=["article-1"],
            sidebar_width="20rem"
        )
        assert sidebar.props["sidebarWidth"] == "20rem"

    def test_generate_sidebar_empty_sidebar_content(self):
        """Test sidebar with empty sidebar_content raises error."""
        with pytest.raises(ValueError, match="Sidebar requires at least 1 sidebar content item"):
            generate_sidebar(
                sidebar_content=[],
                main_content=["content-1"]
            )

    def test_generate_sidebar_empty_main_content(self):
        """Test sidebar with empty main_content raises error."""
        with pytest.raises(ValueError, match="Sidebar requires at least 1 main content item"):
            generate_sidebar(
                sidebar_content=["nav-1"],
                main_content=[]
            )

    def test_generate_sidebar_invalid_sidebar_content_type(self):
        """Test sidebar with non-list sidebar_content raises error."""
        with pytest.raises(ValueError, match="Sidebar sidebar_content must be a list"):
            generate_sidebar(
                sidebar_content="nav-1",
                main_content=["content-1"]
            )

    def test_generate_sidebar_invalid_main_content_type(self):
        """Test sidebar with non-list main_content raises error."""
        with pytest.raises(ValueError, match="Sidebar main_content must be a list"):
            generate_sidebar(
                sidebar_content=["nav-1"],
                main_content="content-1"
            )

    def test_generate_sidebar_empty_width(self):
        """Test sidebar with empty sidebar_width raises error."""
        with pytest.raises(ValueError, match="Sidebar sidebar_width cannot be empty"):
            generate_sidebar(
                sidebar_content=["nav-1"],
                main_content=["content-1"],
                sidebar_width=""
            )

        with pytest.raises(ValueError, match="Sidebar sidebar_width cannot be empty"):
            generate_sidebar(
                sidebar_content=["nav-1"],
                main_content=["content-1"],
                sidebar_width="   "
            )

    # ========================================================================
    # Layout Integration Tests
    # ========================================================================

    def test_layout_nesting_section_with_grid(self):
        """Test nesting grid inside section."""
        reset_id_counter()

        # Create grid
        grid = generate_grid(
            columns=2,
            items=["card-1", "card-2", "card-3", "card-4"]
        )

        # Create section containing grid
        section = generate_section(
            title="Dashboard Cards",
            content=[grid.id]
        )

        assert section.children == [grid.id]
        assert grid.type == "a2ui.Grid"

    def test_layout_nesting_tabs_with_sections(self):
        """Test tabs containing multiple sections."""
        reset_id_counter()

        # Create sections
        section1 = generate_section(title="Stats", content=["stat-1", "stat-2"])
        section2 = generate_section(title="Charts", content=["chart-1", "chart-2"])

        # Create tabs containing sections
        tabs = generate_tabs(
            tabs_data=[
                {"label": "Overview", "content": [section1.id]},
                {"label": "Analytics", "content": [section2.id]}
            ]
        )

        assert tabs.children["0"] == [section1.id]
        assert tabs.children["1"] == [section2.id]

    def test_layout_nesting_sidebar_with_accordion(self):
        """Test sidebar with accordion in sidebar panel."""
        reset_id_counter()

        # Create accordion for sidebar
        accordion = generate_accordion(
            items=[
                {"title": "Navigation", "content": ["link-1", "link-2"]},
                {"title": "Filters", "content": ["filter-1", "filter-2"]}
            ]
        )

        # Create sidebar layout
        sidebar = generate_sidebar(
            sidebar_content=[accordion.id],
            main_content=["content-1", "content-2"]
        )

        assert sidebar.children["sidebar"] == [accordion.id]
        assert accordion.type == "a2ui.Accordion"

    def test_layout_nesting_columns_with_carousels(self):
        """Test columns containing carousels."""
        reset_id_counter()

        # Create carousels
        carousel1 = generate_carousel(items=["img-1", "img-2", "img-3"])
        carousel2 = generate_carousel(items=["vid-1", "vid-2", "vid-3"])

        # Create columns containing carousels
        columns = generate_columns(
            widths=["50%", "50%"],
            items=[carousel1.id, carousel2.id]
        )

        assert columns.children == [carousel1.id, carousel2.id]

    def test_layout_complex_dashboard_hierarchy(self):
        """Test complex nested layout hierarchy."""
        reset_id_counter()

        # Create bottom-level components (stats)
        stats_ids = ["stat-1", "stat-2", "stat-3", "stat-4"]

        # Create grid of stats
        stats_grid = generate_grid(columns=2, items=stats_ids)

        # Create sections for different categories
        section1 = generate_section(
            title="Performance Metrics",
            content=[stats_grid.id],
            style="elevated"
        )

        charts_ids = ["chart-1", "chart-2"]
        section2 = generate_section(
            title="Trend Analysis",
            content=charts_ids,
            style="elevated"
        )

        # Create tabs containing sections
        tabs = generate_tabs(
            tabs_data=[
                {"label": "Overview", "content": [section1.id]},
                {"label": "Trends", "content": [section2.id]}
            ]
        )

        # Create sidebar layout with tabs
        nav_items = ["nav-1", "nav-2", "nav-3"]
        dashboard = generate_sidebar(
            sidebar_content=nav_items,
            main_content=[tabs.id],
            sidebar_width="250px"
        )

        # Verify structure
        assert dashboard.type == "a2ui.Sidebar"
        assert dashboard.children["main"] == [tabs.id]
        assert tabs.children["0"] == [section1.id]
        assert section1.children == [stats_grid.id]
        assert stats_grid.children == stats_ids

    def test_layout_responsive_grid_configurations(self):
        """Test different responsive grid configurations."""
        reset_id_counter()

        # Single column (mobile-friendly)
        grid1 = generate_grid(columns=1, items=["a", "b", "c"])
        assert grid1.props["columns"] == 1

        # Two columns (tablet)
        grid2 = generate_grid(columns=2, items=["a", "b", "c", "d"])
        assert grid2.props["columns"] == 2

        # Three columns (desktop)
        grid3 = generate_grid(columns=3, items=["a", "b", "c", "d", "e", "f"])
        assert grid3.props["columns"] == 3

        # Four columns (wide desktop)
        grid4 = generate_grid(columns=4, items=["a", "b", "c", "d"])
        assert grid4.props["columns"] == 4

    def test_layout_accordion_tabs_comparison(self):
        """Test similar content organization with accordion vs tabs."""
        reset_id_counter()

        content_sections = [
            {"title": "Section 1", "content": ["item-1", "item-2"]},
            {"title": "Section 2", "content": ["item-3", "item-4"]},
            {"title": "Section 3", "content": ["item-5", "item-6"]}
        ]

        # Create accordion version
        accordion = generate_accordion(
            items=content_sections,
            allow_multiple=True
        )

        # Create tabs version with same data
        tabs_data = [
            {"label": sec["title"], "content": sec["content"]}
            for sec in content_sections
        ]
        tabs = generate_tabs(tabs_data=tabs_data)

        # Both should organize same content differently
        assert accordion.type == "a2ui.Accordion"
        assert tabs.type == "a2ui.Tabs"
        assert len(accordion.props["items"]) == len(tabs.props["tabs"])

    def test_layout_carousel_grid_comparison(self):
        """Test content display with carousel vs grid."""
        reset_id_counter()

        items = ["card-1", "card-2", "card-3", "card-4", "card-5", "card-6"]

        # Carousel shows items one at a time (or few at once)
        carousel = generate_carousel(items=items, visible_count=1)
        assert carousel.props["visibleCount"] == 1

        # Grid shows all items simultaneously
        grid = generate_grid(columns=3, items=items)
        assert len(grid.children) == 6

    def test_layout_all_generators_integration(self):
        """Test integration workflow using all layout generators."""
        reset_id_counter()

        # Build a complete dashboard using all layout types

        # 1. Create grid of stat cards
        stats_grid = generate_grid(
            columns=4,
            items=["stat-1", "stat-2", "stat-3", "stat-4"],
            gap="md"
        )

        # 2. Create carousel of featured items
        featured_carousel = generate_carousel(
            items=["featured-1", "featured-2", "featured-3"],
            visible_count=1,
            auto_advance=True
        )

        # 3. Create accordion for FAQs
        faq_accordion = generate_accordion(
            items=[
                {"title": "How do I get started?", "content": ["answer-1"]},
                {"title": "What features are available?", "content": ["answer-2"]},
                {"title": "How much does it cost?", "content": ["answer-3"]}
            ]
        )

        # 4. Create tabs for different views
        main_tabs = generate_tabs(
            tabs_data=[
                {"label": "Dashboard", "content": [stats_grid.id, featured_carousel.id]},
                {"label": "FAQ", "content": [faq_accordion.id]},
                {"label": "Settings", "content": ["settings-1"]}
            ]
        )

        # 5. Create two-column layout
        content_columns = generate_columns(
            widths=["2fr", "1fr"],
            items=[main_tabs.id, "widget-panel"],
            gap="lg"
        )

        # 6. Wrap in section
        main_section = generate_section(
            title="Dashboard",
            content=[content_columns.id],
            footer="Last updated: 2 minutes ago",
            style="elevated"
        )

        # 7. Create final sidebar layout
        final_layout = generate_sidebar(
            sidebar_content=["nav-1", "profile-1"],
            main_content=[main_section.id],
            sidebar_width="20%"
        )

        # Verify all components created
        assert final_layout.type == "a2ui.Sidebar"
        assert main_section.type == "a2ui.Section"
        assert content_columns.type == "a2ui.Columns"
        assert main_tabs.type == "a2ui.Tabs"
        assert faq_accordion.type == "a2ui.Accordion"
        assert featured_carousel.type == "a2ui.Carousel"
        assert stats_grid.type == "a2ui.Grid"
