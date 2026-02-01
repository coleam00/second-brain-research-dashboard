import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
  {
    variants: {
      variant: {
        default:
          "border-transparent bg-gradient-to-r from-blue-600 to-blue-500 text-white shadow-sm shadow-blue-500/20",
        secondary:
          "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
        destructive:
          "border-transparent bg-gradient-to-r from-red-600 to-red-500 text-white shadow-sm shadow-red-500/20",
        outline: "border-blue-500/50 text-blue-400 bg-blue-500/10",
        success:
          "border-transparent bg-gradient-to-r from-emerald-600 to-emerald-500 text-white shadow-sm shadow-emerald-500/20",
        warning:
          "border-transparent bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-sm shadow-amber-500/20",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }
