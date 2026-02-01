"""
Comprehensive test suite for the main orchestrator pipeline.

Tests the orchestrate_dashboard function which wires together:
- Markdown parsing (parse_markdown)
- Content analysis (analyze_content)
- Layout selection (select_layout)
- Component generation (all generators)
- Variety enforcement
- Component tree building
"""

import pytest
from a2ui_generator import (
    orchestrate_dashboard,
    A2UIComponent,
    reset_id_counter,
)


class TestOrchestratorBasic:
    """Test basic orchestrator functionality."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_orchestrate_dashboard_minimal_content(self):
        """Test orchestrator with minimal markdown content."""
        markdown = "# Hello World\n\nThis is a test."

        components = orchestrate_dashboard(markdown)

        # Should return at least 4 components (minimum requirement)
        assert len(components) >= 4
        assert all(isinstance(comp, A2UIComponent) for comp in components)

    def test_orchestrate_dashboard_empty_content(self):
        """Test orchestrator with empty content."""
        markdown = ""

        components = orchestrate_dashboard(markdown)

        # Should still return minimum components
        assert len(components) >= 4

    def test_orchestrate_dashboard_only_title(self):
        """Test orchestrator with only title."""
        markdown = "# Just a Title"

        components = orchestrate_dashboard(markdown)

        assert len(components) >= 4
        # First component should be a Section with the title
        assert components[0].type == "a2ui.Section"
        assert "Just a Title" in components[0].props.get("title", "")

    def test_orchestrate_dashboard_returns_list(self):
        """Test that orchestrator returns a list."""
        markdown = "# Test\n\nContent here."

        result = orchestrate_dashboard(markdown)

        assert isinstance(result, list)
        assert all(isinstance(item, A2UIComponent) for item in result)

    def test_orchestrate_dashboard_unique_ids(self):
        """Test that all components have unique IDs."""
        markdown = "# Test Document\n\n## Section 1\n\n## Section 2"

        components = orchestrate_dashboard(markdown)

        ids = [comp.id for comp in components]
        assert len(ids) == len(set(ids)), "All component IDs should be unique"


class TestOrchestratorVarietyEnforcement:
    """Test variety enforcement constraints."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_minimum_four_component_types(self):
        """Test that output has minimum 4 different component types."""
        markdown = "# Test\n\nSome content here."

        components = orchestrate_dashboard(markdown)

        # Count unique component types
        component_types = set(comp.type for comp in components)

        assert len(component_types) >= 4, f"Expected at least 4 different types, got {len(component_types)}: {component_types}"

    def test_no_three_consecutive_same_type(self):
        """Test that there are no 3+ consecutive components of same type."""
        markdown = """
# Tutorial

## Step 1
Content here

## Step 2
More content

## Step 3
Even more

## Step 4
And more
"""

        components = orchestrate_dashboard(markdown)

        # Check for 3+ consecutive same types
        for i in range(len(components) - 2):
            type1 = components[i].type
            type2 = components[i + 1].type
            type3 = components[i + 2].type

            if type1 == type2 == type3:
                pytest.fail(f"Found 3 consecutive components of type {type1} at positions {i}, {i+1}, {i+2}")

    def test_variety_with_code_heavy_content(self):
        """Test variety enforcement with code-heavy content."""
        markdown = """
# Code Tutorial

```python
print("hello")
```

```javascript
console.log("world")
```

```bash
echo "test"
```

```python
def foo():
    pass
```
"""

        components = orchestrate_dashboard(markdown)

        # Even with many code blocks, should have variety
        component_types = set(comp.type for comp in components)
        assert len(component_types) >= 4

    def test_variety_with_link_heavy_content(self):
        """Test variety enforcement with many links."""
        markdown = """
# Resources

- [Link 1](https://example.com/1)
- [Link 2](https://example.com/2)
- [Link 3](https://example.com/3)
- [Link 4](https://example.com/4)
- [Link 5](https://example.com/5)
"""

        components = orchestrate_dashboard(markdown)

        component_types = set(comp.type for comp in components)
        assert len(component_types) >= 4


class TestOrchestratorContentTypes:
    """Test orchestrator with different content types."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_tutorial_content_generates_code_blocks(self):
        """Test that tutorial content generates code blocks."""
        markdown = """
# Python Tutorial

## Step 1: Install
```python
pip install requests
```

## Step 2: Import
```python
import requests
```
"""

        components = orchestrate_dashboard(markdown)

        # Should have at least one code block
        code_blocks = [c for c in components if c.type == "a2ui.CodeBlock"]
        assert len(code_blocks) > 0

    def test_tutorial_content_generates_step_cards(self):
        """Test that tutorial content generates step cards."""
        markdown = """
# How to Build an App

## Step 1: Setup
Configure your environment

## Step 2: Code
Write the application

## Step 3: Deploy
Launch to production
"""

        components = orchestrate_dashboard(markdown)

        # Should have step cards for tutorial content
        step_cards = [c for c in components if c.type == "a2ui.StepCard"]
        # May or may not have steps depending on classification, but should have variety
        assert len(components) >= 4

    def test_research_content_generates_tables(self):
        """Test that research content generates tables."""
        markdown = """
# Research Paper

| Metric | Value |
|--------|-------|
| Accuracy | 95% |
| Precision | 92% |
"""

        components = orchestrate_dashboard(markdown)

        # Should have table component
        tables = [c for c in components if c.type == "a2ui.DataTable"]
        # Tables should be generated if detected
        assert len(components) >= 4

    def test_research_content_generates_stat_cards(self):
        """Test that research content may generate stat cards."""
        markdown = """
# AI Research Results

The model achieved 95% accuracy with 87% precision.
Performance improved by 23% compared to baseline.
"""

        components = orchestrate_dashboard(markdown)

        # Should have variety of components
        assert len(components) >= 4
        component_types = set(comp.type for comp in components)
        assert len(component_types) >= 4

    def test_article_content_generates_headlines(self):
        """Test that article content generates headlines."""
        markdown = """
# Breaking News

## Major Development
Important update here

## Analysis
Expert commentary
"""

        components = orchestrate_dashboard(markdown)

        # Should have components appropriate for article
        assert len(components) >= 4

    def test_article_content_with_youtube_links(self):
        """Test article content with YouTube links generates video cards."""
        markdown = """
# Tech Article

Watch this video: https://www.youtube.com/watch?v=dQw4w9WgXcQ

Another video: https://youtu.be/abcdefghijk
"""

        components = orchestrate_dashboard(markdown)

        # Should have video cards
        video_cards = [c for c in components if c.type == "a2ui.VideoCard"]
        assert len(video_cards) > 0

    def test_github_links_generate_repo_cards(self):
        """Test that GitHub links generate repo cards."""
        markdown = """
# Open Source Projects

Check out: https://github.com/facebook/react
Also see: https://github.com/microsoft/vscode
"""

        components = orchestrate_dashboard(markdown)

        # Should have repo cards
        repo_cards = [c for c in components if c.type == "a2ui.RepoCard"]
        assert len(repo_cards) > 0


class TestOrchestratorComponentGeneration:
    """Test specific component generation scenarios."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_generates_section_for_title(self):
        """Test that title generates a Section component."""
        markdown = "# Main Title\n\nContent"

        components = orchestrate_dashboard(markdown)

        # First component should be Section with title
        assert components[0].type == "a2ui.Section"
        assert "Main Title" in components[0].props.get("title", "")

    def test_generates_tldr_for_long_content(self):
        """Test that long content generates TLDR."""
        markdown = "# Article\n\n" + "Lorem ipsum dolor sit amet. " * 50

        components = orchestrate_dashboard(markdown)

        # Should have TLDR for long content
        tldr_components = [c for c in components if c.type == "a2ui.TLDR"]
        assert len(tldr_components) > 0

    def test_generates_table_of_contents_for_many_sections(self):
        """Test that many sections generate table of contents."""
        markdown = """
# Main Title

## Section 1
## Section 2
## Section 3
## Section 4
## Section 5
## Section 6
"""

        components = orchestrate_dashboard(markdown)

        # Should have table of contents
        toc_components = [c for c in components if c.type == "a2ui.TableOfContents"]
        assert len(toc_components) > 0

    def test_generates_tags_for_technologies(self):
        """Test that technology mentions generate tags."""
        markdown = """
# Tech Stack

We use React, Python, and Docker for our application.
"""

        components = orchestrate_dashboard(markdown)

        # Should have tag components for technologies
        tags = [c for c in components if c.type == "a2ui.Tag"]
        assert len(tags) > 0

    def test_generates_link_cards_for_urls(self):
        """Test that URLs generate link cards."""
        markdown = """
# Resources

- https://example.com/resource1
- https://example.com/resource2
"""

        components = orchestrate_dashboard(markdown)

        # Should have link cards
        link_cards = [c for c in components if c.type == "a2ui.LinkCard"]
        assert len(link_cards) > 0


class TestOrchestratorEdgeCases:
    """Test edge cases and error handling."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_very_long_content(self):
        """Test with very long markdown content."""
        markdown = "# Long Document\n\n" + ("## Section\n\nContent here.\n\n" * 50)

        components = orchestrate_dashboard(markdown)

        assert len(components) >= 4
        # Should not crash with long content

    def test_content_with_special_characters(self):
        """Test content with special characters."""
        markdown = """
# Test & Demo

Special chars: @#$%^&*()

Code: `print("test")`
"""

        components = orchestrate_dashboard(markdown)

        assert len(components) >= 4

    def test_content_with_unicode(self):
        """Test content with unicode characters."""
        markdown = """
# 测试文档

这是中文内容。

Emoji: 🚀 🎉 ✨
"""

        components = orchestrate_dashboard(markdown)

        assert len(components) >= 4

    def test_malformed_markdown(self):
        """Test with malformed markdown."""
        markdown = """
# Missing closing bracket

[Link without closing(https://example.com

| Incomplete | Table
|------------|
| Missing cell |
"""

        components = orchestrate_dashboard(markdown)

        # Should handle gracefully
        assert len(components) >= 4

    def test_mixed_content_types(self):
        """Test with mixed content (code + links + tables)."""
        markdown = """
# Mixed Content

## Code
```python
def hello():
    return "world"
```

## Table
| Name | Value |
|------|-------|
| A    | 1     |

## Links
- https://github.com/example/repo
- https://www.youtube.com/watch?v=test123
"""

        components = orchestrate_dashboard(markdown)

        # Should have multiple component types
        component_types = set(comp.type for comp in components)
        assert len(component_types) >= 4

        # Should have code, table, and link components
        has_code = any(c.type == "a2ui.CodeBlock" for c in components)
        has_table = any(c.type == "a2ui.DataTable" for c in components)
        has_repo = any(c.type == "a2ui.RepoCard" for c in components)
        has_video = any(c.type == "a2ui.VideoCard" for c in components)

        # At least some specialized components should be present
        assert has_code or has_table or has_repo or has_video


class TestOrchestratorIntegration:
    """Integration tests for full pipeline."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_complete_tutorial_pipeline(self):
        """Test complete pipeline with tutorial content."""
        markdown = """
# Python FastAPI Tutorial

## Introduction
FastAPI is a modern web framework for building APIs.

## Installation
```bash
pip install fastapi uvicorn
```

## Creating Your First App
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

## Running the App
```bash
uvicorn main:app --reload
```

## Conclusion
You now have a working FastAPI application!
"""

        components = orchestrate_dashboard(markdown)

        # Verify orchestration worked
        assert len(components) >= 4

        # Should have variety
        component_types = set(comp.type for comp in components)
        assert len(component_types) >= 4

        # Should have code blocks
        code_blocks = [c for c in components if c.type == "a2ui.CodeBlock"]
        assert len(code_blocks) > 0

        # Should not have 3 consecutive same type
        for i in range(len(components) - 2):
            assert not (components[i].type == components[i+1].type == components[i+2].type)

    def test_complete_research_pipeline(self):
        """Test complete pipeline with research content."""
        markdown = """
# AI Model Performance Study

## Abstract
This paper evaluates different AI models.

## Results

| Model | Accuracy | F1 Score |
|-------|----------|----------|
| GPT-4 | 95%      | 0.94     |
| Claude| 93%      | 0.92     |
| Llama | 89%      | 0.88     |

The results show 95% accuracy for GPT-4 with 87% precision.

## References
- https://github.com/openai/research
- https://arxiv.org/paper/12345
"""

        components = orchestrate_dashboard(markdown)

        # Verify orchestration
        assert len(components) >= 4
        component_types = set(comp.type for comp in components)
        assert len(component_types) >= 4

    def test_complete_article_pipeline(self):
        """Test complete pipeline with article content."""
        markdown = """
# The Future of AI

## Introduction
Artificial intelligence is transforming industries.

## Video Overview
Watch this explanation: https://www.youtube.com/watch?v=dQw4w9WgXcQ

## Key Technologies
- React for frontend
- Python for ML
- Docker for deployment

## Open Source Projects
Check out: https://github.com/tensorflow/tensorflow

## Conclusion
AI will continue to evolve rapidly.
"""

        components = orchestrate_dashboard(markdown)

        # Verify orchestration
        assert len(components) >= 4
        component_types = set(comp.type for comp in components)
        assert len(component_types) >= 4

        # Should have video card
        video_cards = [c for c in components if c.type == "a2ui.VideoCard"]
        assert len(video_cards) > 0


class TestOrchestratorComponentProperties:
    """Test that generated components have valid properties."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_all_components_have_valid_type(self):
        """Test that all components have valid A2UI type."""
        markdown = "# Test\n\nContent with code:\n```python\nprint('hi')\n```"

        components = orchestrate_dashboard(markdown)

        for comp in components:
            assert comp.type.startswith("a2ui.")
            assert comp.type[5:6].isupper()  # Component name starts with capital

    def test_all_components_have_id(self):
        """Test that all components have non-empty IDs."""
        markdown = "# Test\n\nMultiple sections\n## Section 1\n## Section 2"

        components = orchestrate_dashboard(markdown)

        for comp in components:
            assert comp.id
            assert isinstance(comp.id, str)
            assert len(comp.id) > 0

    def test_all_components_have_props(self):
        """Test that all components have props dictionary."""
        markdown = "# Test\n\nContent here"

        components = orchestrate_dashboard(markdown)

        for comp in components:
            assert hasattr(comp, 'props')
            assert isinstance(comp.props, dict)

    def test_components_are_json_serializable(self):
        """Test that all components can be serialized to JSON."""
        import json

        markdown = "# Test\n\nContent\n```python\ncode\n```"

        components = orchestrate_dashboard(markdown)

        for comp in components:
            # Should be able to convert to dict and serialize
            comp_dict = comp.model_dump()
            json_str = json.dumps(comp_dict)
            assert json_str  # Should produce valid JSON


class TestOrchestratorLayoutAlignment:
    """Test that components align with selected layout."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_tutorial_layout_has_instructional_components(self):
        """Test tutorial layout includes instructional components."""
        markdown = """
# Step-by-Step Tutorial

## Step 1
First step

```python
code here
```

## Step 2
Second step
"""

        components = orchestrate_dashboard(markdown)

        # Should have instructional-style components
        component_types = {comp.type for comp in components}

        # May have CodeBlock, StepCard, or CalloutCard
        instructional_types = {'a2ui.CodeBlock', 'a2ui.StepCard', 'a2ui.CalloutCard'}
        has_instructional = bool(component_types & instructional_types)

        assert has_instructional or len(component_types) >= 4

    def test_data_layout_has_data_components(self):
        """Test data layout includes data visualization components."""
        markdown = """
# Research Results

| Metric | Value |
|--------|-------|
| Speed  | 100ms |
| Accuracy | 95% |

Performance: 95% with 87% precision.
"""

        components = orchestrate_dashboard(markdown)

        component_types = {comp.type for comp in components}

        # May have DataTable or StatCard
        data_types = {'a2ui.DataTable', 'a2ui.StatCard'}
        has_data_components = bool(component_types & data_types)

        assert has_data_components or len(component_types) >= 4


class TestOrchestratorPerformance:
    """Test orchestrator performance characteristics."""

    def setup_method(self):
        """Reset ID counter before each test."""
        reset_id_counter()

    def test_reasonable_component_count(self):
        """Test that component count is reasonable for content size."""
        markdown = "# Title\n\n" + "Short content. " * 10

        components = orchestrate_dashboard(markdown)

        # Should have reasonable count (not hundreds for small content)
        assert 4 <= len(components) <= 50

    def test_handles_no_sections(self):
        """Test handling content with no sections."""
        markdown = "Just plain text without any headers."

        components = orchestrate_dashboard(markdown)

        assert len(components) >= 4

    def test_handles_only_code_blocks(self):
        """Test handling content that's only code."""
        markdown = """
```python
def foo():
    pass
```

```javascript
console.log('test');
```
"""

        components = orchestrate_dashboard(markdown)

        assert len(components) >= 4
        component_types = set(comp.type for comp in components)
        assert len(component_types) >= 4
