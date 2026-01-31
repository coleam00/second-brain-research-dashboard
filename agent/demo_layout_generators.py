"""
Demo script for layout component generators.

This script demonstrates all 7 layout generators in action with realistic examples.
"""

import json
from a2ui_generator import (
    reset_id_counter,
    generate_section,
    generate_grid,
    generate_columns,
    generate_tabs,
    generate_accordion,
    generate_carousel,
    generate_sidebar,
    # Import some content generators for realistic demos
    generate_stat_card,
    generate_headline_card,
    generate_link_card,
    generate_profile_card,
)


def demo_section():
    """Demonstrate Section generator."""
    print("=" * 80)
    print("SECTION DEMO - Grouping related content with header/footer")
    print("=" * 80)

    # Create some stat cards
    stat1 = generate_stat_card(title="AI Market Size", value="$196B", change=23.0, change_type="positive")
    stat2 = generate_stat_card(title="Adoption Rate", value="47%", change=12.0, change_type="positive")
    stat3 = generate_stat_card(title="Active Users", value="2.5M", change=18.0, change_type="positive")

    # Create section containing stats
    section = generate_section(
        title="Key Metrics - Q4 2025",
        content=[stat1.id, stat2.id, stat3.id],
        footer="Updated 5 minutes ago",
        style="elevated"
    )

    print(json.dumps(section.model_dump(), indent=2))
    print()


def demo_grid():
    """Demonstrate Grid generator."""
    print("=" * 80)
    print("GRID DEMO - Multi-column responsive grid layout")
    print("=" * 80)

    # Create news headlines
    headlines = [
        generate_headline_card("OpenAI Releases GPT-5", "Revolutionary AI model with enhanced capabilities", "TechNews", "2025-01-30T10:00:00Z", "positive"),
        generate_headline_card("Quantum Computing Breakthrough", "Scientists achieve new quantum milestone", "ScienceDaily", "2025-01-30T09:30:00Z", "positive"),
        generate_headline_card("New Climate Agreement Signed", "Global leaders commit to emissions targets", "WorldNews", "2025-01-30T08:00:00Z", "neutral"),
        generate_headline_card("SpaceX Mars Mission Update", "Crew training begins for 2027 mission", "SpaceToday", "2025-01-30T07:00:00Z", "positive"),
        generate_headline_card("Electric Vehicles Surpass Gas Sales", "EV market share reaches historic high", "AutoNews", "2025-01-29T18:00:00Z", "positive"),
        generate_headline_card("Global Health Summit Concludes", "New initiatives announced for pandemic preparedness", "HealthWatch", "2025-01-29T16:00:00Z", "neutral"),
    ]

    headline_ids = [h.id for h in headlines]

    # Create 3-column grid
    grid = generate_grid(
        columns=3,
        items=headline_ids,
        gap="md",
        align="start"
    )

    print(json.dumps(grid.model_dump(), indent=2))
    print()


def demo_columns():
    """Demonstrate Columns generator."""
    print("=" * 80)
    print("COLUMNS DEMO - Flexible width column layout")
    print("=" * 80)

    # Create columns with 2:1 ratio (main content wider than sidebar)
    columns = generate_columns(
        widths=["2fr", "1fr"],
        items=["article-content-1", "related-links-widget"],
        gap="lg"
    )

    print(json.dumps(columns.model_dump(), indent=2))
    print()

    # Also demo 3-column layout
    columns3 = generate_columns(
        widths=["300px", "auto", "250px"],
        items=["left-nav", "main-content", "right-sidebar"],
        gap="md"
    )

    print("3-column layout:")
    print(json.dumps(columns3.model_dump(), indent=2))
    print()


def demo_tabs():
    """Demonstrate Tabs generator."""
    print("=" * 80)
    print("TABS DEMO - Tabbed interface for organizing content")
    print("=" * 80)

    # Create tabs for different content views
    tabs = generate_tabs(
        tabs_data=[
            {
                "label": "Overview",
                "content": ["summary-1", "key-stats-grid", "recent-activity"]
            },
            {
                "label": "Analytics",
                "content": ["charts-section", "data-tables", "insights"]
            },
            {
                "label": "Settings",
                "content": ["profile-settings", "notification-prefs", "privacy-controls"]
            },
            {
                "label": "Help",
                "content": ["faq-accordion", "support-contact", "documentation-links"]
            }
        ],
        active_tab=0  # Start with Overview tab
    )

    print(json.dumps(tabs.model_dump(), indent=2))
    print()


def demo_accordion():
    """Demonstrate Accordion generator."""
    print("=" * 80)
    print("ACCORDION DEMO - Collapsible sections for space efficiency")
    print("=" * 80)

    # Create FAQ accordion
    accordion = generate_accordion(
        items=[
            {
                "title": "How do I get started?",
                "content": ["step-card-1", "step-card-2", "step-card-3"]
            },
            {
                "title": "What features are included?",
                "content": ["feature-list", "pricing-comparison"]
            },
            {
                "title": "How do I upgrade my plan?",
                "content": ["upgrade-instructions", "billing-info"]
            },
            {
                "title": "What integrations are supported?",
                "content": ["integration-grid", "api-docs-link"]
            },
            {
                "title": "How do I contact support?",
                "content": ["support-channels", "contact-form"]
            }
        ],
        allow_multiple=True  # Allow multiple sections open at once
    )

    print(json.dumps(accordion.model_dump(), indent=2))
    print()


def demo_carousel():
    """Demonstrate Carousel generator."""
    print("=" * 80)
    print("CAROUSEL DEMO - Scrollable content carousel/slider")
    print("=" * 80)

    # Single-item carousel (slideshow)
    carousel1 = generate_carousel(
        items=["featured-image-1", "featured-image-2", "featured-image-3", "featured-image-4"],
        visible_count=1,
        auto_advance=True
    )

    print("Single-item auto-advancing carousel:")
    print(json.dumps(carousel1.model_dump(), indent=2))
    print()

    # Multi-item carousel showing 3 at once
    carousel2 = generate_carousel(
        items=["testimonial-1", "testimonial-2", "testimonial-3", "testimonial-4", "testimonial-5", "testimonial-6"],
        visible_count=3,
        auto_advance=False
    )

    print("Multi-item carousel (3 visible):")
    print(json.dumps(carousel2.model_dump(), indent=2))
    print()


def demo_sidebar():
    """Demonstrate Sidebar generator."""
    print("=" * 80)
    print("SIDEBAR DEMO - Fixed sidebar + main content layout")
    print("=" * 80)

    # Create sidebar layout
    sidebar_layout = generate_sidebar(
        sidebar_content=["main-nav", "user-profile-widget", "quick-actions"],
        main_content=["page-header", "content-tabs", "footer"],
        sidebar_width="250px"
    )

    print(json.dumps(sidebar_layout.model_dump(), indent=2))
    print()

    # Also demo percentage-based sidebar
    sidebar_layout2 = generate_sidebar(
        sidebar_content=["table-of-contents"],
        main_content=["article-body"],
        sidebar_width="25%"
    )

    print("Percentage-based sidebar:")
    print(json.dumps(sidebar_layout2.model_dump(), indent=2))
    print()


def demo_complex_nested_layout():
    """Demonstrate complex nested layout combining multiple layout types."""
    print("=" * 80)
    print("COMPLEX NESTED LAYOUT DEMO - Complete dashboard structure")
    print("=" * 80)

    reset_id_counter()

    # 1. Create bottom-level content components
    stat1 = generate_stat_card(title="AI Market Size", value="$196B", change=23.0, change_type="positive")
    stat2 = generate_stat_card(title="Adoption Rate", value="47%", change=12.0, change_type="positive")
    stat3 = generate_stat_card(title="Active Users", value="2.5M", change=18.0, change_type="positive")
    stat4 = generate_stat_card(title="Uptime", value="99.9%", change_type="neutral")

    # 2. Create grid of stats
    stats_grid = generate_grid(
        columns=4,
        items=[stat1.id, stat2.id, stat3.id, stat4.id],
        gap="md"
    )

    # 3. Create sections for different content areas
    overview_section = generate_section(
        title="Performance Overview",
        content=[stats_grid.id],
        style="elevated"
    )

    # 4. Create carousel of featured content
    featured_carousel = generate_carousel(
        items=["featured-1", "featured-2", "featured-3"],
        visible_count=1,
        auto_advance=True
    )

    featured_section = generate_section(
        title="Featured Content",
        content=[featured_carousel.id],
        style="bordered"
    )

    # 5. Create accordion for FAQ
    faq_accordion = generate_accordion(
        items=[
            {"title": "Getting Started", "content": ["faq-1", "faq-2"]},
            {"title": "Advanced Features", "content": ["faq-3", "faq-4"]},
            {"title": "Troubleshooting", "content": ["faq-5", "faq-6"]}
        ]
    )

    faq_section = generate_section(
        title="Frequently Asked Questions",
        content=[faq_accordion.id]
    )

    # 6. Create tabs to organize main content
    main_tabs = generate_tabs(
        tabs_data=[
            {"label": "Dashboard", "content": [overview_section.id, featured_section.id]},
            {"label": "Help", "content": [faq_section.id]},
            {"label": "Settings", "content": ["settings-panel"]}
        ]
    )

    # 7. Create columns for main content + widget panel
    content_columns = generate_columns(
        widths=["2fr", "1fr"],
        items=[main_tabs.id, "widgets-panel"],
        gap="lg"
    )

    # 8. Wrap in final section
    main_section = generate_section(
        title="AI Research Dashboard",
        content=[content_columns.id],
        footer="Last updated: 2 minutes ago"
    )

    # 9. Create final sidebar layout
    final_layout = generate_sidebar(
        sidebar_content=["main-nav", "user-profile", "notifications"],
        main_content=[main_section.id],
        sidebar_width="250px"
    )

    print("Complete nested dashboard structure:")
    print(json.dumps(final_layout.model_dump(), indent=2))
    print()
    print(f"Total components created: {len([stat1, stat2, stat3, stat4, stats_grid, overview_section, featured_carousel, featured_section, faq_accordion, faq_section, main_tabs, content_columns, main_section, final_layout])}")
    print()


def main():
    """Run all layout generator demos."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "A2UI LAYOUT GENERATORS DEMO" + " " * 31 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")

    reset_id_counter()

    demo_section()
    demo_grid()
    demo_columns()
    demo_tabs()
    demo_accordion()
    demo_carousel()
    demo_sidebar()
    demo_complex_nested_layout()

    print("=" * 80)
    print("All layout generator demos completed successfully!")
    print("=" * 80)


if __name__ == "__main__":
    main()
