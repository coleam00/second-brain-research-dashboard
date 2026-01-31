/**
 * Grid Component
 *
 * A responsive grid layout with configurable columns and gap spacing.
 * Automatically adjusts to mobile (1 column) and desktop (configurable columns).
 */

import React from 'react';
import { cn } from "@/lib/utils";

export interface GridProps {
  /** Number of columns (desktop) */
  columns?: 1 | 2 | 3 | 4;

  /** Gap spacing between grid items */
  gap?: 'sm' | 'md' | 'lg';

  /** Grid items */
  children: React.ReactNode;

  /** Additional CSS classes */
  className?: string;
}

/**
 * Grid Component
 *
 * Responsive grid layout that adapts to screen size.
 * Defaults to 2 columns on desktop, 1 column on mobile.
 */
export function Grid({
  columns = 2,
  gap = 'md',
  children,
  className,
}: GridProps): React.ReactElement {
  const gapClasses = {
    sm: 'gap-2',
    md: 'gap-4',
    lg: 'gap-6',
  };

  const columnClasses = {
    1: 'md:grid-cols-1',
    2: 'md:grid-cols-2',
    3: 'md:grid-cols-3',
    4: 'md:grid-cols-4',
  };

  return (
    <div
      className={cn(
        'grid',
        'grid-cols-1', // Mobile default
        columnClasses[columns],
        gapClasses[gap],
        className
      )}
    >
      {children}
    </div>
  );
}

export default Grid;
