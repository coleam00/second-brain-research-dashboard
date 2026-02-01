import * as React from "react"

import { cn } from "@/lib/utils"

const Textarea = React.forwardRef<
  HTMLTextAreaElement,
  React.ComponentProps<"textarea">
>(({ className, ...props }, ref) => {
  return (
    <textarea
      className={cn(
        "flex min-h-[80px] w-full rounded-lg border border-border/50 bg-secondary/50 px-3 py-2 text-base text-foreground ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500/50 focus-visible:ring-offset-0 focus-visible:border-blue-500/50 disabled:cursor-not-allowed disabled:opacity-50 md:text-sm transition-all duration-200 hover:border-blue-500/30 hover:bg-secondary/70",
        className
      )}
      ref={ref}
      {...props}
    />
  )
})
Textarea.displayName = "Textarea"

export { Textarea }
