/**
 * ComparisonBar Component
 *
 * Displays horizontal bars comparing two values side-by-side.
 * Auto-scales to the maximum value and shows labels for each bar.
 */

import React from 'react';

export interface ComparisonBarProps {
  /** Main label for the comparison */
  label: string;

  /** First value to compare */
  value_a: number;

  /** Second value to compare */
  value_b: number;

  /** Label for first value */
  label_a: string;

  /** Label for second value */
  label_b: string;

  /** Optional maximum value for scaling (defaults to max of both values) */
  max_value?: number;

  /** Optional color for first bar (defaults to blue) */
  color_a?: string;

  /** Optional color for second bar (defaults to purple) */
  color_b?: string;
}

/**
 * ComparisonBar Component
 *
 * A horizontal bar chart component for comparing two values
 * with automatic scaling and customizable colors.
 */
export function ComparisonBar({
  label,
  value_a,
  value_b,
  label_a,
  label_b,
  max_value,
  color_a = 'blue',
  color_b = 'purple',
}: ComparisonBarProps): React.ReactElement {
  const maxVal = max_value || Math.max(value_a, value_b);
  const percentA = (value_a / maxVal) * 100;
  const percentB = (value_b / maxVal) * 100;

  return (
    <div className="space-y-2">
      <div className="text-sm font-medium dark:text-slate-200">{label}</div>
      <div className="flex items-center gap-2">
        <span className="text-xs w-20 text-right text-muted-foreground dark:text-slate-400">
          {label_a}
        </span>
        <div className="flex-1 h-6 bg-muted dark:bg-slate-800 rounded-full overflow-hidden flex">
          <div
            className={`bg-${color_a}-500 h-full transition-all`}
            style={{ width: `${percentA}%` }}
          />
        </div>
        <span className="text-xs w-12 font-semibold dark:text-slate-100">{value_a}</span>
      </div>
      <div className="flex items-center gap-2">
        <span className="text-xs w-20 text-right text-muted-foreground dark:text-slate-400">
          {label_b}
        </span>
        <div className="flex-1 h-6 bg-muted dark:bg-slate-800 rounded-full overflow-hidden flex">
          <div
            className={`bg-${color_b}-500 h-full transition-all`}
            style={{ width: `${percentB}%` }}
          />
        </div>
        <span className="text-xs w-12 font-semibold dark:text-slate-100">{value_b}</span>
      </div>
    </div>
  );
}

export default ComparisonBar;
