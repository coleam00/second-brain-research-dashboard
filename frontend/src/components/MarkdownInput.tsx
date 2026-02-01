import * as React from "react"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Upload } from "lucide-react"
import { sampleDocuments } from "@/data/sampleDocuments"

interface MarkdownInputProps {
  onGenerate?: (content: string, file?: File) => void
  placeholder?: string
  className?: string
  initialValue?: string
}

export function MarkdownInput({
  onGenerate,
  placeholder = "Enter your markdown content or drag and drop a file...",
  className,
  initialValue = ""
}: MarkdownInputProps) {
  const [content, setContent] = React.useState(initialValue)
  const [isDragging, setIsDragging] = React.useState(false)

  // Update content when initialValue changes (e.g., when going back to input view)
  React.useEffect(() => {
    if (initialValue) {
      setContent(initialValue)
    }
  }, [initialValue])
  const [uploadedFile, setUploadedFile] = React.useState<File | null>(null)
  const fileInputRef = React.useRef<HTMLInputElement>(null)

  // Calculate character and word count
  const charCount = content.length
  const wordCount = content.trim() === "" ? 0 : content.trim().split(/\s+/).length

  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(true)
  }

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setIsDragging(false)

    const files = Array.from(e.dataTransfer.files)
    if (files.length > 0) {
      const file = files[0]
      setUploadedFile(file)

      // Read file content if it's a text/markdown file
      if (file.type.startsWith('text/') || file.name.endsWith('.md')) {
        const text = await file.text()
        setContent(text)
      }
    }
  }

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      const file = files[0]
      setUploadedFile(file)

      // Read file content if it's a text/markdown file
      if (file.type.startsWith('text/') || file.name.endsWith('.md')) {
        const text = await file.text()
        setContent(text)
      }
    }
  }

  const handleGenerate = () => {
    if (onGenerate) {
      onGenerate(content, uploadedFile || undefined)
    }
  }

  const loadSampleDocument = (documentId: string) => {
    const doc = sampleDocuments.find(d => d.id === documentId)
    if (doc) {
      setContent(doc.content)
      setUploadedFile(null) // Clear any uploaded file
    }
  }

  return (
    <div className={cn("w-full space-y-4", className)}>
      <div
        onDragEnter={handleDragEnter}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={cn(
          "relative rounded-xl border-2 border-dashed transition-all duration-300",
          isDragging
            ? "border-blue-500 bg-blue-500/10 shadow-lg shadow-blue-500/20"
            : "border-blue-500/30 bg-secondary/30 hover:border-blue-500/50"
        )}
      >
        <div className="p-6">
          <div className="space-y-4">
            {/* File Upload Section */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Upload className="h-5 w-5 text-blue-400" />
                <span className="text-sm text-muted-foreground">
                  {uploadedFile ? <span className="text-blue-300">{uploadedFile.name}</span> : "Drag and drop a file or click to upload"}
                </span>
              </div>
              <input
                ref={fileInputRef}
                type="file"
                onChange={handleFileSelect}
                className="hidden"
                accept=".md,.txt,text/*"
              />
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => fileInputRef.current?.click()}
              >
                Browse Files
              </Button>
            </div>

            {/* Sample Documents Section */}
            <div className="space-y-2">
              <p className="text-sm font-medium text-muted-foreground">
                Or try a sample document:
              </p>
              <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
                {sampleDocuments.map((doc) => (
                  <Button
                    key={doc.id}
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => loadSampleDocument(doc.id)}
                    className="flex flex-col items-center justify-center h-auto py-3 px-2 gap-1 bg-secondary/50 border-blue-500/20 hover:bg-blue-500/20 hover:border-blue-500/50 hover:shadow-md hover:shadow-blue-500/10 transition-all duration-200"
                    title={doc.description}
                  >
                    <span className="text-2xl">{doc.icon}</span>
                    <span className="text-xs font-medium text-center leading-tight">
                      {doc.title}
                    </span>
                    <span className="text-[10px] text-muted-foreground">
                      {doc.category}
                    </span>
                  </Button>
                ))}
              </div>
            </div>

            {/* Textarea */}
            <Textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder={placeholder}
              className="min-h-[200px] resize-y font-mono text-sm"
              rows={10}
            />

            {/* Stats and Actions */}
            <div className="flex items-center justify-between">
              <div className="flex gap-4 text-sm text-muted-foreground">
                <span data-testid="char-count">
                  {charCount} character{charCount !== 1 ? 's' : ''}
                </span>
                <span data-testid="word-count">
                  {wordCount} word{wordCount !== 1 ? 's' : ''}
                </span>
              </div>
              <Button
                onClick={handleGenerate}
                disabled={content.trim() === ""}
                size="lg"
              >
                Generate Dashboard
              </Button>
            </div>
          </div>
        </div>

        {/* Drag overlay */}
        {isDragging && (
          <div className="absolute inset-0 flex items-center justify-center bg-blue-500/20 rounded-xl backdrop-blur-sm border-2 border-blue-500">
            <div className="text-center">
              <Upload className="h-12 w-12 mx-auto mb-2 text-blue-400 animate-bounce" />
              <p className="text-lg font-medium text-blue-300">Drop file here</p>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
