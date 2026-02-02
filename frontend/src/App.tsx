import { useState, useCallback, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import remarkBreaks from 'remark-breaks'
import { MarkdownInput } from "@/components/MarkdownInput"
import { A2UIRenderer, A2UIRendererList } from "@/components/A2UIRenderer"
import { LoadingSkeleton } from "@/components/LoadingSkeleton"
import type { SemanticZone } from "@/lib/a2ui-catalog"
import { getGridSpan } from "@/lib/layout-engine"
import { useDashboardAgent } from "@/hooks/useDashboardAgent"
import {
  FileText, Sparkles, ArrowLeft, RotateCcw, LayoutDashboard,
  BookOpen, TrendingUp, Lightbulb, FileCode, Video, Link2, Tags
} from "lucide-react"
import { Button } from "@/components/ui/button"

// Zone configuration for visual styling
const ZONE_CONFIG: Record<SemanticZone, { title: string; icon: React.ReactNode; className: string }> = {
  hero: { title: '', icon: null, className: '' }, // Hero has no header
  metrics: { title: 'Key Metrics', icon: <TrendingUp className="h-4 w-4" />, className: 'bg-gradient-to-r from-blue-500/10 to-cyan-500/10 border-blue-500/20' },
  insights: { title: 'Key Insights', icon: <Lightbulb className="h-4 w-4" />, className: 'bg-gradient-to-r from-amber-500/10 to-orange-500/10 border-amber-500/20' },
  content: { title: 'Details', icon: <FileCode className="h-4 w-4" />, className: 'bg-gradient-to-r from-purple-500/10 to-pink-500/10 border-purple-500/20' },
  media: { title: 'Media', icon: <Video className="h-4 w-4" />, className: 'bg-gradient-to-r from-rose-500/10 to-red-500/10 border-rose-500/20' },
  resources: { title: 'Resources', icon: <Link2 className="h-4 w-4" />, className: 'bg-gradient-to-r from-emerald-500/10 to-green-500/10 border-emerald-500/20' },
  tags: { title: 'Categories', icon: <Tags className="h-4 w-4" />, className: 'bg-gradient-to-r from-slate-500/10 to-gray-500/10 border-slate-500/20' },
};

// Zone render order
const ZONE_ORDER: SemanticZone[] = ['hero', 'metrics', 'insights', 'content', 'media', 'resources', 'tags'];

type ViewState = 'input' | 'loading' | 'dashboard'
type DashboardTab = 'dashboard' | 'source'

function App() {
  const [viewState, setViewState] = useState<ViewState>('input')
  const [dashboardTab, setDashboardTab] = useState<DashboardTab>('dashboard')

  // Use AG-UI agent hook for state management
  const {
    state,
    componentsByZone,
    generateDashboard,
    isGenerating,
    isComplete,
  } = useDashboardAgent()

  // Handle generate action
  const handleGenerate = useCallback((content: string, _file?: File) => {
    console.log('Generate dashboard:', { contentLength: content.length })
    setViewState('loading')
    generateDashboard(content)
  }, [generateDashboard])

  // Watch for completion and transition views
  useEffect(() => {
    if (isComplete && viewState === 'loading') {
      setViewState('dashboard')
    }
  }, [isComplete, viewState])

  const handleBackToInput = useCallback(() => {
    setViewState('input')
  }, [])

  const handleRegenerate = useCallback(() => {
    if (state.markdown_content) {
      handleGenerate(state.markdown_content)
    }
  }, [state.markdown_content, handleGenerate])

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header - compact for dashboard, full for input */}
      <AnimatePresence mode="wait">
        {viewState === 'dashboard' ? (
          <motion.header
            key="compact-header"
            className="sticky top-0 z-50 border-b border-blue-500/20 bg-card/95 backdrop-blur-sm shadow-lg shadow-black/10"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            <div className="px-4 py-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={handleBackToInput}
                    className="gap-2 text-muted-foreground hover:text-foreground"
                  >
                    <ArrowLeft className="h-4 w-4" />
                    Back
                  </Button>
                  <div className="h-6 w-px bg-border" />
                  <div className="flex items-center gap-2">
                    <Sparkles className="h-5 w-5 text-blue-400" />
                    <span className="font-semibold text-sm">
                      {state.document_title || "Research Dashboard"}
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  {/* Tab toggle */}
                  <div className="flex items-center bg-secondary/50 rounded-lg p-0.5">
                    <Button
                      variant={dashboardTab === 'dashboard' ? 'default' : 'ghost'}
                      size="sm"
                      onClick={() => setDashboardTab('dashboard')}
                      className="gap-1.5 h-7 px-3"
                    >
                      <LayoutDashboard className="h-3.5 w-3.5" />
                      Dashboard
                    </Button>
                    <Button
                      variant={dashboardTab === 'source' ? 'default' : 'ghost'}
                      size="sm"
                      onClick={() => setDashboardTab('source')}
                      className="gap-1.5 h-7 px-3"
                    >
                      <BookOpen className="h-3.5 w-3.5" />
                      Source
                    </Button>
                  </div>
                  <div className="h-6 w-px bg-border" />
                  <span className="text-xs text-muted-foreground">
                    {state.components.length} components
                  </span>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={handleRegenerate}
                    disabled={isGenerating}
                    className="gap-2"
                  >
                    <RotateCcw className={`h-3 w-3 ${isGenerating ? 'animate-spin' : ''}`} />
                    Regenerate
                  </Button>
                </div>
              </div>
            </div>
            <div className="h-px bg-gradient-to-r from-transparent via-blue-500/50 to-transparent" />
          </motion.header>
        ) : (
          <motion.header
            key="full-header"
            className="border-b border-blue-500/20 bg-gradient-to-r from-card via-card to-secondary/30 shadow-lg shadow-black/20"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.4, ease: "easeOut" }}
          >
            <div className="px-6 py-4">
              <div className="flex items-center gap-3">
                <motion.div
                  initial={{ rotate: -180, scale: 0 }}
                  animate={{ rotate: 0, scale: 1 }}
                  transition={{ duration: 0.5, ease: "easeOut", delay: 0.2 }}
                  className="relative"
                >
                  <div className="absolute inset-0 bg-blue-500/20 rounded-full blur-xl" />
                  <Sparkles className="h-8 w-8 text-blue-400 relative" />
                </motion.div>
                <motion.div
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.4, ease: "easeOut", delay: 0.3 }}
                >
                  <h1 className="text-2xl font-bold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
                    Second Brain Research Dashboard
                  </h1>
                  <p className="text-sm text-muted-foreground">
                    Transform markdown into AI-powered dashboards with CopilotKit + AG-UI
                  </p>
                </motion.div>
              </div>
            </div>
            <div className="h-px bg-gradient-to-r from-transparent via-blue-500/50 to-transparent" />
          </motion.header>
        )}
      </AnimatePresence>

      {/* Main content area with optional chat sidebar */}
      <div className="flex">
        <div className="flex-1">
          <AnimatePresence mode="wait">
            {/* Input View */}
            {viewState === 'input' && (
              <motion.main
                key="input-view"
                className="min-h-[calc(100vh-5rem)]"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.4 }}
              >
                <div className="max-w-4xl mx-auto px-4 py-8">
                  <motion.div
                    className="mb-6"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.2 }}
                  >
                    <div className="flex items-center gap-2 mb-2">
                      <FileText className="h-5 w-5 text-blue-400" />
                      <h2 className="text-lg font-semibold text-foreground">Enter Your Research</h2>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      Paste markdown or drag a .md file. The AI agent will analyze and generate a dashboard.
                    </p>
                  </motion.div>

                  <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.3 }}
                    className="bg-card rounded-xl border border-border p-6 shadow-xl"
                  >
                    <MarkdownInput
                      onGenerate={handleGenerate}
                      placeholder="# Your Research Title

## Introduction
Enter your research content here...

## Key Findings
- Finding 1
- Finding 2

## Data & Statistics
- 85% improvement in efficiency
- $2.5M cost savings

## Code Examples
```python
def analyze_data(content):
    return insights
```

## Conclusion
Your conclusions here..."
                      initialValue={state.markdown_content}
                    />
                  </motion.div>

                  <motion.div
                    className="mt-6 text-center"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.4, delay: 0.5 }}
                  >
                    <p className="text-xs text-muted-foreground">
                      Tip: Include statistics, code blocks, links, and structured sections for best results
                    </p>
                  </motion.div>
                </div>
              </motion.main>
            )}

            {/* Loading View - shows real-time progress from agent state */}
            {viewState === 'loading' && (
              <motion.main
                key="loading-view"
                className="min-h-[calc(100vh-5rem)]"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.3 }}
              >
                <div className="max-w-6xl mx-auto px-4 py-8">
                  <div className="text-center mb-8">
                    <Sparkles className="h-8 w-8 text-blue-400 animate-pulse mx-auto" />
                    <h2 className="text-xl font-semibold mt-4">
                      {state.current_step || "Generating Your Dashboard"}
                    </h2>
                    {/* Progress bar from agent state */}
                    <div className="max-w-md mx-auto mt-4">
                      <div className="h-2 bg-secondary rounded-full overflow-hidden">
                        <motion.div
                          className="h-full bg-gradient-to-r from-blue-500 to-cyan-500"
                          initial={{ width: 0 }}
                          animate={{ width: `${state.progress}%` }}
                          transition={{ duration: 0.3 }}
                        />
                      </div>
                      <p className="text-sm text-muted-foreground mt-2">
                        {state.progress}% complete
                      </p>
                    </div>
                    {/* Activity log */}
                    <div className="mt-4 space-y-1">
                      {state.activity_log.slice(-5).map((log) => (
                        <p key={log.id} className="text-xs text-muted-foreground">
                          {log.status === 'completed' ? '✓' : '⏳'} {log.message}
                        </p>
                      ))}
                    </div>
                  </div>

                  {/* Show components as they stream in */}
                  {state.components.length > 0 ? (
                    <div className="space-y-6 animate-fade-in">
                      <A2UIRendererList
                        components={state.components}
                        spacing="lg"
                        showErrors={true}
                      />
                    </div>
                  ) : (
                    <LoadingSkeleton />
                  )}
                </div>
              </motion.main>
            )}

            {/* Dashboard View */}
            {viewState === 'dashboard' && (
              <motion.main
                key="dashboard-view"
                className="min-h-[calc(100vh-3rem)]"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.4 }}
              >
                <div className="max-w-7xl mx-auto px-4 py-6">
                  <AnimatePresence mode="wait">
                    {dashboardTab === 'dashboard' ? (
                      /* Zone-based dashboard layout */
                      <motion.div
                        key="dashboard-content"
                        className="space-y-8"
                        initial="hidden"
                        animate="visible"
                        exit={{ opacity: 0 }}
                        variants={{
                          hidden: { opacity: 0 },
                          visible: {
                            opacity: 1,
                            transition: { staggerChildren: 0.15 }
                          }
                        }}
                      >
                        {ZONE_ORDER.map((zone) => {
                          const components = componentsByZone[zone];
                          if (!components || components.length === 0) return null;

                          const config = ZONE_CONFIG[zone];

                          // Hero zone - no wrapper, full prominence
                          if (zone === 'hero') {
                            return (
                              <motion.div
                                key={zone}
                                className="space-y-4"
                                variants={{
                                  hidden: { opacity: 0, y: 20 },
                                  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
                                }}
                              >
                                {components.map((component, index) => (
                                  <div key={component.id || `${zone}-${index}`} className="col-span-12">
                                    <A2UIRenderer component={component} showErrors={true} />
                                  </div>
                                ))}
                              </motion.div>
                            );
                          }

                          // Metrics zone - horizontal layout
                          if (zone === 'metrics') {
                            return (
                              <motion.section
                                key={zone}
                                className={`rounded-xl border p-6 ${config.className}`}
                                variants={{
                                  hidden: { opacity: 0, y: 20 },
                                  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
                                }}
                              >
                                <div className="flex items-center gap-2 mb-4">
                                  <span className="text-blue-400">{config.icon}</span>
                                  <h2 className="text-lg font-semibold text-blue-100">{config.title}</h2>
                                </div>
                                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                                  {components.map((component, index) => (
                                    <A2UIRenderer key={component.id || `${zone}-${index}`} component={component} showErrors={true} />
                                  ))}
                                </div>
                              </motion.section>
                            );
                          }

                          // Tags zone - compact horizontal layout
                          if (zone === 'tags') {
                            return (
                              <motion.section
                                key={zone}
                                className={`rounded-xl border p-4 ${config.className}`}
                                variants={{
                                  hidden: { opacity: 0, y: 20 },
                                  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
                                }}
                              >
                                <div className="flex items-center gap-2 mb-3">
                                  <span className="text-slate-400">{config.icon}</span>
                                  <h2 className="text-sm font-semibold text-slate-300">{config.title}</h2>
                                </div>
                                <div className="flex flex-wrap gap-2">
                                  {components.map((component, index) => (
                                    <A2UIRenderer key={component.id || `${zone}-${index}`} component={component} showErrors={true} />
                                  ))}
                                </div>
                              </motion.section>
                            );
                          }

                          // Other zones - grid layout
                          return (
                            <motion.section
                              key={zone}
                              className={`rounded-xl border p-6 ${config.className}`}
                              variants={{
                                hidden: { opacity: 0, y: 20 },
                                visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
                              }}
                            >
                              <div className="flex items-center gap-2 mb-4">
                                <span className="text-blue-400">{config.icon}</span>
                                <h2 className="text-lg font-semibold text-blue-100">{config.title}</h2>
                                <span className="text-xs text-muted-foreground ml-auto">
                                  {components.length} {components.length === 1 ? 'item' : 'items'}
                                </span>
                              </div>
                              <div className="grid grid-cols-12 gap-4 auto-rows-min">
                                {components.map((component, index) => (
                                  <div
                                    key={component.id || `${zone}-${index}`}
                                    className={getGridSpan(component)}
                                  >
                                    <A2UIRenderer component={component} showErrors={true} />
                                  </div>
                                ))}
                              </div>
                            </motion.section>
                          );
                        })}
                      </motion.div>
                    ) : (
                      /* Source view */
                      <motion.div
                        key="source-content"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0 }}
                        transition={{ duration: 0.3 }}
                        className="bg-card rounded-xl border border-blue-500/20 p-6 shadow-xl"
                      >
                        <div className="flex items-center gap-2 mb-4 pb-4 border-b border-border">
                          <BookOpen className="h-5 w-5 text-blue-400" />
                          <h2 className="text-lg font-semibold">Source Document</h2>
                          <span className="text-xs text-muted-foreground ml-auto">
                            {state.markdown_content.length} characters
                          </span>
                        </div>
                        <div className="markdown-source">
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm, remarkBreaks]}
                            components={{
                              h1: ({children}) => <h1 className="text-3xl font-bold text-blue-100 border-b border-blue-500/30 pb-3 mb-6 mt-0">{children}</h1>,
                              h2: ({children}) => <h2 className="text-2xl font-bold text-blue-100 border-b border-blue-500/20 pb-2 mb-4 mt-10">{children}</h2>,
                              h3: ({children}) => <h3 className="text-xl font-semibold text-blue-100 mb-3 mt-8">{children}</h3>,
                              h4: ({children}) => <h4 className="text-lg font-semibold text-blue-200 mb-2 mt-6">{children}</h4>,
                              p: ({children}) => <p className="text-blue-200 leading-relaxed mb-4">{children}</p>,
                              strong: ({children}) => <strong className="text-blue-100 font-semibold">{children}</strong>,
                              em: ({children}) => <em className="text-blue-300 italic">{children}</em>,
                              ul: ({children}) => <ul className="text-blue-200 my-4 ml-6 list-disc space-y-2">{children}</ul>,
                              ol: ({children}) => <ol className="text-blue-200 my-4 ml-6 list-decimal space-y-2">{children}</ol>,
                              li: ({children}) => <li className="text-blue-200 marker:text-blue-400">{children}</li>,
                              a: ({href, children}) => <a href={href} className="text-blue-400 underline hover:text-blue-300 transition-colors">{children}</a>,
                              code: ({className, children}) => {
                                const isInline = !className;
                                if (isInline) {
                                  return <code className="text-blue-300 bg-blue-900/40 px-1.5 py-0.5 rounded text-sm font-mono">{children}</code>;
                                }
                                return (
                                  <code className={`${className} block bg-secondary/60 border border-blue-500/20 rounded-lg p-4 my-4 overflow-x-auto text-sm font-mono text-blue-200`}>
                                    {children}
                                  </code>
                                );
                              },
                              pre: ({children}) => <pre className="bg-secondary/60 border border-blue-500/20 rounded-lg p-4 my-6 overflow-x-auto">{children}</pre>,
                              blockquote: ({children}) => <blockquote className="border-l-4 border-blue-500 pl-4 my-6 text-blue-300 italic">{children}</blockquote>,
                              table: ({children}) => <table className="w-full border-collapse my-6">{children}</table>,
                              thead: ({children}) => <thead className="bg-blue-900/30">{children}</thead>,
                              th: ({children}) => <th className="text-blue-100 p-3 text-left border border-blue-500/20 font-semibold">{children}</th>,
                              td: ({children}) => <td className="p-3 border border-blue-500/20 text-blue-200">{children}</td>,
                              hr: () => <hr className="border-blue-500/30 my-8" />,
                            }}
                          >
                            {state.markdown_content}
                          </ReactMarkdown>
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </motion.main>
            )}
          </AnimatePresence>
        </div>

      </div>
    </div>
  )
}

export default App
