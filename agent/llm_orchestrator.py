"""
LLM Orchestrator - Actual LLM-powered dashboard generation using OpenRouter.

This module replaces the heuristic-based orchestrate_dashboard with real LLM calls
using OpenRouter API to intelligently select and generate A2UI components based
on the content analysis.
"""

import os
import json
import re
from typing import AsyncGenerator
import httpx
from dotenv import load_dotenv

from a2ui_generator import (
    A2UIComponent,
    generate_component,
    generate_id,
    reset_id_counter,
    VALID_COMPONENT_TYPES,
    # Component generators
    generate_tldr,
    generate_key_takeaways,
    generate_stat_card,
    generate_code_block,
    generate_step_card,
    generate_callout_card,
    generate_video_card,
    generate_repo_card,
    generate_link_card,
    generate_data_table,
    generate_headline_card,
    generate_table_of_contents,
    generate_quote_card,
    generate_comparison_table,
    generate_checklist_item,
    generate_bullet_point,
    generate_section,
    generate_grid,
    generate_expert_tip,
    generate_tag,
    generate_badge,
    # Additional component generators
    generate_trend_indicator,
    generate_metric_row,
    generate_comparison_bar,
    generate_ranked_item,
    generate_pro_con_item,
    generate_accordion,
    generate_executive_summary,
    generate_tool_card,
    generate_book_card,
    generate_timeline_event,
)
from content_analyzer import parse_markdown, ContentAnalysis, _classify_heuristic
from prompts import (
    format_content_analysis_prompt,
    format_layout_selection_prompt,
    format_component_selection_prompt,
    validate_component_variety,
)

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-haiku-4.5")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Default semantic zones for each component type
# These are used when the LLM doesn't specify a zone
COMPONENT_DEFAULT_ZONES = {
    # Hero zone - prominent top-level content
    "TLDR": "hero",
    "ExecutiveSummary": "hero",

    # Metrics zone - statistics and data
    "StatCard": "metrics",
    "TrendIndicator": "metrics",
    "MetricRow": "metrics",
    "ProgressRing": "metrics",
    "MiniChart": "metrics",
    "ComparisonBar": "metrics",

    # Insights zone - key findings and observations
    "KeyTakeaways": "insights",
    "CalloutCard": "insights",
    "QuoteCard": "insights",
    "ExpertTip": "insights",
    "RankedItem": "insights",
    "HeadlineCard": "insights",

    # Content zone - detailed information
    "CodeBlock": "content",
    "DataTable": "content",
    "StepCard": "content",
    "ChecklistItem": "content",
    "ProConItem": "content",
    "BulletPoint": "content",
    "CommandCard": "content",
    "TableOfContents": "content",
    "ComparisonTable": "content",
    "FeatureMatrix": "content",
    "PricingTable": "content",
    "VsCard": "content",
    "Accordion": "content",
    "TimelineEvent": "content",

    # Media zone - multimedia content
    "VideoCard": "media",
    "ImageCard": "media",
    "PlaylistCard": "media",
    "PodcastCard": "media",

    # Resources zone - links and references
    "LinkCard": "resources",
    "ToolCard": "resources",
    "BookCard": "resources",
    "RepoCard": "resources",
    "ProfileCard": "resources",
    "CompanyCard": "resources",

    # Tags zone - categorization
    "TagCloud": "tags",
    "CategoryBadge": "tags",
    "StatusIndicator": "tags",
    "PriorityBadge": "tags",
    "DifficultyBadge": "tags",
    "Tag": "tags",
    "Badge": "tags",

    # Default for unknown types
    "Section": "content",
    "Grid": "content",
}

# Default width hints for each component type
# These are used when the LLM doesn't specify a width_hint
COMPONENT_DEFAULT_WIDTHS = {
    # Full width components
    "TLDR": "full",
    "ExecutiveSummary": "full",
    "CodeBlock": "full",
    "DataTable": "full",
    "TableOfContents": "full",
    "Section": "full",
    "ComparisonTable": "full",
    "FeatureMatrix": "full",
    "PricingTable": "full",

    # Half width components
    "KeyTakeaways": "half",
    "QuoteCard": "half",
    "CalloutCard": "half",
    "VsCard": "half",
    "ExpertTip": "half",
    "RankedItem": "half",
    "ProConItem": "half",
    "ChecklistItem": "half",
    "HeadlineCard": "half",

    # Third width components (3-column grid on desktop)
    "StatCard": "third",
    "LinkCard": "third",
    "RepoCard": "third",
    "VideoCard": "third",
    "ToolCard": "third",
    "BookCard": "third",
    "ProfileCard": "third",
    "CompanyCard": "third",
    "TrendIndicator": "third",
    "MetricRow": "third",
    "ImageCard": "third",

    # Quarter width (small items)
    "Badge": "quarter",
    "Tag": "quarter",
    "BulletPoint": "full",
    "StepCard": "full",
    "CommandCard": "full",
    "TimelineEvent": "full",
}


async def call_llm(prompt: str, system_prompt: str = "", max_tokens: int = 4000, temperature: float = 0.7) -> str:
    """
    Call OpenRouter LLM API with the given prompt.

    Args:
        prompt: The user prompt to send
        system_prompt: Optional system prompt
        max_tokens: Maximum tokens in the response
        temperature: Sampling temperature (lower = more precise)

    Returns:
        The LLM response text
    """
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY not set in environment")

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:3010",
                "X-Title": "Second Brain Research Dashboard",
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
        )

        if response.status_code != 200:
            error_text = response.text
            print(f"[LLM ERROR] Status {response.status_code}: {error_text}")
            raise Exception(f"LLM API error: {response.status_code} - {error_text}")

        result = response.json()
        return result["choices"][0]["message"]["content"]


def extract_json_from_response(response: str) -> dict:
    """
    Extract JSON from LLM response, handling markdown code blocks and truncated responses.

    Args:
        response: Raw LLM response text

    Returns:
        Parsed JSON dictionary
    """
    # Try to find JSON in code blocks first
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', response)
    if json_match:
        json_str = json_match.group(1).strip()
    else:
        # Try to find raw JSON
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = response

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"[JSON PARSE ERROR] {e}", flush=True)
        # Try to recover truncated JSON by extracting complete component objects
        recovered = _recover_truncated_components(json_str)
        if recovered:
            print(f"[JSON RECOVERY] Recovered {len(recovered)} components from truncated response", flush=True)
            return {"components": recovered}
        print(f"[RAW RESPONSE] {response[:500]}...", flush=True)
        return {}


def _recover_truncated_components(json_str: str) -> list[dict]:
    """
    Recover individual component objects from a truncated JSON response.
    Finds the components array and extracts all complete JSON objects from it.
    """
    # Find the start of the components array
    match = re.search(r'"components"\s*:\s*\[', json_str)
    if not match:
        return []

    array_start = match.end()
    components = []
    pos = array_start

    # Extract complete JSON objects one at a time
    while pos < len(json_str):
        # Skip whitespace and commas
        while pos < len(json_str) and json_str[pos] in ' \t\n\r,':
            pos += 1
        if pos >= len(json_str) or json_str[pos] != '{':
            break

        # Find the matching closing brace
        depth = 0
        start = pos
        in_string = False
        escape_next = False
        for i in range(start, len(json_str)):
            c = json_str[i]
            if escape_next:
                escape_next = False
                continue
            if c == '\\' and in_string:
                escape_next = True
                continue
            if c == '"' and not escape_next:
                in_string = not in_string
                continue
            if in_string:
                continue
            if c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    # Found complete object
                    try:
                        obj = json.loads(json_str[start:i+1])
                        components.append(obj)
                    except json.JSONDecodeError:
                        pass
                    pos = i + 1
                    break
        else:
            # Reached end without finding matching brace — truncated
            break

    return components


async def analyze_content_with_llm(markdown_content: str) -> dict:
    """
    Use LLM to analyze markdown content and classify it.

    Args:
        markdown_content: Raw markdown content

    Returns:
        Content analysis dictionary
    """
    system_prompt = """You are an expert content analyst. Analyze documents and return structured JSON.
Always respond with valid JSON only, no additional text."""

    prompt = format_content_analysis_prompt(markdown_content)

    print(f"[LLM] Analyzing content... (prompt length: {len(prompt)} chars)")
    try:
        response = await call_llm(prompt, system_prompt)
        print(f"[LLM] Analysis response received ({len(response)} chars)")
    except Exception as e:
        print(f"[LLM ERROR] Content analysis failed: {e}")
        import traceback
        traceback.print_exc()
        response = ""
    result = extract_json_from_response(response)

    # Provide defaults if parsing failed
    if not result:
        parsed = parse_markdown(markdown_content)
        result = {
            "document_type": _classify_heuristic(markdown_content, parsed),
            "title": parsed.get("title", "Untitled"),
            "entities": {"technologies": [], "tools": [], "languages": [], "concepts": []},
            "confidence": 0.5,
            "reasoning": "Fallback to heuristic analysis"
        }

    print(f"[LLM] Content analyzed: {result.get('document_type', 'unknown')}")
    return result


async def select_layout_with_llm(content_analysis: dict) -> dict:
    """
    Use LLM to select optimal layout based on content analysis.

    Args:
        content_analysis: Content analysis results

    Returns:
        Layout selection dictionary
    """
    system_prompt = """You are an expert UI/UX designer. Select optimal layouts and return structured JSON.
Always respond with valid JSON only, no additional text."""

    prompt = format_layout_selection_prompt(content_analysis)

    print("[LLM] Selecting layout...")
    response = await call_llm(prompt, system_prompt)
    result = extract_json_from_response(response)

    # Provide defaults if parsing failed
    if not result or "layout_type" not in result:
        result = {
            "layout_type": "summary_layout",
            "confidence": 0.5,
            "reasoning": "Default layout selection",
            "alternative_layouts": ["list_layout", "news_layout"],
            "component_suggestions": ["TLDR", "KeyTakeaways", "StatCard", "CalloutCard"]
        }

    print(f"[LLM] Layout selected: {result.get('layout_type', 'unknown')}")
    return result


async def select_components_with_llm(
    content_analysis: dict,
    layout_decision: dict,
    markdown_content: str
) -> list[dict]:
    """
    Use LLM to select and configure A2UI components.

    Args:
        content_analysis: Content analysis results
        layout_decision: Layout selection results
        markdown_content: Original markdown for context

    Returns:
        List of component specifications
    """
    system_prompt = """You are an expert A2UI component architect. Generate diverse dashboard components.
CRITICAL: You MUST return valid JSON with a "components" array containing component specifications.
Each component needs: component_type, priority, zone, and props with actual data from the document.
RULES:
1. Cover ALL sections of the document - do NOT stop at the first few sections.
2. Use at least 6 different component types. No single type should exceed 40% of components.
3. Never place 3+ consecutive components of the same type.
4. Match component types to content: quotes->QuoteCard, news stories->HeadlineCard, stats->StatCard, events->TimelineEvent.
5. For documents with 5+ sections, generate 15-25 components."""

    prompt = format_component_selection_prompt(content_analysis, layout_decision)

    # Add full document content for the LLM to use (up to 30k chars)
    content_limit = 30000
    if len(markdown_content) > content_limit:
        doc_content = markdown_content[:content_limit] + "\n\n[... content truncated ...]"
    else:
        doc_content = markdown_content

    prompt += f"""

## Actual Document Content (use this to populate component props)

{doc_content}

CRITICAL: You must generate components covering ALL sections and topics above, not just the first few.
Extract REAL data from the document to populate component props.
Return JSON with "components" array."""

    import sys
    print(f"[LLM] Selecting components... (prompt length: {len(prompt)} chars)", flush=True)
    try:
        response = await call_llm(prompt, system_prompt, max_tokens=16000, temperature=0.4)
        print(f"[LLM] Response received ({len(response)} chars)", flush=True)
    except Exception as e:
        print(f"[LLM ERROR] Component selection LLM call failed: {e}", file=sys.stderr, flush=True)
        import traceback
        traceback.print_exc()
        raise

    result = extract_json_from_response(response)

    components = result.get("components", [])

    if not components:
        print(f"[LLM ERROR] No components parsed. Response first 1000 chars:\n{response[:1000]}", file=sys.stderr, flush=True)
        raise ValueError(f"LLM returned no components. Parsed keys: {list(result.keys())}. Response length: {len(response)}. First 200 chars: {response[:200]}")

    # Validate variety
    variety = validate_component_variety(components)
    print(f"[LLM] Components selected: {len(components)}, unique types: {variety['unique_types_count']}")
    if not variety['valid']:
        for violation in variety.get('violations', []):
            print(f"[LLM VARIETY WARNING] {violation}")

    return components


def apply_layout_and_zone(component: A2UIComponent, spec: dict) -> A2UIComponent:
    """
    Apply layout width hint and semantic zone to a component.

    Uses the width_hint and zone from the spec if provided, otherwise falls back
    to the defaults for the component type.

    Args:
        component: The built A2UIComponent
        spec: Original component spec that may contain width_hint and zone

    Returns:
        Component with layout and zone fields set
    """
    # Get component type without 'a2ui.' prefix
    component_type = component.type.replace("a2ui.", "")

    # Check for explicit width_hint in spec
    props = spec.get("props", {})
    explicit_width = props.get("width_hint") or spec.get("width_hint")

    # Use explicit width or fall back to default
    width = explicit_width or COMPONENT_DEFAULT_WIDTHS.get(component_type, "full")

    # Apply the layout
    component.layout = {"width": width}

    # Check for explicit zone in spec
    explicit_zone = spec.get("zone")

    # Case-insensitive lookup for zone defaults
    # Build a lowercase mapping for robust lookups
    zone_lookup_key = component_type
    default_zone = COMPONENT_DEFAULT_ZONES.get(zone_lookup_key)

    # If not found, try case-insensitive lookup
    if default_zone is None:
        lower_key = component_type.lower()
        for key, value in COMPONENT_DEFAULT_ZONES.items():
            if key.lower() == lower_key:
                default_zone = value
                print(f"[ZONE] Case-insensitive match: '{component_type}' → '{key}' → zone='{value}'")
                break

    # Final fallback to "content"
    if default_zone is None:
        default_zone = "content"
        print(f"[ZONE] No default zone for '{component_type}', using 'content'")

    # Use explicit zone or fall back to default
    zone = explicit_zone or default_zone

    # Debug logging for zone assignment
    print(f"[ZONE] {component_type}: explicit_zone={explicit_zone!r}, default={default_zone}, final={zone}")

    # Apply the zone
    component.zone = zone

    return component


def expand_component_specs(specs: list[dict]) -> list[dict]:
    """
    Expand component specs that contain batched items into individual specs.

    This handles ProConItem specs that have multiple items in an 'items' array,
    converting them into individual specs for each item.

    Args:
        specs: List of component specifications

    Returns:
        Expanded list with batched items converted to individual specs
    """
    expanded = []

    for spec in specs:
        component_type = spec.get("component_type", "")
        props = spec.get("props", {})

        # Handle ProConItem with multiple items
        if component_type == "ProConItem":
            items = props.get("items", [])
            item_type = props.get("type", "").lower()

            if items and isinstance(items, list) and len(items) > 1:
                is_pro = item_type in ("pro", "pros")
                is_con = item_type in ("con", "cons")

                if is_pro or is_con:
                    # Expand each item into its own ProConItem spec
                    for item in items:
                        expanded.append({
                            "component_type": "ProConItem",
                            "priority": spec.get("priority", "medium"),
                            "props": {
                                "type": "pro" if is_pro else "con",
                                "label": item,
                            }
                        })
                    continue

        # Keep spec as-is for all other cases
        expanded.append(spec)

    return expanded


def build_a2ui_component(spec: dict, content_analysis: dict) -> A2UIComponent | None:
    """
    Build an A2UIComponent from a specification dictionary.

    Args:
        spec: Component specification from LLM
        content_analysis: Content analysis for fallback data

    Returns:
        A2UIComponent instance or None if invalid
    """
    component_type = spec.get("component_type", "")
    props = spec.get("props", {})

    # Normalize component type - strip whitespace
    component_type = component_type.strip()

    # Case-insensitive type mapping for robust LLM output handling
    # Maps lowercase versions to canonical PascalCase names
    COMPONENT_TYPE_CANONICAL = {
        "tldr": "TLDR",
        "keytakeaways": "KeyTakeaways",
        "statcard": "StatCard",
        "codeblock": "CodeBlock",
        "stepcard": "StepCard",
        "calloutcard": "CalloutCard",
        "videocard": "VideoCard",
        "repocard": "RepoCard",
        "linkcard": "LinkCard",
        "datatable": "DataTable",
        "headlinecard": "HeadlineCard",
        "tableofcontents": "TableOfContents",
        "quotecard": "QuoteCard",
        "checklistitem": "ChecklistItem",
        "bulletpoint": "BulletPoint",
        "experttip": "ExpertTip",
        "badge": "Badge",
        "tag": "Tag",
        "section": "Section",
        "comparisontable": "ComparisonTable",
        "trendindicator": "TrendIndicator",
        "metricrow": "MetricRow",
        "comparisonbar": "ComparisonBar",
        "rankeditem": "RankedItem",
        "proconitem": "ProConItem",
        "accordion": "Accordion",
        "executivesummary": "ExecutiveSummary",
        "grid": "Grid",
        "toolcard": "ToolCard",
        "bookcard": "BookCard",
        "taggroup": "TagGroup",
        "tagcloud": "TagCloud",
        "categorybadge": "CategoryBadge",
        "statusindicator": "StatusIndicator",
        "prioritybadge": "PriorityBadge",
        "difficultybadge": "DifficultyBadge",
        "profilecard": "ProfileCard",
        "companycard": "CompanyCard",
        "timelineevent": "TimelineEvent",
    }

    # Try to normalize type (handle various casing from LLM)
    original_type = component_type
    if component_type.lower() in COMPONENT_TYPE_CANONICAL:
        component_type = COMPONENT_TYPE_CANONICAL[component_type.lower()]
        if original_type != component_type:
            print(f"[BUILD] Normalized component type: '{original_type}' → '{component_type}'")
    elif component_type and component_type not in COMPONENT_TYPE_CANONICAL.values():
        print(f"[BUILD] Unknown component type: '{component_type}' (will use fallback)")

    try:
        # Map component types to generator functions
        if component_type == "TLDR":
            content = props.get("content", "Summary of the document")
            if len(content) > 300:
                content = content[:297] + "..."
            return generate_tldr(content=content, max_length=props.get("max_length", 200))

        elif component_type == "KeyTakeaways":
            items = props.get("items", ["Key takeaway 1", "Key takeaway 2"])
            if not items:
                items = ["Key takeaway 1", "Key takeaway 2"]
            return generate_key_takeaways(items=items[:5])

        elif component_type == "StatCard":
            # Map LLM props to generator signature: title, value, unit, change, change_type, highlight
            change_val = props.get("trendValue", props.get("change_value", props.get("change")))
            # Parse change value, handling string formats
            change_float = None
            if change_val is not None:
                try:
                    change_str = str(change_val).replace(",", "").replace("%", "").replace("+", "")
                    change_float = float(change_str) if change_str else None
                except (ValueError, TypeError):
                    change_float = None

            # Map trend to change_type (positive/negative/neutral)
            trend = props.get("trend", "neutral")
            change_type_map = {"up": "positive", "down": "negative", "positive": "positive", "negative": "negative"}
            change_type = change_type_map.get(trend, "neutral")

            return generate_stat_card(
                title=props.get("label", props.get("title", "Metric")),
                value=str(props.get("value", "N/A")),
                unit=props.get("unit"),
                change=change_float,
                change_type=change_type,
                highlight=props.get("highlight", False)
            )

        elif component_type == "CodeBlock":
            code = props.get("code", "// Code example")
            if not code or not code.strip():
                return None
            return generate_code_block(
                code=code,
                language=props.get("language", "text")
            )

        elif component_type == "StepCard":
            return generate_step_card(
                step_number=props.get("step_number", props.get("number", 1)),
                title=props.get("title", "Step"),
                description=props.get("description", "Step description")
            )

        elif component_type == "CalloutCard":
            return generate_callout_card(
                type=props.get("type", "info"),
                title=props.get("title", "Note"),
                content=props.get("content", "Important information")
            )

        elif component_type == "VideoCard":
            video_url = props.get("video_url", props.get("url", ""))
            if not video_url:
                return None
            return generate_video_card(
                video_url=video_url,
                title=props.get("title", "Video"),
                description=props.get("description", "")
            )

        elif component_type == "RepoCard":
            return generate_repo_card(
                name=props.get("name", "Repository"),
                owner=props.get("owner"),
                repo_url=props.get("repo_url", props.get("url", "https://github.com"))
            )

        elif component_type == "LinkCard":
            url = props.get("url", "")
            if not url:
                return None
            return generate_link_card(
                url=url,
                title=props.get("title", "Resource")
            )

        elif component_type == "DataTable":
            headers = props.get("headers", ["Column 1", "Column 2"])
            rows = props.get("rows", [["Data 1", "Data 2"]])
            if not headers or not rows:
                return None
            return generate_data_table(headers=headers, rows=rows)

        elif component_type == "HeadlineCard":
            # Generator signature: title, summary, source, published_at, sentiment, image_url
            return generate_headline_card(
                title=props.get("headline", props.get("title", "Headline")),
                summary=props.get("subheadline", props.get("subtitle", props.get("summary", ""))),
                source=props.get("source", "Source"),
                published_at=props.get("timestamp", props.get("published_at", props.get("publishedAt", ""))),
                sentiment=props.get("sentiment", "neutral"),
                image_url=props.get("image_url", props.get("imageUrl"))
            )

        elif component_type == "TableOfContents":
            items = props.get("items", [])
            if not items:
                sections = content_analysis.get("sections", [])
                items = [{"title": s, "anchor": f"#{s.lower().replace(' ', '-')}"} for s in sections[:8]]
            if not items:
                return None
            return generate_table_of_contents(items=items)

        elif component_type == "QuoteCard":
            return generate_quote_card(
                text=props.get("quote", props.get("text", "Quote text")),
                author=props.get("author", "Unknown"),
                source=props.get("source")
            )

        elif component_type == "ChecklistItem":
            return generate_checklist_item(
                text=props.get("text", "Checklist item"),
                completed=props.get("completed", False)
            )

        elif component_type == "BulletPoint":
            return generate_bullet_point(
                text=props.get("text", "Bullet point")
            )

        elif component_type == "ExpertTip":
            # Generator signature: title, content, expert_name, difficulty, category
            tip_content = props.get("tip", props.get("content", "Expert tip"))
            tip_title = props.get("title", "Expert Tip")
            # If no explicit title but we have tip content, use a truncated version as title
            if tip_title == "Expert Tip" and tip_content and len(tip_content) > 50:
                tip_title = tip_content[:47] + "..."

            return generate_expert_tip(
                title=tip_title,
                content=tip_content,
                expert_name=props.get("expert", props.get("author", props.get("expert_name"))),
                difficulty=props.get("difficulty"),
                category=props.get("category")
            )

        elif component_type == "Badge":
            return generate_badge(
                label=props.get("label", "Badge"),
                count=props.get("count", 1)
            )

        elif component_type == "Tag":
            return generate_tag(
                label=props.get("label", "Tag"),
                type=props.get("type", "default")
            )

        elif component_type == "Section":
            # Sections need special handling for children
            title = props.get("title", "Section")
            children = props.get("children", [])
            if not children:
                children = ["placeholder"]
            return generate_section(title=title, content=children)

        elif component_type == "ComparisonTable":
            items = props.get("items", [])
            features = props.get("features", [])
            if not items or not features:
                return None
            return generate_comparison_table(items=items, features=features)

        elif component_type == "TrendIndicator":
            # Parse value - handle commas, percentages, and plus signs
            def parse_numeric(val, default=0):
                if val is None:
                    return default
                try:
                    val_str = str(val).replace(",", "").replace("%", "").replace("+", "").strip()
                    return float(val_str) if val_str else default
                except (ValueError, TypeError):
                    return default

            return generate_trend_indicator(
                label=props.get("label", props.get("metric", "Metric")),
                value=parse_numeric(props.get("value"), 0),
                trend=props.get("direction", props.get("trend", "stable")),
                change=parse_numeric(props.get("change", props.get("trendValue")), 0),
                unit=props.get("unit", "")
            )

        elif component_type == "MetricRow":
            # Handle both single metric and multiple metrics format
            metrics_data = props.get("metrics", [])
            if metrics_data and isinstance(metrics_data, list):
                # Convert to expected format
                metrics = []
                for m in metrics_data:
                    if isinstance(m, dict):
                        metrics.append({
                            "label": m.get("label", "Metric"),
                            "value": m.get("value", "N/A"),
                            "unit": m.get("unit", "")
                        })
                return generate_metric_row(
                    label=props.get("title", props.get("label", "")),
                    metrics=metrics
                )
            else:
                return generate_metric_row(
                    label=props.get("label", props.get("title", "Metric")),
                    value=props.get("value", "N/A"),
                    unit=props.get("unit", "")
                )

        elif component_type == "ComparisonBar":
            # Generator signature: label, items, max_value
            items = props.get("items", [])
            if not items:
                return None
            return generate_comparison_bar(
                label=props.get("title", props.get("label", "Comparison")),
                items=items,
                max_value=props.get("max_value", props.get("maxValue"))
            )

        elif component_type == "RankedItem":
            # Map LLM props (title, description) to frontend props (label, value)
            return generate_component("a2ui.RankedItem", {
                "rank": props.get("rank", 1),
                "label": props.get("title", props.get("label", "Item")),
                "value": props.get("description", props.get("value", "")),
                "badge": props.get("badge"),
                "score": props.get("score")
            })

        elif component_type == "ProConItem":
            # LLM can output two formats:
            # 1. Individual item: {type: 'pro'|'con', label: '...', description: '...'}
            # 2. Batch format: {type: 'pros'|'cons', items: ['item1', 'item2'], title: '...'}
            item_type = props.get("type", "info").lower()
            items = props.get("items", [])

            # Handle batch format - return FIRST item as proper ProConItem
            # The orchestrator loop will handle expansion for multiple items
            if items and isinstance(items, list):
                is_pro = item_type in ("pro", "pros")
                is_con = item_type in ("con", "cons")

                if is_pro or is_con:
                    # Return the first item as a properly formatted ProConItem
                    first_item = items[0] if items else "Item"
                    return generate_component("a2ui.ProConItem", {
                        "type": "pro" if is_pro else "con",
                        "label": first_item,
                        "description": props.get("title") if len(items) == 1 else None
                    })

            # Handle individual item format directly
            if item_type in ("pro", "con"):
                return generate_component("a2ui.ProConItem", {
                    "type": item_type,
                    "label": props.get("label", props.get("text", "Item")),
                    "description": props.get("description"),
                    "weight": props.get("weight")
                })

            # Legacy format with separate pros and cons arrays
            pros = props.get("pros", [])
            cons = props.get("cons", [])
            if pros:
                return generate_component("a2ui.ProConItem", {
                    "type": "pro",
                    "label": pros[0] if pros else "Advantage"
                })
            if cons:
                return generate_component("a2ui.ProConItem", {
                    "type": "con",
                    "label": cons[0] if cons else "Disadvantage"
                })

            return None

        elif component_type == "Accordion":
            # LLM outputs sections with text content, but generate_accordion expects
            # component IDs. Convert to a CalloutCard with formatted section list instead.
            title = props.get("title", "Details")
            sections = props.get("sections", props.get("items", []))

            if sections:
                # Format sections as collapsible-style text
                formatted_sections = []
                for section in sections[:10]:
                    if isinstance(section, dict):
                        sec_title = section.get("title", "Section")
                        sec_content = section.get("content", "")
                        formatted_sections.append(f"**{sec_title}**: {sec_content}")
                    else:
                        formatted_sections.append(str(section))

                return generate_callout_card(
                    type="info",
                    title=title,
                    content="\n\n".join(formatted_sections)
                )
            return None

        elif component_type == "ExecutiveSummary":
            # Extract key_metrics (dict) and recommendations (list) from LLM props
            # The LLM may use various prop names, so we handle multiple formats
            key_metrics = props.get("key_metrics", props.get("metrics", props.get("keyMetrics")))

            # Recommendations can come from highlights, key_points, or recommendations
            recommendations = props.get("recommendations", props.get("highlights", props.get("key_points")))
            # Ensure recommendations is a list (may be None)
            if recommendations and not isinstance(recommendations, list):
                recommendations = [recommendations] if isinstance(recommendations, str) else None

            return generate_executive_summary(
                title=props.get("title", "Executive Summary"),
                summary=props.get("summary", props.get("content", "Summary content")),
                key_metrics=key_metrics,
                recommendations=recommendations
            )

        elif component_type == "Grid":
            # Grid component expects child component IDs, not text
            # For now, convert to a simple Section with title
            title = props.get("title", "Grid Content")
            columns = props.get("columns", 2)
            children = props.get("children", [])

            # If children are actual text descriptions, render as info
            if children and isinstance(children[0], str):
                return generate_callout_card(
                    type="info",
                    title=title,
                    content=f"Layout: {columns} columns with {len(children)} items"
                )
            return None

        elif component_type == "ToolCard":
            name = props.get("name", props.get("title", "Tool"))
            description = props.get("description", "")
            url = props.get("url", "")

            # ToolCard requires a valid URL
            if url and url.startswith(("http://", "https://")):
                return generate_tool_card(
                    name=name,
                    description=description,
                    url=url,
                    category=props.get("category"),
                    pricing=props.get("pricing"),
                    features=props.get("features", [])[:5] if props.get("features") else None
                )
            else:
                # Fallback to LinkCard-style display without URL
                return generate_component("a2ui.ToolCard", {
                    "name": name,
                    "description": description,
                    "url": url or "https://example.com",
                    "category": props.get("category", "tool")
                })

        elif component_type == "BookCard":
            return generate_book_card(
                title=props.get("title", "Book"),
                author=props.get("author", "Unknown Author"),
                year=props.get("year"),
                isbn=props.get("isbn"),
                url=props.get("url"),
                rating=props.get("rating"),
                description=props.get("description")
            )

        elif component_type == "TagGroup":
            # TagGroup is deprecated - convert to TagCloud
            tags = props.get("tags", props.get("items", []))
            if tags:
                # Convert to TagCloud format
                tag_items = []
                for t in tags[:20]:
                    if isinstance(t, str):
                        tag_items.append({"name": t, "count": 1})
                    elif isinstance(t, dict):
                        tag_items.append({"name": t.get("label", t.get("name", str(t))), "count": t.get("count", 1)})
                return generate_component("a2ui.TagCloud", {"tags": tag_items})
            return None

        elif component_type == "TagCloud":
            tags = props.get("tags", props.get("items", []))
            if tags:
                # Normalize tag format
                tag_items = []
                for t in tags[:20]:
                    if isinstance(t, str):
                        tag_items.append({"name": t, "count": 1})
                    elif isinstance(t, dict):
                        tag_items.append({"name": t.get("label", t.get("name", str(t))), "count": t.get("count", 1)})
                return generate_component("a2ui.TagCloud", {"tags": tag_items})
            return None

        elif component_type == "CategoryBadge":
            return generate_component("a2ui.CategoryBadge", {
                "category": props.get("category", props.get("label", "Category")),
                "color": props.get("color"),
                "icon": props.get("icon"),
                "size": props.get("size", "md"),
            })

        elif component_type == "StatusIndicator":
            return generate_component("a2ui.StatusIndicator", {
                "status": props.get("status", "pending"),
                "label": props.get("label"),
                "pulse": props.get("pulse", False),
            })

        elif component_type == "PriorityBadge":
            return generate_component("a2ui.PriorityBadge", {
                "priority": props.get("priority", props.get("level", "medium")),
            })

        elif component_type == "DifficultyBadge":
            return generate_component("a2ui.DifficultyBadge", {
                "level": props.get("level", props.get("difficulty", "intermediate")),
            })

        elif component_type == "ProfileCard":
            return generate_component("a2ui.ProfileCard", {
                "name": props.get("name", "Person"),
                "title": props.get("title", props.get("role", "")),
                "bio": props.get("bio", props.get("description", "")),
                "imageUrl": props.get("imageUrl", props.get("avatar")),
                "links": props.get("links", [])
            })

        elif component_type == "CompanyCard":
            return generate_component("a2ui.CompanyCard", {
                "name": props.get("name", "Company"),
                "description": props.get("description", ""),
                "industry": props.get("industry"),
                "logoUrl": props.get("logoUrl", props.get("logo")),
                "website": props.get("website", props.get("url"))
            })

        elif component_type == "TimelineEvent":
            event_type = props.get("event_type", props.get("eventType", "announcement"))
            if event_type not in {"article", "announcement", "milestone", "update"}:
                event_type = "announcement"
            return generate_timeline_event(
                title=props.get("title", "Event"),
                timestamp=props.get("timestamp", props.get("date", "")),
                content=props.get("content", props.get("description", "")),
                event_type=event_type,
            )

        else:
            # Generic fallback - create a callout with the data
            print(f"[COMPONENT] Unknown type '{component_type}', using CalloutCard fallback")
            return generate_callout_card(
                type="info",
                title=component_type,
                content=json.dumps(props, indent=2)[:200] if props else "Component data"
            )

    except Exception as e:
        print(f"[COMPONENT ERROR] Failed to build {component_type}: {e}")
        return None


async def orchestrate_dashboard_with_llm(markdown_content: str) -> AsyncGenerator[A2UIComponent, None]:
    """
    Main orchestration function that uses LLM to generate dashboard components.

    This is the async generator version that yields components one at a time
    for streaming via SSE.

    Args:
        markdown_content: Raw markdown content to transform

    Yields:
        A2UIComponent instances
    """
    # Reset ID counter for fresh component IDs
    reset_id_counter()

    print("\n" + "="*60)
    print("[ORCHESTRATOR] Starting LLM-powered dashboard generation")
    print("="*60)

    # Step 1: Parse markdown structure (fast, no LLM)
    parsed = parse_markdown(markdown_content)
    print(f"[PARSE] Title: {parsed.get('title', 'Untitled')}")
    print(f"[PARSE] Sections: {len(parsed.get('sections', []))}")
    print(f"[PARSE] Code blocks: {len(parsed.get('code_blocks', []))}")

    # Step 2: Analyze content with LLM
    content_analysis = await analyze_content_with_llm(markdown_content)

    # Merge parsed data with LLM analysis
    full_analysis = {
        **content_analysis,
        "sections": parsed.get("sections", []),
        "code_blocks": parsed.get("code_blocks", []),
        "tables": parsed.get("tables", []),
        "links": parsed.get("all_links", []),
        "youtube_links": parsed.get("youtube_links", []),
        "github_links": parsed.get("github_links", []),
    }

    # Step 3: Select layout with LLM
    layout_decision = await select_layout_with_llm(full_analysis)

    # Step 4: Select components with LLM
    component_specs = await select_components_with_llm(
        full_analysis,
        layout_decision,
        markdown_content
    )

    # Step 5: Expand batched specs (e.g., ProConItem with multiple items)
    expanded_specs = expand_component_specs(component_specs)

    # Step 6: Build and yield A2UI components
    print(f"\n[BUILD] Building {len(expanded_specs)} components (expanded from {len(component_specs)} specs)...")

    components_built = 0
    component_types_used = set()

    for spec in expanded_specs:
        component = build_a2ui_component(spec, full_analysis)
        if component:
            # Apply layout width hints and semantic zone
            component = apply_layout_and_zone(component, spec)

            components_built += 1
            component_types_used.add(component.type)
            print(f"[YIELD] Component {components_built}: {component.type} (id={component.id}, width={component.layout.get('width', 'full')}, zone={component.zone})")
            yield component

    print(f"\n[COMPLETE] Generated {components_built} components with {len(component_types_used)} unique types")
    print("="*60 + "\n")


async def orchestrate_dashboard_with_llm_list(markdown_content: str) -> list[A2UIComponent]:
    """
    Synchronous list version that collects all components.

    Args:
        markdown_content: Raw markdown content

    Returns:
        List of A2UIComponent instances
    """
    components = []
    async for component in orchestrate_dashboard_with_llm(markdown_content):
        components.append(component)
    return components
