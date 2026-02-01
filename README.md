# Second Brain Research Dashboard

A generative UI application that transforms Markdown research documents into dynamic, visual dashboards. Paste or upload your research notes and watch them automatically convert into an interactive layout with stat cards, timelines, comparison tables, code blocks, and 50+ other intelligent components.

## Quick Start

**Prerequisites:** Node.js 18+, Python 3.11+, an OpenRouter API key

1. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Add your OPENROUTER_API_KEY to .env
   ```

2. **Start the backend** (port 8000)
   ```bash
   cd agent
   uv sync
   uv run uvicorn main:app --reload --port 8000
   ```

3. **Start the frontend** (port 3010)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Open http://localhost:3010** and paste some Markdown

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                         │
│  ┌───────────────┐    ┌──────────────┐    ┌─────────────────┐  │
│  │ MarkdownInput │───▶│ A2UIRenderer │───▶│ 59 A2UI         │  │
│  │               │    │              │    │ Components      │  │
│  └───────────────┘    └──────────────┘    └─────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ SSE Stream
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                          │
│  ┌─────────────────┐  ┌────────────────┐  ┌─────────────────┐  │
│  │ Content         │─▶│ Layout         │─▶│ A2UI            │  │
│  │ Analyzer        │  │ Selector       │  │ Generator       │  │
│  └─────────────────┘  └────────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

**Frontend** (`/frontend`)
- React 19 + Vite + TypeScript
- Tailwind CSS with dark theme
- 59 A2UI components across 11 categories (News, Media, Data, Lists, Resources, People, Summary, Comparison, Instructional, Layout, Tags)
- Catalog-based dynamic rendering via `A2UIRenderer`

**Backend** (`/agent`)
- FastAPI with Pydantic AI
- `content_analyzer.py` - Parses markdown, extracts links/code/tables, classifies document type
- `layout_selector.py` - Chooses from 10 layout strategies based on content
- `a2ui_generator.py` - Generates component specs with variety enforcement
- Streams components via SSE at `/ag-ui/stream`

**Sample Documents** (`/sample-documents`)
- 5 example markdown files demonstrating different layout types

## Project Structure

```
second-brain-research-dashboard/
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── A2UI/           # 59 components in 11 categories
│       │   └── ui/             # Shadcn/ui base components
│       ├── lib/
│       │   └── a2ui-catalog.tsx # Component registry
│       └── App.tsx             # Main app with split-panel layout
├── agent/
│   ├── main.py                 # FastAPI server
│   ├── content_analyzer.py     # Markdown parsing & classification
│   ├── layout_selector.py      # Layout strategy selection
│   └── a2ui_generator.py       # Component generation
└── sample-documents/           # Demo markdown files
```
