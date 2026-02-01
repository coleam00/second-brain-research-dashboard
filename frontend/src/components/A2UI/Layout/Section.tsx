/**
 * Section Component
 *
 * A layout container/wrapper with optional header (title and subtitle).
 * Provides consistent spacing and max-width constraints for content sections.
 */

import React from 'react';
import { cn } from "@/lib/utils";

export interface SectionProps {
  /** Section title */
  title?: string;

  /** Section subtitle or description */
  subtitle?: string;

  /** Content to display in the section */
  children: React.ReactNode;

  /** Full width layout (no max-width constraint) */
  fullWidth?: boolean;

  /** Maximum width of the section container */
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl';

  /** Additional CSS classes */
  className?: string;
}

/**
 * Section Component
 *
 * A flexible layout container for organizing content with optional headers.
 * Supports different max-widths and full-width layouts.
 */
export function Section({
  title,
  subtitle,
  children,
  fullWidth = false,
  maxWidth = 'lg',
  className,
}: SectionProps): React.ReactElement {
  const maxWidthClasses = {
    sm: 'max-w-2xl',
    md: 'max-w-4xl',
    lg: 'max-w-6xl',
    xl: 'max-w-7xl',
  };

  return (
    <section
      className={cn(
        'space-y-4 p-6 rounded-lg bg-gradient-to-br from-slate-900/50 to-blue-950/30 border border-blue-500/20',
        !fullWidth && maxWidthClasses[maxWidth],
        !fullWidth && 'mx-auto',
        className
      )}
    >
      {(title || subtitle) && (
        <div className="space-y-2 border-b border-blue-500/20 pb-4">
          {title && (
            <h2 className="text-2xl font-bold tracking-tight text-white bg-gradient-to-r from-blue-400 to-blue-200 bg-clip-text text-transparent">
              {title}
            </h2>
          )}
          {subtitle && (
            <p className="text-sm text-blue-300/80">
              {subtitle}
            </p>
          )}
        </div>
      )}
      <div className="space-y-4">{children}</div>
    </section>
  );
}

export default Section;
