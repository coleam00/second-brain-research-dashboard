/**
 * ComparisonBar Component
 *
 * Displays horizontal bars comparing multiple values.
 * Auto-scales to the maximum value and shows labels for each bar.
 */

import React from 'react';

interface ComparisonItem {
  label: string;
  value: number;
  color?: string;
}

export interface ComparisonBarProps {
  /** Main label for the comparison */
  label: string;

  /** Array of items to compare (from backend) */
  items?: ComparisonItem[];

  /** Optional maximum value for scaling (accepts both snake_case and camelCase) */
  max_value?: number;
  maxValue?: number;

  // Legacy props for two-value comparison
  /** First value to compare (legacy) */
  value_a?: number;
  /** Second value to compare (legacy) */
  value_b?: number;
  /** Label for first value (legacy) */
  label_a?: string;
  /** Label for second value (legacy) */
  label_b?: string;
}

// Color palette for bars
const BAR_COLORS = [
  'from-blue-600 to-blue-400 shadow-blue-500/30',
  'from-cyan-500 to-blue-500 shadow-cyan-500/30',
  'from-purple-500 to-blue-500 shadow-purple-500/30',
  'from-teal-500 to-cyan-500 shadow-teal-500/30',
  'from-indigo-500 to-blue-500 shadow-indigo-500/30',
];

/**
 * ComparisonBar Component
 *
 * A horizontal bar chart component for comparing values
 * with automatic scaling and customizable colors.
 */
export function ComparisonBar({
  label,
  items,
  max_value,
  maxValue,
  value_a,
  value_b,
  label_a,
  label_b,
}: ComparisonBarProps): React.ReactElement {
  // Support both items array (backend) and legacy two-value format
  const displayItems: ComparisonItem[] = items && items.length > 0
    ? items
    : [
        ...(value_a !== undefined && label_a ? [{ label: label_a, value: value_a }] : []),
        ...(value_b !== undefined && label_b ? [{ label: label_b, value: value_b }] : []),
      ];

  // Calculate max value
  const calculatedMax = max_value || maxValue || Math.max(...displayItems.map(item => item.value), 1);

  if (displayItems.length === 0) {
    return (
      <div className="p-4 rounded-xl bg-secondary/30 border border-blue-500/10">
        <div className="text-sm text-blue-300/70">No data to display</div>
      </div>
    );
  }

  return (
    <div className="space-y-3 p-4 rounded-xl bg-secondary/30 border border-blue-500/10">
      <div className="text-sm font-medium text-blue-200">{label}</div>
      {displayItems.map((item, index) => {
        const percent = (item.value / calculatedMax) * 100;
        const colorClass = BAR_COLORS[index % BAR_COLORS.length];

        return (
          <div key={item.label || index} className="flex items-center gap-2">
            <span className="text-xs w-24 text-right text-blue-300/70 truncate" title={item.label}>
              {item.label}
            </span>
            <div className="flex-1 h-6 bg-secondary rounded-full overflow-hidden flex">
              <div
                className={`bg-gradient-to-r ${colorClass} h-full transition-all duration-500 shadow-lg`}
                style={{ width: `${Math.min(percent, 100)}%` }}
              />
            </div>
            <span className="text-xs w-14 font-semibold text-white text-right">{item.value}</span>
          </div>
        );
      })}
    </div>
  );
}

export default ComparisonBar;
