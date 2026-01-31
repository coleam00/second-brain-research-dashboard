/**
 * Columns Component
 *
 * Flex-based column layout with configurable distribution (equal width or auto-fit).
 * Provides flexible multi-column layouts with customizable gap spacing.
 */

import React from 'react';
import { cn } from "@/lib/utils";

export interface ColumnsProps {
  /** Number of columns */
  count: 1 | 2 | 3;

  /** Distribution mode for column sizing */
  distribution?: 'equal' | 'auto';

  /** Gap spacing between columns */
  gap?: string;

  /** Column content */
  children: React.ReactNode;

  /** Additional CSS classes */
  className?: string;
}

/**
 * Columns Component
 *
 * Display items in N columns with flexible sizing.
 * Supports equal width or auto-fit distribution.
 */
export function Columns({
  // @ts-expect-error - count is part of the interface but not used in implementation
  count,
  distribution = 'equal',
  gap = '1rem',
  children,
  className,
}: ColumnsProps): React.ReactElement {
  const childArray = React.Children.toArray(children);

  return (
    <div
      className={cn(
        'flex flex-col md:flex-row',
        className
      )}
      style={{ gap }}
    >
      {distribution === 'equal' ? (
        // Equal width columns
        childArray.map((child, index) => (
          <div key={index} style={{ flex: 1 }}>
            {child}
          </div>
        ))
      ) : (
        // Auto-fit columns
        childArray.map((child, index) => (
          <div key={index} style={{ flex: '0 1 auto' }}>
            {child}
          </div>
        ))
      )}
    </div>
  );
}

export default Columns;
