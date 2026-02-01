import { Sparkles, FileText, Zap } from 'lucide-react'
import { Card } from '@/components/ui/card'

export function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[500px] animate-fade-in">
      <div className="max-w-2xl text-center space-y-6">
        {/* Icon */}
        <div className="relative inline-block">
          <div className="absolute inset-0 bg-blue-500/30 rounded-full blur-2xl animate-pulse" />
          <div className="relative bg-gradient-to-br from-blue-500/20 to-blue-600/10 p-6 rounded-full border border-blue-500/20">
            <Sparkles className="h-16 w-16 text-blue-400" />
          </div>
        </div>

        {/* Title */}
        <div className="space-y-2">
          <h3 className="text-2xl font-bold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
            No Dashboard Yet
          </h3>
          <p className="text-muted-foreground">
            Transform your research into an interactive dashboard in seconds
          </p>
        </div>

        {/* Instructions */}
        <Card className="p-6 bg-gradient-to-br from-card to-secondary/30 backdrop-blur-sm border-2 border-dashed border-blue-500/30">
          <div className="space-y-4 text-left">
            <h4 className="font-semibold text-foreground flex items-center gap-2">
              <Zap className="h-4 w-4 text-blue-400" />
              How to get started:
            </h4>
            <ol className="space-y-3 text-sm text-muted-foreground">
              <li className="flex gap-3">
                <span className="flex-shrink-0 flex items-center justify-center h-6 w-6 rounded-full bg-blue-500/20 text-blue-400 font-semibold text-xs border border-blue-500/30">
                  1
                </span>
                <span>
                  <strong className="text-blue-300">Enter or upload</strong> your markdown research content in the left panel
                </span>
              </li>
              <li className="flex gap-3">
                <span className="flex-shrink-0 flex items-center justify-center h-6 w-6 rounded-full bg-blue-500/20 text-blue-400 font-semibold text-xs border border-blue-500/30">
                  2
                </span>
                <span>
                  <strong className="text-blue-300">Click "Generate Dashboard"</strong> to start the AI analysis
                </span>
              </li>
              <li className="flex gap-3">
                <span className="flex-shrink-0 flex items-center justify-center h-6 w-6 rounded-full bg-blue-500/20 text-blue-400 font-semibold text-xs border border-blue-500/30">
                  3
                </span>
                <span>
                  <strong className="text-blue-300">Watch</strong> as your content transforms into interactive components
                </span>
              </li>
            </ol>
          </div>
        </Card>

        {/* Example Markdown Hint */}
        <Card className="p-4 bg-gradient-to-r from-secondary/50 to-muted/30 border-blue-500/20">
          <div className="flex items-start gap-3 text-left">
            <FileText className="h-5 w-5 text-blue-400 flex-shrink-0 mt-0.5" />
            <div className="space-y-1">
              <p className="text-sm font-medium text-foreground">
                Example Content
              </p>
              <p className="text-xs text-muted-foreground">
                Try pasting research notes, meeting minutes, technical documentation, or any markdown content.
                The AI will automatically extract insights and create relevant visualizations.
              </p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  )
}
