import { useState } from 'react'
import { motion } from 'framer-motion'
import { MarkdownInput } from "@/components/MarkdownInput"
import { A2UIRendererList } from "@/components/A2UIRenderer"
import { LoadingSkeleton } from "@/components/LoadingSkeleton"
import { EmptyState } from "@/components/EmptyState"
import type { A2UIComponent } from "@/lib/a2ui-catalog"
import { FileText, Sparkles } from "lucide-react"

function App() {
  const [dashboardComponents, setDashboardComponents] = useState<A2UIComponent[]>([])
  const [isGenerating, setIsGenerating] = useState(false)

  const handleGenerate = async (content: string, file?: File) => {
    console.log('Generate dashboard called:', { content, file })
    setIsGenerating(true)

    try {
      // TODO: Call the backend orchestrator API at http://localhost:8000/ag-ui/stream
      // This will be implemented to stream A2UI components from the backend
      // For now, just log the content
      console.log('Calling orchestrator with content:', content.substring(0, 100) + '...')

      // Placeholder: In the future, this will stream components from the backend
      // const response = await fetch('http://localhost:8000/ag-ui/stream', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ content, file_name: file?.name })
      // })
      // Process streaming response and update dashboardComponents

      // For now, clear any existing dashboard
      setDashboardComponents([])
    } catch (error) {
      console.error('Error generating dashboard:', error)
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      {/* Header */}
      <motion.header
        className="border-b border-border bg-card shadow-sm"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, ease: "easeOut" }}
      >
        <div className="px-6 py-4">
          <div className="flex items-center gap-3">
            <motion.div
              initial={{ rotate: -180, scale: 0 }}
              animate={{ rotate: 0, scale: 1 }}
              transition={{ duration: 0.5, ease: "easeOut", delay: 0.2 }}
            >
              <Sparkles className="h-8 w-8 text-primary" />
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.4, ease: "easeOut", delay: 0.3 }}
            >
              <h1 className="text-2xl font-bold">Second Brain Research Dashboard</h1>
              <p className="text-sm text-muted-foreground">
                Transform your markdown research into interactive, AI-powered dashboards
              </p>
            </motion.div>
          </div>
        </div>
      </motion.header>

      {/* Split Panel Layout */}
      <div className="h-[calc(100vh-5rem)] grid grid-cols-1 md:grid-cols-2 gap-0">
        {/* Left Panel - Input */}
        <motion.div
          className="border-r border-border overflow-y-auto"
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, ease: "easeOut", delay: 0.4 }}
        >
          <div className="p-4 md:p-6">
            <motion.div
              className="mb-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.6 }}
            >
              <div className="flex items-center gap-2 mb-2">
                <FileText className="h-5 w-5 text-muted-foreground" />
                <h2 className="text-lg font-semibold">Markdown Input</h2>
              </div>
              <p className="text-sm text-muted-foreground">
                Upload or paste your research content to generate a dashboard
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.7 }}
            >
              <MarkdownInput
                onGenerate={handleGenerate}
                placeholder="Enter your markdown research content here, or drag and drop a .md file..."
              />
            </motion.div>
          </div>
        </motion.div>

        {/* Right Panel - Dashboard */}
        <motion.div
          className="overflow-y-auto bg-muted/30"
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, ease: "easeOut", delay: 0.4 }}
        >
          <div className="p-4 md:p-6">
            <motion.div
              className="mb-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4, delay: 0.6 }}
            >
              <div className="flex items-center gap-2 mb-2">
                <Sparkles className="h-5 w-5 text-muted-foreground" />
                <h2 className="text-lg font-semibold">Generated Dashboard</h2>
              </div>
              <p className="text-sm text-muted-foreground">
                Your AI-generated dashboard will appear here
              </p>
            </motion.div>

            {/* Empty State */}
            {!isGenerating && dashboardComponents.length === 0 && (
              <EmptyState />
            )}

            {/* Loading State */}
            {isGenerating && (
              <LoadingSkeleton />
            )}

            {/* A2UI Dashboard Renderer */}
            {!isGenerating && dashboardComponents.length > 0 && (
              <div className="space-y-6 animate-fade-in">
                <A2UIRendererList
                  components={dashboardComponents}
                  spacing="lg"
                  showErrors={true}
                />
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default App
