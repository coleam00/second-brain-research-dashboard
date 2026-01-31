"""
Tests for Prompts Module.

Comprehensive test suite for prompts.py covering:
- Prompt template formatting
- Helper function behavior
- Variety validation
- Content truncation
- Edge cases and error handling
"""

import pytest
from prompts import (
    CONTENT_ANALYSIS_PROMPT,
    LAYOUT_SELECTION_PROMPT,
    COMPONENT_SELECTION_PROMPT,
    format_content_analysis_prompt,
    format_layout_selection_prompt,
    format_component_selection_prompt,
    validate_component_variety,
)


class TestPromptTemplates:
    """Test suite for raw prompt templates."""

    def test_content_analysis_prompt_structure(self):
        """Test that content analysis prompt has required sections."""
        assert "Document to Analyze" in CONTENT_ANALYSIS_PROMPT
        assert "document_type" in CONTENT_ANALYSIS_PROMPT
        assert "tutorial" in CONTENT_ANALYSIS_PROMPT
        assert "research" in CONTENT_ANALYSIS_PROMPT
        assert "article" in CONTENT_ANALYSIS_PROMPT
        assert "guide" in CONTENT_ANALYSIS_PROMPT
        assert "notes" in CONTENT_ANALYSIS_PROMPT
        assert "technical_doc" in CONTENT_ANALYSIS_PROMPT
        assert "overview" in CONTENT_ANALYSIS_PROMPT

    def test_content_analysis_prompt_has_entity_types(self):
        """Test that content analysis prompt mentions all entity types."""
        assert "Technologies" in CONTENT_ANALYSIS_PROMPT
        assert "Tools" in CONTENT_ANALYSIS_PROMPT
        assert "Programming Languages" in CONTENT_ANALYSIS_PROMPT
        assert "Key Concepts" in CONTENT_ANALYSIS_PROMPT

    def test_content_analysis_prompt_has_examples(self):
        """Test that content analysis prompt includes example output."""
        assert "Example Output Structure" in CONTENT_ANALYSIS_PROMPT
        assert "FastAPI" in CONTENT_ANALYSIS_PROMPT  # Example technology
        assert "confidence" in CONTENT_ANALYSIS_PROMPT
        assert "reasoning" in CONTENT_ANALYSIS_PROMPT

    def test_layout_selection_prompt_structure(self):
        """Test that layout selection prompt has all layout types."""
        assert "instructional_layout" in LAYOUT_SELECTION_PROMPT
        assert "data_layout" in LAYOUT_SELECTION_PROMPT
        assert "news_layout" in LAYOUT_SELECTION_PROMPT
        assert "list_layout" in LAYOUT_SELECTION_PROMPT
        assert "summary_layout" in LAYOUT_SELECTION_PROMPT
        assert "reference_layout" in LAYOUT_SELECTION_PROMPT
        assert "media_layout" in LAYOUT_SELECTION_PROMPT

    def test_layout_selection_prompt_has_criteria(self):
        """Test that layout selection prompt includes selection criteria."""
        assert "Content Structure" in LAYOUT_SELECTION_PROMPT
        assert "Document Type" in LAYOUT_SELECTION_PROMPT
        assert "User Intent" in LAYOUT_SELECTION_PROMPT
        assert "Content Length" in LAYOUT_SELECTION_PROMPT

    def test_component_selection_prompt_structure(self):
        """Test that component selection prompt has component categories."""
        assert "News & Trends Components" in COMPONENT_SELECTION_PROMPT
        assert "Media Components" in COMPONENT_SELECTION_PROMPT
        assert "Data & Statistics Components" in COMPONENT_SELECTION_PROMPT
        assert "List & Navigation Components" in COMPONENT_SELECTION_PROMPT
        assert "Resource & Link Components" in COMPONENT_SELECTION_PROMPT
        assert "People & Social Components" in COMPONENT_SELECTION_PROMPT
        assert "Summary Components" in COMPONENT_SELECTION_PROMPT
        assert "Instructional Components" in COMPONENT_SELECTION_PROMPT
        assert "Comparison Components" in COMPONENT_SELECTION_PROMPT
        assert "Layout Components" in COMPONENT_SELECTION_PROMPT
        assert "Tagging Components" in COMPONENT_SELECTION_PROMPT

    def test_component_selection_prompt_has_variety_rules(self):
        """Test that component selection prompt includes variety enforcement."""
        assert "VARIETY ENFORCEMENT RULES" in COMPONENT_SELECTION_PROMPT
        assert "Minimum Component Type Diversity" in COMPONENT_SELECTION_PROMPT
        assert "No Consecutive Repetition" in COMPONENT_SELECTION_PROMPT
        assert "at least 4 DIFFERENT component types" in COMPONENT_SELECTION_PROMPT
        assert "Never place 3+ components of the same type consecutively" in COMPONENT_SELECTION_PROMPT

    def test_component_selection_prompt_has_examples(self):
        """Test that component selection prompt includes good and bad examples."""
        assert "Example Good Selection" in COMPONENT_SELECTION_PROMPT
        assert "Example Bad Selection" in COMPONENT_SELECTION_PROMPT
        assert "AVOID" in COMPONENT_SELECTION_PROMPT


class TestContentAnalysisPromptFormatting:
    """Test suite for content analysis prompt formatting."""

    def test_format_simple_markdown(self):
        """Test formatting with simple markdown content."""
        markdown = "# Test Document\n\nThis is a test."
        result = format_content_analysis_prompt(markdown)

        assert "# Test Document" in result
        assert "This is a test." in result
        assert "Document to Analyze" in result

    def test_format_long_markdown_truncates(self):
        """Test that very long markdown content is truncated."""
        # Create content longer than 8000 characters
        markdown = "# Test\n\n" + ("This is a very long document. " * 500)
        result = format_content_analysis_prompt(markdown)

        assert "content truncated" in result
        assert len(result) < len(markdown) + 1000  # Should be truncated

    def test_format_empty_markdown(self):
        """Test formatting with empty markdown."""
        result = format_content_analysis_prompt("")

        assert "Document to Analyze" in result
        assert "{markdown_content}" not in result  # Should be replaced

    def test_format_special_characters(self):
        """Test formatting with special characters in markdown."""
        markdown = "# Test\n\n**Bold** and *italic* and `code`"
        result = format_content_analysis_prompt(markdown)

        assert "**Bold**" in result
        assert "*italic*" in result
        assert "`code`" in result

    def test_format_code_blocks(self):
        """Test formatting with code blocks in markdown."""
        markdown = """# Test

```python
def hello():
    print("world")
```
"""
        result = format_content_analysis_prompt(markdown)

        assert "```python" in result
        assert 'def hello():' in result


class TestLayoutSelectionPromptFormatting:
    """Test suite for layout selection prompt formatting."""

    def test_format_complete_content_analysis(self):
        """Test formatting with complete content analysis data."""
        content_analysis = {
            'document_type': 'tutorial',
            'title': 'Python Basics',
            'sections': ['Introduction', 'Setup', 'First Program'],
            'code_blocks': [{'language': 'python', 'code': 'print("hello")'}],
            'tables': [],
            'links': ['https://python.org'],
            'youtube_links': [],
            'github_links': ['https://github.com/test/repo'],
            'entities': {
                'technologies': ['Python', 'pip'],
                'tools': ['VS Code'],
                'languages': ['Python'],
                'concepts': ['Programming Basics']
            }
        }

        result = format_layout_selection_prompt(content_analysis)

        assert 'tutorial' in result
        assert 'Python Basics' in result
        assert '3 sections' in result
        assert '1 code blocks' in result
        assert 'Python' in result
        assert 'Available Layout Types' in result

    def test_format_minimal_content_analysis(self):
        """Test formatting with minimal content analysis data."""
        content_analysis = {
            'document_type': 'unknown',
            'title': 'Untitled'
        }

        result = format_layout_selection_prompt(content_analysis)

        assert 'unknown' in result
        assert 'Untitled' in result
        assert '0 sections' in result
        assert '0 code blocks' in result

    def test_format_empty_entities(self):
        """Test formatting when entities are empty."""
        content_analysis = {
            'document_type': 'article',
            'title': 'Test Article',
            'entities': {
                'technologies': [],
                'tools': [],
                'languages': [],
                'concepts': []
            }
        }

        result = format_layout_selection_prompt(content_analysis)

        # Should handle empty lists gracefully
        assert 'Technologies:' in result
        assert 'Tools:' in result

    def test_format_many_entities_truncates(self):
        """Test that many entities are truncated to first 10."""
        content_analysis = {
            'document_type': 'technical_doc',
            'title': 'Tech Stack',
            'entities': {
                'technologies': [f'Tech{i}' for i in range(20)],
                'tools': ['Tool1', 'Tool2'],
                'languages': ['Python'],
                'concepts': ['Concept1']
            }
        }

        result = format_layout_selection_prompt(content_analysis)

        # Should only show first 10 technologies
        assert 'Tech0' in result
        assert 'Tech9' in result
        # Should not show later ones in the truncated view
        # (they might appear elsewhere, but not in the list)


class TestComponentSelectionPromptFormatting:
    """Test suite for component selection prompt formatting."""

    def test_format_complete_data(self):
        """Test formatting with complete content analysis and layout decision."""
        content_analysis = {
            'document_type': 'tutorial',
            'title': 'FastAPI Tutorial',
            'sections': ['Intro', 'Setup', 'Hello World', 'Database', 'Deployment'],
            'code_blocks': [{'language': 'python', 'code': 'test'}] * 5,
            'tables': [{'headers': ['A', 'B'], 'rows': [['1', '2']]}],
            'links': ['https://example.com'] * 3,
            'youtube_links': ['https://youtube.com/watch?v=test'],
            'github_links': ['https://github.com/test/repo']
        }

        layout_decision = {
            'layout_type': 'instructional_layout',
            'confidence': 0.95,
            'reasoning': 'Tutorial format with code examples',
            'alternative_layouts': ['reference_layout', 'list_layout'],
            'component_suggestions': ['CodeBlock', 'StepCard', 'CalloutCard']
        }

        result = format_component_selection_prompt(content_analysis, layout_decision)

        assert 'tutorial' in result
        assert 'FastAPI Tutorial' in result
        assert 'instructional_layout' in result
        assert '0.95' in result
        assert 'Tutorial format with code examples' in result
        assert 'CodeBlock' in result

    def test_format_shows_first_5_sections(self):
        """Test that only first 5 sections are shown."""
        content_analysis = {
            'document_type': 'guide',
            'title': 'Long Guide',
            'sections': [f'Section {i}' for i in range(20)]
        }

        layout_decision = {
            'layout_type': 'list_layout',
            'confidence': 0.8,
            'reasoning': 'Many sections'
        }

        result = format_component_selection_prompt(content_analysis, layout_decision)

        assert 'Section 0' in result
        assert 'Section 4' in result
        assert '(showing first 5)' in result

    def test_format_handles_missing_fields(self):
        """Test formatting when some fields are missing."""
        content_analysis = {'title': 'Test'}
        layout_decision = {'layout_type': 'summary_layout'}

        result = format_component_selection_prompt(content_analysis, layout_decision)

        assert 'Test' in result
        assert 'summary_layout' in result
        assert 'unknown' in result  # Default for missing document_type


class TestComponentVarietyValidation:
    """Test suite for component variety validation."""

    def test_valid_diverse_components(self):
        """Test validation passes for diverse components."""
        components = [
            {'component_type': 'TLDR'},
            {'component_type': 'StatCard'},
            {'component_type': 'CodeBlock'},
            {'component_type': 'StepCard'},
            {'component_type': 'LinkCard'},
        ]

        result = validate_component_variety(components)

        assert result['valid'] is True
        assert result['unique_types_count'] == 5
        assert result['max_consecutive_same_type'] == 1
        assert result['meets_min_types'] is True
        assert result['meets_no_consecutive'] is True
        assert len(result['violations']) == 0

    def test_invalid_too_few_types(self):
        """Test validation fails when too few unique types."""
        components = [
            {'component_type': 'StatCard'},
            {'component_type': 'StatCard'},
            {'component_type': 'CodeBlock'},
            {'component_type': 'CodeBlock'},
        ]

        result = validate_component_variety(components)

        assert result['valid'] is False
        assert result['unique_types_count'] == 2
        assert result['meets_min_types'] is False
        assert 'Only 2 unique types' in result['violations'][0]

    def test_invalid_too_many_consecutive(self):
        """Test validation fails with 3+ consecutive same type."""
        components = [
            {'component_type': 'StatCard'},
            {'component_type': 'StatCard'},
            {'component_type': 'StatCard'},
            {'component_type': 'CodeBlock'},
            {'component_type': 'LinkCard'},
            {'component_type': 'TLDR'},
        ]

        result = validate_component_variety(components)

        assert result['valid'] is False
        assert result['max_consecutive_same_type'] == 3
        assert result['meets_no_consecutive'] is False
        assert 'consecutive same type' in result['violations'][0]

    def test_edge_case_exactly_2_consecutive(self):
        """Test that exactly 2 consecutive is allowed."""
        components = [
            {'component_type': 'StatCard'},
            {'component_type': 'StatCard'},
            {'component_type': 'CodeBlock'},
            {'component_type': 'LinkCard'},
            {'component_type': 'TLDR'},
        ]

        result = validate_component_variety(components)

        assert result['valid'] is True
        assert result['max_consecutive_same_type'] == 2
        assert result['meets_no_consecutive'] is True

    def test_edge_case_exactly_4_types(self):
        """Test that exactly 4 unique types meets minimum."""
        components = [
            {'component_type': 'Type1'},
            {'component_type': 'Type2'},
            {'component_type': 'Type3'},
            {'component_type': 'Type4'},
        ]

        result = validate_component_variety(components)

        assert result['valid'] is True
        assert result['unique_types_count'] == 4
        assert result['meets_min_types'] is True

    def test_empty_components_list(self):
        """Test validation handles empty component list."""
        result = validate_component_variety([])

        assert result['valid'] is False
        assert result['unique_types_count'] == 0
        assert 'No components provided' in result['violations']

    def test_component_type_distribution(self):
        """Test that component type distribution is calculated correctly."""
        components = [
            {'component_type': 'StatCard'},
            {'component_type': 'StatCard'},
            {'component_type': 'StatCard'},
            {'component_type': 'CodeBlock'},
            {'component_type': 'CodeBlock'},
            {'component_type': 'LinkCard'},
            {'component_type': 'TLDR'},
        ]

        result = validate_component_variety(components)

        distribution = result['component_type_distribution']
        assert distribution['StatCard'] == 3
        assert distribution['CodeBlock'] == 2
        assert distribution['LinkCard'] == 1
        assert distribution['TLDR'] == 1

    def test_long_consecutive_sequence(self):
        """Test validation catches long consecutive sequences."""
        components = [
            {'component_type': 'StatCard'},
            {'component_type': 'StatCard'},
            {'component_type': 'StatCard'},
            {'component_type': 'StatCard'},
            {'component_type': 'StatCard'},
            {'component_type': 'CodeBlock'},
            {'component_type': 'LinkCard'},
            {'component_type': 'TLDR'},
        ]

        result = validate_component_variety(components)

        assert result['valid'] is False
        assert result['max_consecutive_same_type'] == 5
        assert 'Found 5 consecutive same type' in result['violations'][0]


class TestPromptIntegration:
    """Integration tests for prompt templates."""

    def test_full_pipeline_tutorial_document(self):
        """Test complete prompt pipeline for tutorial document."""
        # Sample markdown
        markdown = """# Python FastAPI Tutorial

Learn how to build REST APIs with FastAPI.

## Setup

```python
pip install fastapi uvicorn
```

## Hello World

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

## Run the app

```bash
uvicorn main:app --reload
```
"""

        # Step 1: Format content analysis prompt
        content_prompt = format_content_analysis_prompt(markdown)
        assert "Python FastAPI Tutorial" in content_prompt
        assert "pip install fastapi" in content_prompt

        # Step 2: Simulate content analysis result
        content_analysis = {
            'document_type': 'tutorial',
            'title': 'Python FastAPI Tutorial',
            'sections': ['Setup', 'Hello World', 'Run the app'],
            'code_blocks': [
                {'language': 'python', 'code': 'pip install...'},
                {'language': 'python', 'code': 'from fastapi...'},
                {'language': 'bash', 'code': 'uvicorn...'}
            ],
            'tables': [],
            'links': [],
            'youtube_links': [],
            'github_links': [],
            'entities': {
                'technologies': ['FastAPI', 'Python'],
                'tools': ['pip', 'uvicorn'],
                'languages': ['Python', 'Bash'],
                'concepts': ['REST API']
            }
        }

        # Step 3: Format layout selection prompt
        layout_prompt = format_layout_selection_prompt(content_analysis)
        assert 'tutorial' in layout_prompt
        assert '3 sections' in layout_prompt
        assert '3 code blocks' in layout_prompt

        # Step 4: Simulate layout decision
        layout_decision = {
            'layout_type': 'instructional_layout',
            'confidence': 0.95,
            'reasoning': 'Tutorial with code examples',
            'alternative_layouts': ['reference_layout'],
            'component_suggestions': ['CodeBlock', 'StepCard', 'CommandCard']
        }

        # Step 5: Format component selection prompt
        component_prompt = format_component_selection_prompt(content_analysis, layout_decision)
        assert 'instructional_layout' in component_prompt
        assert 'CodeBlock' in component_prompt
        assert 'StepCard' in component_prompt

    def test_full_pipeline_research_document(self):
        """Test complete prompt pipeline for research document."""
        markdown = """# AI Market Analysis 2025

## Executive Summary

The AI market reached $196B in 2024, with 23% YoY growth.

## Key Metrics

| Metric | 2023 | 2024 | Growth |
|--------|------|------|--------|
| Market Size | $159B | $196B | 23% |
| Users | 2.1B | 2.8B | 33% |

## Conclusion

Strong growth trajectory continues.
"""

        content_prompt = format_content_analysis_prompt(markdown)
        assert "AI Market Analysis" in content_prompt

        content_analysis = {
            'document_type': 'research',
            'title': 'AI Market Analysis 2025',
            'sections': ['Executive Summary', 'Key Metrics', 'Conclusion'],
            'code_blocks': [],
            'tables': [{'headers': ['Metric', '2023', '2024', 'Growth'], 'rows': [['Market Size', '$159B', '$196B', '23%']]}],
            'links': [],
            'youtube_links': [],
            'github_links': [],
            'entities': {
                'technologies': ['AI'],
                'tools': [],
                'languages': [],
                'concepts': ['Market Analysis']
            }
        }

        layout_prompt = format_layout_selection_prompt(content_analysis)
        assert 'research' in layout_prompt
        assert '1 tables' in layout_prompt

        layout_decision = {
            'layout_type': 'data_layout',
            'confidence': 0.90,
            'reasoning': 'Research with data tables',
            'alternative_layouts': ['summary_layout'],
            'component_suggestions': ['DataTable', 'StatCard', 'ExecutiveSummary']
        }

        component_prompt = format_component_selection_prompt(content_analysis, layout_decision)
        assert 'data_layout' in component_prompt
        assert 'DataTable' in component_prompt


class TestPromptVarietyEnforcement:
    """Test that prompts correctly explain variety enforcement."""

    def test_component_prompt_explains_min_types(self):
        """Test that component prompt explains minimum 4 types rule."""
        assert "at least 4 DIFFERENT component types" in COMPONENT_SELECTION_PROMPT
        assert "Mix structural, data, media, and interactive components" in COMPONENT_SELECTION_PROMPT

    def test_component_prompt_explains_no_consecutive(self):
        """Test that component prompt explains no 3+ consecutive rule."""
        assert "Never place 3+ components of the same type consecutively" in COMPONENT_SELECTION_PROMPT
        assert "intersperse them with other components" in COMPONENT_SELECTION_PROMPT

    def test_component_prompt_shows_bad_example(self):
        """Test that component prompt shows what NOT to do."""
        # Find the bad example section
        bad_example_start = COMPONENT_SELECTION_PROMPT.index("Example Bad Selection")
        bad_example_section = COMPONENT_SELECTION_PROMPT[bad_example_start:bad_example_start + 1000]

        assert "AVOID" in bad_example_section
        assert "violates" in bad_example_section
        assert "meets_requirements" in bad_example_section
        assert "false" in bad_example_section


class TestPromptEdgeCases:
    """Test edge cases and error handling in prompt functions."""

    def test_format_content_with_unicode(self):
        """Test formatting with unicode characters."""
        markdown = "# Test 测试\n\nEmoji: 🚀 👍"
        result = format_content_analysis_prompt(markdown)

        assert "测试" in result
        assert "🚀" in result

    def test_format_layout_with_none_values(self):
        """Test formatting when some values are None."""
        content_analysis = {
            'document_type': 'article',
            'title': 'Test',
            'sections': None,
            'code_blocks': None,
            'entities': None
        }

        # Should handle None gracefully
        result = format_layout_selection_prompt(content_analysis)
        assert 'article' in result

    def test_validate_components_with_missing_type(self):
        """Test validation when component_type is missing."""
        components = [
            {'component_type': 'StatCard'},
            {'other_field': 'value'},  # Missing component_type
            {'component_type': 'CodeBlock'},
        ]

        result = validate_component_variety(components)

        # Should handle missing type (counts as empty string)
        assert result['unique_types_count'] >= 2

    def test_format_very_long_section_list(self):
        """Test formatting with very long section list."""
        content_analysis = {
            'document_type': 'guide',
            'title': 'Complete Guide',
            'sections': [f'Section {i}' for i in range(100)]
        }

        layout_decision = {'layout_type': 'list_layout'}

        result = format_component_selection_prompt(content_analysis, layout_decision)

        # Should truncate to first 5
        assert 'Section 0' in result
        assert 'Section 4' in result
        assert '(showing first 5)' in result
