"""
Demo script for Prompts Module.

Demonstrates the three prompt templates with sample documents:
1. Tutorial document → Content Analysis → Layout Selection → Component Selection
2. Research document → Full pipeline
3. Article document → Full pipeline

This script shows how the prompts would be used in a real scenario.
"""

from prompts import (
    format_content_analysis_prompt,
    format_layout_selection_prompt,
    format_component_selection_prompt,
    validate_component_variety,
)


# Sample documents for demonstration
SAMPLE_TUTORIAL = """# Building REST APIs with FastAPI

A comprehensive tutorial for creating production-ready REST APIs using FastAPI and Python.

## Prerequisites

Before starting, ensure you have:
- Python 3.9+
- pip installed
- Basic understanding of HTTP and REST concepts

## Setup

First, install FastAPI and Uvicorn:

```bash
pip install fastapi uvicorn[standard]
```

## Creating Your First API

Create a file called `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

## Running the Server

Start your development server:

```bash
uvicorn main:app --reload
```

Visit http://localhost:8000/docs to see the interactive API documentation.

## Adding Data Models

Use Pydantic for request/response validation:

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items/")
def create_item(item: Item):
    return item
```

## Next Steps

- Add database integration with SQLAlchemy
- Implement authentication with OAuth2
- Deploy to production with Docker
"""

SAMPLE_RESEARCH = """# AI Market Analysis Q1 2025

## Executive Summary

The global AI market reached $196 billion in Q1 2025, representing 23% year-over-year growth.
Key drivers include enterprise AI adoption, edge computing advances, and regulatory clarity.

## Market Size and Growth

| Region | Q1 2024 | Q1 2025 | Growth |
|--------|---------|---------|--------|
| North America | $89B | $112B | 26% |
| Europe | $34B | $41B | 21% |
| Asia Pacific | $28B | $35B | 25% |
| Rest of World | $8B | $8B | 0% |

Total market: $159B → $196B (+23%)

## Key Findings

### Enterprise Adoption

- 78% of Fortune 500 companies now use AI in production (up from 64% in 2024)
- Average AI budget increased 31% to $12.4M per company
- ROI improved from 2.1x to 2.8x average

### Technology Trends

1. **Edge AI Computing**: 45% growth in edge AI deployments
2. **Multimodal Models**: 67% of new projects use multimodal capabilities
3. **AI Agents**: Autonomous agent adoption up 112%

## Segment Analysis

### By Use Case

- Generative AI: $87B (44%)
- Predictive Analytics: $51B (26%)
- Computer Vision: $32B (16%)
- NLP/Language: $26B (14%)

### By Industry

Healthcare leads with 28% adoption, followed by Financial Services (24%) and Retail (18%).

## Forecast

We project 21% CAGR through 2028, reaching $385B by year-end 2028.

Key risks: Regulatory uncertainty, talent shortage, infrastructure costs.

## Methodology

Data collected from 500+ companies, 50 venture funds, and 25 industry analysts.
Survey period: January 1 - March 31, 2025.
"""

SAMPLE_ARTICLE = """# The Rise of AI-First Product Development

How artificial intelligence is transforming the way we build software products.

## A New Paradigm

We're witnessing a fundamental shift in how software products are conceived and built.
Traditional development cycles are being augmented—and in some cases replaced—by AI-first approaches.

## What AI-First Means

AI-first development means building products where artificial intelligence is not an add-on feature,
but the core architecture from day one. Companies like OpenAI, Anthropic, and Midjourney exemplify this approach.

### Key Characteristics

**Intelligence as Infrastructure**: The AI model isn't a feature—it's the platform.

**Generative Interfaces**: UIs that create content rather than just display it.

**Continuous Learning**: Products improve through usage without explicit programming.

## Real-World Examples

### GitHub Copilot

Transformed coding from writing to editing. Developers now guide AI rather than type every character.

Watch the demo: https://www.youtube.com/watch?v=example

### Notion AI

Added AI writing assistance directly into the note-taking workflow. No separate tools needed.

### Replit Ghostwriter

Built AI pair programming into their browser-based IDE from the ground up.

Check out their approach: https://github.com/replit/ghostwriter

## The Impact on Teams

Development teams are reorganizing around AI capabilities:

- **Prompt Engineers**: Craft the right questions and constraints
- **AI Trainers**: Curate datasets and fine-tune models
- **Integration Specialists**: Connect AI outputs to existing systems

## Challenges

Despite the promise, AI-first development faces obstacles:

1. **Unpredictability**: AI outputs aren't deterministic
2. **Cost**: Inference can be expensive at scale
3. **Trust**: Users need confidence in AI decisions

## Looking Ahead

The next wave will combine AI-first thinking with robust engineering practices.
We'll see hybrid approaches that balance AI creativity with human oversight.

> "The future of development is collaborative, with AI as a true partner, not just a tool."
> — Jensen Huang, NVIDIA CEO

## Resources

- [OpenAI Developer Platform](https://platform.openai.com)
- [Anthropic Claude Docs](https://docs.anthropic.com)
- [Google AI for Developers](https://ai.google.dev)
"""


def demo_content_analysis():
    """Demonstrate content analysis prompt formatting."""
    print("=" * 80)
    print("DEMO 1: CONTENT ANALYSIS PROMPT")
    print("=" * 80)
    print()

    # Format the prompt for a tutorial document
    prompt = format_content_analysis_prompt(SAMPLE_TUTORIAL)

    print("Sample Document Type: Tutorial (FastAPI)")
    print()
    print("Formatted Prompt Preview (first 1000 chars):")
    print("-" * 80)
    print(prompt[:1000])
    print("...")
    print("-" * 80)
    print()
    print(f"Full prompt length: {len(prompt)} characters")
    print()


def demo_layout_selection():
    """Demonstrate layout selection prompt formatting."""
    print("=" * 80)
    print("DEMO 2: LAYOUT SELECTION PROMPT")
    print("=" * 80)
    print()

    # Simulate content analysis result for research document
    content_analysis = {
        'document_type': 'research',
        'title': 'AI Market Analysis Q1 2025',
        'sections': [
            'Executive Summary',
            'Market Size and Growth',
            'Key Findings',
            'Segment Analysis',
            'Forecast',
            'Methodology'
        ],
        'code_blocks': [],
        'tables': [
            {
                'headers': ['Region', 'Q1 2024', 'Q1 2025', 'Growth'],
                'rows': [
                    ['North America', '$89B', '$112B', '26%'],
                    ['Europe', '$34B', '$41B', '21%'],
                ]
            }
        ],
        'links': ['https://platform.openai.com'],
        'youtube_links': [],
        'github_links': [],
        'entities': {
            'technologies': ['AI', 'Edge Computing', 'Multimodal Models'],
            'tools': [],
            'languages': [],
            'concepts': ['Market Analysis', 'Enterprise Adoption', 'ROI']
        }
    }

    prompt = format_layout_selection_prompt(content_analysis)

    print("Sample Document Type: Research (AI Market Analysis)")
    print()
    print("Content Analysis Summary:")
    print(f"  - Document Type: {content_analysis['document_type']}")
    print(f"  - Sections: {len(content_analysis['sections'])}")
    print(f"  - Tables: {len(content_analysis['tables'])}")
    print(f"  - Technologies: {len(content_analysis['entities']['technologies'])}")
    print()
    print("Formatted Prompt Preview (first 1200 chars):")
    print("-" * 80)
    print(prompt[:1200])
    print("...")
    print("-" * 80)
    print()
    print(f"Full prompt length: {len(prompt)} characters")
    print()


def demo_component_selection():
    """Demonstrate component selection prompt formatting."""
    print("=" * 80)
    print("DEMO 3: COMPONENT SELECTION PROMPT")
    print("=" * 80)
    print()

    # Simulate content analysis for article
    content_analysis = {
        'document_type': 'article',
        'title': 'The Rise of AI-First Product Development',
        'sections': [
            'A New Paradigm',
            'What AI-First Means',
            'Real-World Examples',
            'The Impact on Teams',
            'Challenges',
            'Looking Ahead',
            'Resources'
        ],
        'code_blocks': [],
        'tables': [],
        'links': [
            'https://platform.openai.com',
            'https://docs.anthropic.com',
            'https://ai.google.dev'
        ],
        'youtube_links': ['https://www.youtube.com/watch?v=example'],
        'github_links': ['https://github.com/replit/ghostwriter'],
        'entities': {
            'technologies': ['AI', 'GitHub Copilot', 'Notion AI', 'Replit'],
            'tools': [],
            'languages': [],
            'concepts': ['AI-First Development', 'Product Development']
        }
    }

    # Simulate layout decision
    layout_decision = {
        'layout_type': 'news_layout',
        'confidence': 0.88,
        'reasoning': 'Article format with media content, real-world examples, and quotes',
        'alternative_layouts': ['media_layout', 'summary_layout'],
        'component_suggestions': ['HeadlineCard', 'VideoCard', 'QuoteCard', 'LinkCard', 'RepoCard']
    }

    prompt = format_component_selection_prompt(content_analysis, layout_decision)

    print("Sample Document Type: Article (AI-First Development)")
    print()
    print("Content Analysis Summary:")
    print(f"  - Document Type: {content_analysis['document_type']}")
    print(f"  - Sections: {len(content_analysis['sections'])}")
    print(f"  - Links: {len(content_analysis['links'])}")
    print(f"  - Videos: {len(content_analysis['youtube_links'])}")
    print(f"  - GitHub Repos: {len(content_analysis['github_links'])}")
    print()
    print("Layout Decision:")
    print(f"  - Selected: {layout_decision['layout_type']}")
    print(f"  - Confidence: {layout_decision['confidence']}")
    print(f"  - Reasoning: {layout_decision['reasoning']}")
    print()
    print("Formatted Prompt Preview (first 1500 chars):")
    print("-" * 80)
    print(prompt[:1500])
    print("...")
    print("-" * 80)
    print()
    print(f"Full prompt length: {len(prompt)} characters")
    print()


def demo_variety_validation():
    """Demonstrate component variety validation."""
    print("=" * 80)
    print("DEMO 4: COMPONENT VARIETY VALIDATION")
    print("=" * 80)
    print()

    # Good example - diverse components
    good_components = [
        {'component_type': 'TLDR'},
        {'component_type': 'StatCard'},
        {'component_type': 'StatCard'},
        {'component_type': 'CodeBlock'},
        {'component_type': 'StepCard'},
        {'component_type': 'CalloutCard'},
        {'component_type': 'LinkCard'},
        {'component_type': 'TableOfContents'},
    ]

    print("Example 1: GOOD - Diverse Components")
    print("-" * 80)
    result = validate_component_variety(good_components)
    print(f"Valid: {result['valid']}")
    print(f"Unique Types: {result['unique_types_count']}")
    print(f"Max Consecutive Same Type: {result['max_consecutive_same_type']}")
    print(f"Meets Min Types (4+): {result['meets_min_types']}")
    print(f"Meets No Consecutive (<=2): {result['meets_no_consecutive']}")
    print(f"Distribution: {result['component_type_distribution']}")
    print()

    # Bad example 1 - too few types
    bad_components_1 = [
        {'component_type': 'StatCard'},
        {'component_type': 'StatCard'},
        {'component_type': 'StatCard'},
        {'component_type': 'CodeBlock'},
        {'component_type': 'CodeBlock'},
    ]

    print("Example 2: BAD - Too Few Types")
    print("-" * 80)
    result = validate_component_variety(bad_components_1)
    print(f"Valid: {result['valid']}")
    print(f"Unique Types: {result['unique_types_count']}")
    print(f"Violations: {result['violations']}")
    print()

    # Bad example 2 - too many consecutive
    bad_components_2 = [
        {'component_type': 'StatCard'},
        {'component_type': 'StatCard'},
        {'component_type': 'StatCard'},
        {'component_type': 'StatCard'},
        {'component_type': 'CodeBlock'},
        {'component_type': 'LinkCard'},
        {'component_type': 'TLDR'},
    ]

    print("Example 3: BAD - Too Many Consecutive")
    print("-" * 80)
    result = validate_component_variety(bad_components_2)
    print(f"Valid: {result['valid']}")
    print(f"Max Consecutive Same Type: {result['max_consecutive_same_type']}")
    print(f"Violations: {result['violations']}")
    print()


def main():
    """Run all demonstrations."""
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "PROMPTS MODULE DEMONSTRATION" + " " * 30 + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    demo_content_analysis()
    input("Press Enter to continue to Layout Selection demo...")
    print()

    demo_layout_selection()
    input("Press Enter to continue to Component Selection demo...")
    print()

    demo_component_selection()
    input("Press Enter to continue to Variety Validation demo...")
    print()

    demo_variety_validation()

    print("=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print()
    print("All three prompt templates have been demonstrated with sample documents:")
    print("  ✓ Content Analysis Prompt (Tutorial)")
    print("  ✓ Layout Selection Prompt (Research)")
    print("  ✓ Component Selection Prompt (Article)")
    print("  ✓ Variety Validation (Good and Bad Examples)")
    print()
    print("These prompts are ready for use with Pydantic AI and Claude Sonnet 4.")
    print()


if __name__ == "__main__":
    main()
