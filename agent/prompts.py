"""
Prompt Templates Module - Comprehensive prompts for content analysis and component generation.

This module provides production-quality prompt templates optimized for Claude Sonnet 4
via OpenRouter with Pydantic AI for structured output generation. All prompts include
variety enforcement instructions to ensure diverse, high-quality component generation.

The module contains three main prompt templates:
1. CONTENT_ANALYSIS_PROMPT - For analyzing and classifying Markdown documents
2. LAYOUT_SELECTION_PROMPT - For selecting optimal layouts based on content
3. COMPONENT_SELECTION_PROMPT - For generating diverse A2UI components

All prompts are designed to work with Pydantic AI's structured output capabilities,
ensuring type-safe, validated responses.
"""

# ============================================================================
# CONTENT ANALYSIS PROMPT
# ============================================================================

CONTENT_ANALYSIS_PROMPT = """You are an expert content analyst specializing in Markdown document classification and entity extraction.

Your task is to analyze the provided Markdown document and extract structured information about its content, type, and key entities.

## Document to Analyze

{markdown_content}

## Analysis Requirements

### 1. Document Classification
Classify this document into ONE of the following types based on its primary purpose and structure:

- **tutorial**: Step-by-step guides with code examples and hands-on instructions
- **research**: Academic papers, research notes, analysis, or data-driven content
- **article**: Blog posts, news articles, opinion pieces, or general writing
- **guide**: Reference documentation, comprehensive overviews, or how-to guides
- **notes**: Personal notes, quick references, or informal documentation
- **technical_doc**: API documentation, technical specifications, or developer references
- **overview**: High-level summaries, introductions, or executive briefings

**Classification Criteria:**
- Look at the document structure (headers, sections, formatting)
- Identify the primary intent (teach, inform, reference, document)
- Consider the target audience (beginners, researchers, developers, general readers)
- Analyze the content density and complexity

### 2. Entity Extraction
Extract the following entities from the document:

**Technologies**: Frameworks, platforms, libraries, services
Examples: React, TensorFlow, AWS, PostgreSQL, Docker, Kubernetes

**Tools**: Development tools, applications, utilities
Examples: VS Code, Git, npm, Webpack, Pytest, Postman

**Programming Languages**: All mentioned programming or markup languages
Examples: Python, JavaScript, TypeScript, SQL, Rust, Go

**Key Concepts**: Important topics, methodologies, patterns mentioned in headers
Examples: Machine Learning, REST API, Microservices, CI/CD

### 3. Structural Analysis
Identify:
- Main title (from first H1 header or document start)
- Number of sections and subsections
- Presence of code blocks, tables, links
- Special content types (YouTube videos, GitHub repos, diagrams)

## Output Format

Return a structured analysis with:
- `document_type`: One of the classification types above
- `title`: The main document title
- `entities`: Dictionary with keys: technologies, tools, languages, concepts
- `confidence`: Your confidence score (0.0-1.0) in the classification
- `reasoning`: Brief explanation of why you chose this classification

## Example Output Structure

```json
{{
  "document_type": "tutorial",
  "title": "Building REST APIs with FastAPI",
  "entities": {{
    "technologies": ["FastAPI", "Pydantic", "PostgreSQL"],
    "tools": ["pip", "uvicorn", "Postman"],
    "languages": ["Python", "SQL"],
    "concepts": ["REST API", "Data Validation", "Async Programming"]
  }},
  "confidence": 0.95,
  "reasoning": "Document contains step-by-step code examples with explanations, targeting developers learning FastAPI. Clear instructional structure with numbered sections."
}}
```

## Important Guidelines

1. **Be Accurate**: Choose the classification that best matches the primary document purpose
2. **Extract Comprehensively**: Don't miss important technologies or concepts
3. **Normalize Names**: Use standard capitalization (Python, not python; PostgreSQL, not postgres)
4. **Focus on Relevance**: Only extract entities that are actually discussed, not just mentioned in passing
5. **Provide Context**: Make your reasoning clear and specific to this document

Begin your analysis now."""


# ============================================================================
# LAYOUT SELECTION PROMPT
# ============================================================================

LAYOUT_SELECTION_PROMPT = """You are an expert UI/UX designer specializing in optimal layout selection for content dashboards.

Your task is to select the BEST layout type for displaying the analyzed content in a dynamic dashboard interface.

## Content Analysis

{content_analysis}

## Available Layout Types

Choose ONE of the following layout types:

### 1. instructional_layout
**Best for**: Tutorials, coding guides, step-by-step instructions
**Characteristics**:
- Emphasizes code blocks and examples
- Sequential flow with clear steps
- Progress tracking and navigation
- Collapsible sections for code
**Indicators**: High code block count (>3), numbered steps, "how-to" language

### 2. data_layout
**Best for**: Research papers, statistical analysis, data reports
**Characteristics**:
- Tables and charts prominently featured
- Metric cards for key statistics
- Comparison visualizations
- Citation and reference sections
**Indicators**: Multiple tables (>2), statistics, charts, academic language

### 3. news_layout
**Best for**: Articles, blog posts, news stories
**Characteristics**:
- Hero image/headline at top
- Article-style flow with paragraphs
- Related links sidebar
- Social sharing elements
**Indicators**: Article structure, media content, time-sensitive topics

### 4. list_layout
**Best for**: Guides, checklists, resource collections
**Characteristics**:
- Ordered or bulleted lists
- Checkboxes for action items
- Accordion sections for details
- Side navigation for jumping
**Indicators**: Many list items, actionable content, reference material

### 5. summary_layout
**Best for**: Notes, quick references, TL;DR content
**Characteristics**:
- Condensed information display
- Tag clouds and keywords
- Quick-scan cards
- Highlights and callouts
**Indicators**: Short content (<1000 chars), bullet points, informal tone

### 6. reference_layout
**Best for**: API docs, technical specifications, documentation
**Characteristics**:
- Searchable content
- Tabbed organization
- Code examples with syntax highlighting
- Detailed side navigation
**Indicators**: Many sections (>10), technical terminology, parameter tables

### 7. media_layout
**Best for**: Visual content, video tutorials, multimedia presentations
**Characteristics**:
- Video/image embeds featured prominently
- Timeline or carousel for media
- Hero sections with visuals
- Media gallery organization
**Indicators**: Multiple media links (>3), YouTube/Vimeo, image galleries

## Selection Criteria

Consider these factors in order of importance:

1. **Content Structure** (40%): What structural elements dominate?
   - Code blocks → instructional_layout
   - Tables/stats → data_layout
   - Media links → media_layout
   - Many sections → reference_layout

2. **Document Type** (30%): What is the primary purpose?
   - Tutorial → instructional_layout
   - Research → data_layout
   - Article → news_layout
   - Guide → list_layout

3. **User Intent** (20%): What will users want to do?
   - Learn by doing → instructional_layout
   - Analyze data → data_layout
   - Quick reference → summary_layout or reference_layout

4. **Content Length** (10%): How much content is there?
   - Short (<1000 chars) → summary_layout
   - Very long with many sections → reference_layout
   - Medium with steps → instructional_layout or list_layout

## Output Format

Return a structured layout selection with:
- `layout_type`: One of the 7 layout types above
- `confidence`: Your confidence score (0.0-1.0)
- `reasoning`: Detailed explanation of why this layout is optimal
- `alternative_layouts`: 2-3 fallback options ranked by suitability
- `component_priorities`: Top 5 component types to emphasize in this layout

## Example Output Structure

```json
{{
  "layout_type": "instructional_layout",
  "confidence": 0.92,
  "reasoning": "Document contains 8 code blocks with Python examples, numbered steps (1-6), and clear instructional language. The structure follows a tutorial format with prerequisites, setup, and hands-on exercises. Users will benefit from an instructional layout with collapsible code sections and progress tracking.",
  "alternative_layouts": ["reference_layout", "list_layout"],
  "component_priorities": ["CodeBlock", "StepCard", "CalloutCard", "CommandCard", "TableOfContents"]
}}
```

## Important Guidelines

1. **Choose Decisively**: Pick the SINGLE best layout, not a compromise
2. **Explain Clearly**: Reference specific content characteristics in your reasoning
3. **Consider User Experience**: Think about how users will consume this content
4. **Provide Fallbacks**: Alternative layouts should be genuinely suitable backups
5. **Prioritize Components**: List components that will make this layout most effective

Begin your layout selection now."""


# ============================================================================
# COMPONENT SELECTION PROMPT
# ============================================================================

COMPONENT_SELECTION_PROMPT = """You are an expert A2UI component architect specializing in creating diverse, engaging dashboard interfaces.

Your task is to select and configure the OPTIMAL set of A2UI components to represent the analyzed content in an engaging, scannable dashboard.

## Content Analysis

{content_analysis}

## Selected Layout

{layout_decision}

## Available A2UI Component Types

### News & Trends Components
- **HeadlineCard**: Breaking news, important announcements, featured content
- **TrendIndicator**: Trends, metrics with direction (up/down/stable)
- **TimelineEvent**: Chronological events, version history, milestones
- **NewsTicker**: Live updates, rolling news, status messages

### Media Components
- **VideoCard**: YouTube, Vimeo, or video platform embeds
- **ImageCard**: Featured images, diagrams, screenshots
- **PlaylistCard**: Video/audio playlists, course modules
- **PodcastCard**: Podcast episodes, audio content

### Data & Statistics Components
- **StatCard**: Key metrics, KPIs, important numbers
- **MetricRow**: Multiple related metrics in a row
- **ProgressRing**: Circular progress indicators, completion percentages
- **ComparisonBar**: Side-by-side metric comparisons
- **DataTable**: Structured tabular data with headers
- **MiniChart**: Small inline charts (sparklines)

### List & Navigation Components
- **RankedItem**: Numbered lists, top N items, rankings
- **ChecklistItem**: To-do items, action items, steps
- **ProConItem**: Pros/cons lists, advantages/disadvantages
- **BulletPoint**: Simple bulleted list items

### Resource & Link Components
- **LinkCard**: External links, references, resources
- **ToolCard**: Software tools, applications, utilities
- **BookCard**: Books, papers, reading materials
- **RepoCard**: GitHub repositories, code projects

### People & Social Components
- **ProfileCard**: Author profiles, contributors, experts
- **CompanyCard**: Companies, organizations, brands
- **QuoteCard**: Quotes, testimonials, feedback
- **ExpertTip**: Tips, advice, best practices from experts

### Summary Components
- **TLDR**: Too Long; Didn't Read summaries
- **KeyTakeaways**: Main points, key learnings (3-5 items)
- **ExecutiveSummary**: High-level overview for decision makers
- **TableOfContents**: Navigation for long documents

### Instructional Components
- **StepCard**: Numbered tutorial steps with descriptions
- **CodeBlock**: Code examples with syntax highlighting
- **CalloutCard**: Important notes, warnings, tips, info boxes
- **CommandCard**: Terminal commands, CLI instructions

### Comparison Components
- **ComparisonTable**: Feature comparison across products/options
- **VsCard**: Head-to-head comparisons (A vs B)
- **FeatureMatrix**: Feature availability across tiers/versions
- **PricingTable**: Pricing tiers, subscription plans

### Layout Components
- **Section**: Group related components with optional title (use sparingly for major content groups)

### Tagging Components
- **TagCloud**: Collection of related tags with optional counts and sizing
- **CategoryBadge**: Category label with optional icon and color
- **StatusIndicator**: Status with colored dot indicator (active, inactive, pending, error)
- **PriorityBadge**: Priority level badge (low, medium, high, critical)
- **DifficultyBadge**: Difficulty level badge (beginner, intermediate, advanced, expert)

## COMPREHENSIVE COVERAGE RULES (CRITICAL)

You MUST follow these rules to ensure thorough content representation:

### Rule 1: Cover ALL Major Content Sections
- **Generate a component for EVERY major section/topic in the document**
- If document has 10 sections/topics, generate components for ALL 10, not just 2-3
- Bullet points WITHIN a section should be collapsed into a SINGLE component (KeyTakeaways, CalloutCard, or ChecklistItem) — do NOT create one RankedItem per bullet point
- Only use RankedItem for content that is explicitly ranked/ordered (e.g., "Top 10 tools")
- Minimum: Generate 1-2 components per major section + summary components

### Rule 2: Scale With Document Size
- Short documents (< 500 words): 5-8 components
- Medium documents (500-2000 words): 10-15 components
- Long documents (2000+ words): 15-25 components
- IMPORTANT: Stay within these ranges. More is NOT better — aim for information density per component.

### Rule 3: Minimum Component Type Diversity
- **Generate at least 4 DIFFERENT component types** in your selection
- Do NOT create 10 components of only 2-3 types
- Mix structural, data, media, and interactive components

### Rule 4: No Consecutive Repetition
- **Never place 3+ components of the same type consecutively**
- If you need multiple StatCards, intersperse them with other components
- Break up patterns with different component types

### Rule 5: Balanced Distribution
- Aim for 2-4 instances of your most-used component type
- Include 1-2 instances of several other component types
- Avoid having one component type dominate (>50% of components)

### Rule 6: Width Hints
For each component, you may suggest a `width_hint` in the props to control layout:
- **"full"**: Spans entire width - use for code blocks, tables, summaries, executive content
- **"half"**: Half width (2 columns on desktop) - use for callouts, key points, quotes
- **"third"**: Third width (3 columns on desktop) - use for stat cards, link cards, repo cards
- **"quarter"**: Small items - use for badges, tags

Default widths are applied if not specified, but you can override for visual balance.
Group similar-width components together when possible.

### Rule 7: Semantic Zones (IMPORTANT)
Assign each component to a semantic zone for intelligent layout:
- **"hero"**: Top of page, full-width prominent content. Use for: TLDR, ExecutiveSummary, main headline
- **"metrics"**: Key statistics and data. Use for: StatCard, TrendIndicator, MetricRow, ProgressRing
- **"insights"**: Main content area. Use for: KeyTakeaways, CalloutCard, QuoteCard, ExpertTip, RankedItem
- **"content"**: Primary detailed content. Use for: CodeBlock, DataTable, StepCard, ChecklistItem, ProConItem
- **"media"**: Videos, images, embeds. Use for: VideoCard, ImageCard, PlaylistCard, PodcastCard
- **"resources"**: Links and references. Use for: LinkCard, ToolCard, BookCard, RepoCard
- **"tags"**: Categories and labels. Use for: TagCloud, CategoryBadge, StatusIndicator

Components in the same zone will be grouped together visually. Use zones to create a clear visual hierarchy.

## Component Selection Strategy

Follow this process:

### Step 1: Identify Key Content Elements
- What are the most important pieces of information?
- What content types are present? (code, data, media, text)
- What's the primary user goal? (learn, reference, consume)

### Step 2: Map Content to Components
- Code blocks → CodeBlock
- Statistics/metrics → StatCard, MetricRow, ComparisonBar
- Links → LinkCard, ToolCard, RepoCard, BookCard
- Steps/procedures → StepCard, ChecklistItem
- Media → VideoCard, ImageCard
- Summaries → TLDR, KeyTakeaways, ExecutiveSummary

### Step 2b: Content Pattern Matching (IMPORTANT)
Match these content patterns to the BEST component type:
- Direct quotes with attribution → **QuoteCard** (NOT RankedItem or BulletPoint)
- News stories with dates/sources → **HeadlineCard** (with appropriate sentiment: positive/negative/neutral)
- Statistics with numbers/percentages → **StatCard** or **TrendIndicator**
- Chronological events, upcoming dates, or timelines → **TimelineEvent**
- Named people with roles/titles → **ProfileCard**
- Lists of resources/tools with URLs → **ToolCard** or **LinkCard**
- Pro/con or advantage/disadvantage content → **ProConItem**
- Step-by-step instructions → **StepCard**
- Grouped short items (funding rounds, product launches) → **CalloutCard** with grouped content
- Expert tips or advice → **ExpertTip**
- Key statistics in a group → **MetricRow** for related metrics together

### Sentiment Guidelines for HeadlineCards
Assign accurate sentiment:
- **positive**: achievements, breakthroughs, funding, launches, growth, improvements, open-source releases
- **negative**: failures, layoffs, bans, restrictions, losses, declines, security breaches
- **neutral**: policy announcements without clear positive/negative framing, mixed outcomes
Do NOT default everything to "neutral" - analyze the actual tone of the content.

### Step 3: Enforce Variety
- Check component type counts
- Insert different component types to break up repetition
- Add complementary components (e.g., TableOfContents for long content)

### Step 4: Organize with Layout Components
- Group related components in Sections
- Use Grid for card-based content
- Use Accordion for lengthy collapsible content
- Use Tabs for categorized information

## Output Format

Return a JSON array of component specifications:

```json
{{
  "components": [
    {{
      "component_type": "TLDR",
      "priority": "high",
      "zone": "hero",
      "data_source": "summary of first 2-3 paragraphs",
      "props": {{
        "content": "Brief TL;DR summary text",
        "max_length": 200,
        "width_hint": "full"
      }},
      "rationale": "Provides quick overview at document start"
    }},
    {{
      "component_type": "StatCard",
      "priority": "high",
      "zone": "metrics",
      "data_source": "extract number from 'Market size: $196B' mention",
      "props": {{
        "value": "$196B",
        "label": "AI Market Size",
        "trend": "up",
        "trendValue": "+23%",
        "width_hint": "third"
      }},
      "rationale": "Highlights key market metric"
    }},
    {{
      "component_type": "StatCard",
      "priority": "high",
      "zone": "metrics",
      "props": {{
        "value": "45%",
        "label": "Growth Rate",
        "trend": "up",
        "trendValue": "+5%",
        "width_hint": "third"
      }},
      "rationale": "Shows growth alongside market size"
    }},
    {{
      "component_type": "KeyTakeaways",
      "priority": "high",
      "zone": "insights",
      "props": {{
        "items": ["Key point 1", "Key point 2", "Key point 3"],
        "width_hint": "half"
      }},
      "rationale": "Summarizes main points"
    }}
  ],
  "variety_check": {{
    "unique_types_count": 3,
    "max_consecutive_same_type": 2,
    "meets_requirements": true
  }}
}}
```

## Example Good Selection (DIVERSE with ZONES)

```json
{{
  "components": [
    {{"component_type": "TLDR", "zone": "hero", "priority": "high", "props": {{"width_hint": "full"}}}},
    {{"component_type": "StatCard", "zone": "metrics", "priority": "high", "props": {{"width_hint": "third"}}}},
    {{"component_type": "StatCard", "zone": "metrics", "priority": "high", "props": {{"width_hint": "third"}}}},
    {{"component_type": "TrendIndicator", "zone": "metrics", "priority": "medium", "props": {{"width_hint": "third"}}}},
    {{"component_type": "KeyTakeaways", "zone": "insights", "priority": "medium", "props": {{"width_hint": "half"}}}},
    {{"component_type": "CalloutCard", "zone": "insights", "priority": "medium", "props": {{"width_hint": "half"}}}},
    {{"component_type": "CodeBlock", "zone": "content", "priority": "high", "props": {{"width_hint": "full"}}}},
    {{"component_type": "StepCard", "zone": "content", "priority": "high", "props": {{"width_hint": "full"}}}},
    {{"component_type": "LinkCard", "zone": "resources", "priority": "medium", "props": {{"width_hint": "third"}}}},
    {{"component_type": "RepoCard", "zone": "resources", "priority": "medium", "props": {{"width_hint": "third"}}}}
  ],
  "variety_check": {{
    "unique_types_count": 8,
    "max_consecutive_same_type": 2,
    "meets_requirements": true
  }}
}}
```

## Example Bad Selection (AVOID - NOT DIVERSE)

```json
{{
  "components": [
    {{"component_type": "StatCard"}},
    {{"component_type": "StatCard"}},
    {{"component_type": "StatCard"}},
    {{"component_type": "StatCard"}},
    {{"component_type": "StatCard"}},
    {{"component_type": "StatCard"}},
    {{"component_type": "CodeBlock"}},
    {{"component_type": "CodeBlock"}},
    {{"component_type": "CodeBlock"}},
    {{"component_type": "CodeBlock"}}
  ],
  "variety_check": {{
    "unique_types_count": 2,
    "max_consecutive_same_type": 6,
    "meets_requirements": false
  }}
}}
```
❌ This violates BOTH variety rules!

## Important Guidelines

1. **COMPREHENSIVE COVERAGE**: Generate a component for EVERY major section — do NOT skip sections after the first few
2. **Diversity First**: Aim for 6-8 different component types minimum. No single type should exceed 40% of total.
3. **Break Up Patterns**: Never have more than 2 consecutive identical components
4. **Use Width Hints**: Specify width_hint for visual balance (third for stats, full for code/tables, half for callouts)
5. **Use Semantic Zones**: ALWAYS assign a zone to each component (hero, metrics, insights, content, media, resources, tags)
6. **Match Content to Best Type**: Use QuoteCard for quotes, HeadlineCard for news, StatCard for numbers, TimelineEvent for events
7. **Provide Complete Props**: Include all necessary data for each component
8. **Consolidate Lists**: Bullet points within a section go into ONE component (KeyTakeaways, CalloutCard) — not one RankedItem per bullet
9. **Stay in Range**: 15-25 components for long documents. More is not better.

Begin your component selection now."""


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def format_content_analysis_prompt(markdown_content: str) -> str:
    """
    Format the content analysis prompt with actual markdown content.

    Args:
        markdown_content: Raw markdown document to analyze

    Returns:
        Formatted prompt string ready for LLM
    """
    # Truncate very long content to stay within token limits
    # Claude Haiku 4.5 has 200k context window; 30k chars is ~7500 tokens
    max_length = 30000
    if len(markdown_content) > max_length:
        truncated_content = markdown_content[:max_length] + "\n\n[... content truncated for analysis ...]"
    else:
        truncated_content = markdown_content

    return CONTENT_ANALYSIS_PROMPT.format(markdown_content=truncated_content)


def format_layout_selection_prompt(content_analysis: dict) -> str:
    """
    Format the layout selection prompt with content analysis results.

    Args:
        content_analysis: Dictionary containing content analysis results

    Returns:
        Formatted prompt string ready for LLM
    """
    # Safely extract values with None handling
    sections = content_analysis.get('sections') or []
    code_blocks = content_analysis.get('code_blocks') or []
    tables = content_analysis.get('tables') or []
    links = content_analysis.get('links') or []
    youtube_links = content_analysis.get('youtube_links') or []
    github_links = content_analysis.get('github_links') or []
    entities = content_analysis.get('entities') or {}

    # Convert content analysis dict to readable format
    analysis_text = f"""
Document Type: {content_analysis.get('document_type', 'unknown')}
Title: {content_analysis.get('title', 'Untitled')}
Sections: {len(sections)} sections
Code Blocks: {len(code_blocks)} code blocks
Tables: {len(tables)} tables
Links: {len(links)} links
YouTube Links: {len(youtube_links)} videos
GitHub Links: {len(github_links)} repositories

Key Entities:
- Technologies: {', '.join((entities.get('technologies') or [])[:10])}
- Tools: {', '.join((entities.get('tools') or [])[:10])}
- Languages: {', '.join((entities.get('languages') or [])[:10])}
- Concepts: {', '.join((entities.get('concepts') or [])[:5])}
"""

    return LAYOUT_SELECTION_PROMPT.format(content_analysis=analysis_text)


def format_component_selection_prompt(content_analysis: dict, layout_decision: dict) -> str:
    """
    Format the component selection prompt with content analysis and layout decision.

    Args:
        content_analysis: Dictionary containing content analysis results
        layout_decision: Dictionary containing layout selection results

    Returns:
        Formatted prompt string ready for LLM
    """
    # Safely extract values with None handling
    sections = content_analysis.get('sections') or []
    code_blocks = content_analysis.get('code_blocks') or []
    tables = content_analysis.get('tables') or []
    links = content_analysis.get('links') or []
    youtube_links = content_analysis.get('youtube_links') or []
    github_links = content_analysis.get('github_links') or []

    # Format content analysis
    analysis_text = f"""
Document Type: {content_analysis.get('document_type', 'unknown')}
Title: {content_analysis.get('title', 'Untitled')}
Sections ({len(sections)} total): {sections[:30]}
Code Blocks: {len(code_blocks)} blocks
Tables: {len(tables)} tables
Links: {len(links)} total
Media: {len(youtube_links)} videos, {len(github_links)} repos
"""

    # Format layout decision
    suggestions = layout_decision.get('component_suggestions') or layout_decision.get('component_priorities') or []
    layout_text = f"""
Selected Layout: {layout_decision.get('layout_type', 'unknown')}
Confidence: {layout_decision.get('confidence', 0.0):.2f}
Reasoning: {layout_decision.get('reasoning', '')}
Alternative Layouts: {', '.join(layout_decision.get('alternative_layouts', []))}
Component Priorities: {', '.join(suggestions[:15])}
"""

    return COMPONENT_SELECTION_PROMPT.format(
        content_analysis=analysis_text,
        layout_decision=layout_text
    )


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_component_variety(components: list[dict]) -> dict:
    """
    Validate that component selection meets variety requirements.

    Checks:
    1. At least 4 different component types
    2. No more than 2 consecutive components of the same type

    Args:
        components: List of component specifications

    Returns:
        Dictionary with validation results and statistics
    """
    if not components:
        return {
            'valid': False,
            'unique_types_count': 0,
            'max_consecutive_same_type': 0,
            'meets_min_types': False,
            'meets_no_consecutive': True,
            'violations': ['No components provided']
        }

    # Count unique types
    component_types = [c.get('component_type', '') for c in components]
    unique_types = set(component_types)
    unique_count = len(unique_types)

    # Check consecutive same type
    max_consecutive = 1
    current_consecutive = 1

    for i in range(1, len(component_types)):
        if component_types[i] == component_types[i-1]:
            current_consecutive += 1
            max_consecutive = max(max_consecutive, current_consecutive)
        else:
            current_consecutive = 1

    # Validation checks
    meets_min_types = unique_count >= 4
    meets_no_consecutive = max_consecutive <= 2

    violations = []
    if not meets_min_types:
        violations.append(f'Only {unique_count} unique types, need at least 4')
    if not meets_no_consecutive:
        violations.append(f'Found {max_consecutive} consecutive same type, max allowed is 2')

    # Check for type dominance (no single type should be >40% of components)
    type_distribution = {t: component_types.count(t) for t in unique_types}
    meets_no_dominance = True
    if len(components) >= 5:
        for comp_type, count in type_distribution.items():
            ratio = count / len(components)
            if ratio > 0.40:
                meets_no_dominance = False
                violations.append(
                    f"'{comp_type}' dominates at {count}/{len(components)} ({ratio:.0%}), max allowed is 40%"
                )

    return {
        'valid': meets_min_types and meets_no_consecutive and meets_no_dominance,
        'unique_types_count': unique_count,
        'max_consecutive_same_type': max_consecutive,
        'meets_min_types': meets_min_types,
        'meets_no_consecutive': meets_no_consecutive,
        'meets_no_dominance': meets_no_dominance,
        'violations': violations,
        'component_type_distribution': type_distribution
    }
