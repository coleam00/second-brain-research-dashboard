# Second Brain Research Dashboard

A generative UI application that transforms Markdown research documents into dynamic, visual dashboards. Paste or upload your research notes and watch them automatically convert into an interactive layout with stat cards, timelines, comparison tables, code blocks, and 50+ other intelligent components.

## Quick Start

**Prerequisites:** Node.js 18+, Python 3.11+, an OpenRouter API key

### 1. Set up the backend environment

```bash
cd agent
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
```

### 2. Set up the frontend environment

```bash
cd frontend
cp .env.example .env
# Edit .env if you need to change the backend URL (default: http://localhost:8000)
```

### 3. Start the backend (port 8000)

```bash
cd agent
uv sync
uv run uvicorn main:app --reload --port 8000
```

### 4. Start the frontend (port 3010)

```bash
cd frontend
npm install
npm run dev
```

### 5. Open http://localhost:3010 and paste some Markdown

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (React)                         │
│  ┌───────────────┐    ┌──────────────┐    ┌─────────────────┐  │
│  │ MarkdownInput │───▶│ A2UIRenderer │───▶│ 59 A2UI         │  │
│  │               │    │              │    │ Components      │  │
│  └───────────────┘    └──────────────┘    └─────────────────┘  │
│          │                                                      │
│  ┌───────▼────────────────────────────────────────────────┐    │
│  │ useDashboardAgent hook - AG-UI state management        │    │
│  │ • Handles SSE streaming from backend                   │    │
│  │ • Applies JSON Patch (RFC 6902) state deltas           │    │
│  │ • Organizes components by semantic zones               │    │
│  └────────────────────────────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │ AG-UI Protocol (SSE)
                             │ Events: RunStarted, StateSnapshot,
                             │         StateDelta, TextMessageContent,
                             │         RunFinished
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Backend (FastAPI)                          │
│  ┌─────────────────┐  ┌────────────────┐  ┌─────────────────┐  │
│  │ Content         │─▶│ Layout         │─▶│ A2UI            │  │
│  │ Analyzer        │  │ Selector       │  │ Generator       │  │
│  └─────────────────┘  └────────────────┘  └─────────────────┘  │
│                                                                 │
│  Pydantic AI agent with tools for content analysis, layout     │
│  selection, and component generation via LLM orchestrator       │
└─────────────────────────────────────────────────────────────────┘
```

**Frontend** (`/frontend`)
- React 19 + Vite + TypeScript
- Tailwind CSS with dark theme
- 59 A2UI components across 11 categories (News, Media, Data, Lists, Resources, People, Summary, Comparison, Instructional, Layout, Tags)
- Catalog-based dynamic rendering via `A2UIRenderer`
- `useDashboardAgent` hook for AG-UI protocol state management

**Backend** (`/agent`)
- FastAPI with Pydantic AI
- AG-UI protocol endpoint at `/agent` with proper event streaming
- `content_analyzer.py` - Parses markdown, extracts links/code/tables, classifies document type
- `layout_selector.py` - Chooses from 10 layout strategies based on content
- `a2ui_generator.py` - Generates component specs with variety enforcement
- `llm_orchestrator.py` - LLM-powered component generation

**Sample Documents** (`/sample-documents`)
- 5 example markdown files demonstrating different layout types

## Project Structure

```
second-brain-research-dashboard/
├── frontend/
│   ├── .env.example           # Frontend environment template
│   └── src/
│       ├── components/
│       │   ├── A2UI/          # 59 components in 11 categories
│       │   └── ui/            # Shadcn/ui base components
│       ├── hooks/
│       │   └── useDashboardAgent.ts  # AG-UI state management hook
│       ├── lib/
│       │   └── a2ui-catalog.tsx      # Component registry
│       └── App.tsx            # Main app with split-panel layout
├── agent/
│   ├── .env.example           # Backend environment template
│   ├── main.py                # FastAPI server with AG-UI endpoint
│   ├── agent.py               # Pydantic AI agent with DashboardState
│   ├── content_analyzer.py    # Markdown parsing & classification
│   ├── layout_selector.py     # Layout strategy selection
│   ├── llm_orchestrator.py    # LLM-powered orchestration
│   └── a2ui_generator.py      # Component generation
└── sample-documents/          # Demo markdown files
```

## Environment Variables

### Backend (`agent/.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENROUTER_API_KEY` | Yes | - | Your OpenRouter API key |
| `OPENROUTER_MODEL` | No | `anthropic/claude-sonnet-4` | LLM model to use |
| `BACKEND_PORT` | No | `8000` | Server port |

### Frontend (`frontend/.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VITE_BACKEND_URL` | No | `http://localhost:8000` | Backend API URL |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/agent` | POST | AG-UI protocol endpoint (primary) |
| `/ag-ui/stream` | POST | Legacy SSE streaming endpoint |
| `/docs` | GET | OpenAPI documentation |

## Tech Stack

- **AG-UI Protocol**: Server-Sent Events with JSON Patch state deltas
- **A2UI (Agent-to-UI)**: Component specification pattern for generative UI
- **Pydantic AI**: Python AI agent framework with tools and state management
- **FastAPI**: High-performance Python web framework
- **React 19**: Frontend framework with TypeScript
- **Vite**: Fast build tooling
