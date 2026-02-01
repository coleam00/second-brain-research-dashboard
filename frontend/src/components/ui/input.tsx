import * as React from "react"

import { cn } from "@/lib/utils"

const Input = React.forwardRef<HTMLInputElement, React.ComponentProps<"input">>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-lg border border-border/50 bg-secondary/50 px-3 py-2 text-base text-foreground ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500/50 focus-visible:ring-offset-0 focus-visible:border-blue-500/50 disabled:cursor-not-allowed disabled:opacity-50 md:text-sm transition-all duration-200 hover:border-blue-500/30 hover:bg-secondary/70",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input }
