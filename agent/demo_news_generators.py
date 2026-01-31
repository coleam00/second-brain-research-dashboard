#!/usr/bin/env python3
"""
Demo script for news component generators.
Tests all 4 news generators with realistic content.
"""

import json
from a2ui_generator import (
    generate_headline_card,
    generate_trend_indicator,
    generate_timeline_event,
    generate_news_ticker,
    reset_id_counter
)


def main():
    print("=" * 80)
    print("NEWS COMPONENT GENERATORS DEMO - DYN-192")
    print("=" * 80)
    print()

    reset_id_counter()

    # 1. Generate HeadlineCard
    print("1. HEADLINE CARD")
    print("-" * 80)
    headline = generate_headline_card(
        title="OpenAI Releases GPT-5 with Breakthrough Reasoning Capabilities",
        summary="New model shows significant improvements in mathematical reasoning, "
                "coding, and long-context understanding, marking a major leap in AI capabilities.",
        source="TechCrunch",
        published_at="2026-01-30T10:00:00Z",
        sentiment="positive",
        image_url="https://example.com/gpt5-announcement.jpg"
    )
    print(json.dumps(headline.model_dump(exclude_none=True), indent=2))
    print()

    # 2. Generate TrendIndicators
    print("2. TREND INDICATORS")
    print("-" * 80)
    trends = [
        generate_trend_indicator(
            label="AI Market Cap",
            value=2.5,
            trend="up",
            change=15.3,
            unit="T USD"
        ),
        generate_trend_indicator(
            label="Model Performance",
            value=94.5,
            trend="up",
            change=8.2,
            unit="%"
        ),
        generate_trend_indicator(
            label="Energy Usage",
            value=45.2,
            trend="down",
            change=-12.5,
            unit="%"
        )
    ]
    for trend in trends:
        print(json.dumps(trend.model_dump(exclude_none=True), indent=2))
        print()

    # 3. Generate TimelineEvents
    print("3. TIMELINE EVENTS")
    print("-" * 80)
    events = [
        generate_timeline_event(
            title="Initial Announcement",
            timestamp="2026-01-30T08:00:00Z",
            content="OpenAI CEO announces GPT-5 at keynote presentation",
            event_type="announcement",
            icon="megaphone"
        ),
        generate_timeline_event(
            title="Technical Paper Released",
            timestamp="2026-01-30T09:00:00Z",
            content="Research team publishes 150-page technical documentation",
            event_type="article",
            icon="document"
        ),
        generate_timeline_event(
            title="Beta Access Launched",
            timestamp="2026-01-30T10:00:00Z",
            content="Selected developers gain early access to GPT-5 API",
            event_type="milestone",
            icon="rocket"
        ),
        generate_timeline_event(
            title="API Documentation Updated",
            timestamp="2026-01-30T11:00:00Z",
            content="Developer documentation updated with new endpoints",
            event_type="update",
            icon="code"
        )
    ]
    for event in events:
        print(json.dumps(event.model_dump(exclude_none=True), indent=2))
        print()

    # 4. Generate NewsTicker
    print("4. NEWS TICKER")
    print("-" * 80)
    ticker = generate_news_ticker([
        {
            "text": "OpenAI stock up 23% following GPT-5 announcement",
            "url": "https://example.com/openai-stock-surge",
            "timestamp": "2026-01-30T10:15:00Z"
        },
        {
            "text": "Microsoft announces Azure integration for GPT-5",
            "url": "https://example.com/microsoft-gpt5-azure",
            "timestamp": "2026-01-30T10:30:00Z"
        },
        {
            "text": "Google responds with Gemini 2.0 preview",
            "url": "https://example.com/google-gemini-response",
            "timestamp": "2026-01-30T11:00:00Z"
        },
        {
            "text": "Industry analysts predict AI market boom",
            "url": "https://example.com/ai-market-analysis",
            "timestamp": "2026-01-30T11:15:00Z"
        }
    ])
    print(json.dumps(ticker.model_dump(exclude_none=True), indent=2))
    print()

    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    total_components = 1 + len(trends) + len(events) + 1
    print(f"Total components generated: {total_components}")
    print(f"  - HeadlineCard: 1")
    print(f"  - TrendIndicator: {len(trends)}")
    print(f"  - TimelineEvent: {len(events)}")
    print(f"  - NewsTicker: 1 (with {len(ticker.props['items'])} items)")
    print()
    print("All components validated successfully!")
    print("JSON serialization confirmed working!")
    print()


if __name__ == "__main__":
    main()
