/**
 * MetricRow Component
 *
 * Displays multiple metrics in a horizontal row with labels, values, and optional units.
 * Supports change indicators and comparison with previous values.
 */

import React from 'react';
import { Badge } from "@/components/ui/badge";

export interface Metric {
  /** Metric label */
  label: string;

  /** Current metric value */
  value: string | number;

  /** Optional unit text */
  unit?: string;
}

export interface MetricRowProps {
  /** Label for the entire row */
  label?: string;

  /** Array of metrics to display */
  metrics?: Metric[];

  /** Alternative: single metric props */
  value?: string | number;
  previous_value?: string | number;
  unit?: string;
  change_percentage?: number;
}

/**
 * MetricRow Component
 *
 * A horizontal row component for displaying multiple metrics
 * or a single metric with change indicators.
 */
export function MetricRow({
  label,
  metrics,
  value,
  previous_value,
  unit,
  change_percentage,
}: MetricRowProps): React.ReactElement {
  // Single metric mode
  if (value !== undefined && !metrics) {
    return (
      <div className="flex items-center justify-between p-3 rounded-lg hover:bg-muted/50 transition-colors">
        <span className="text-sm font-medium dark:text-slate-200">{label}</span>
        <div className="flex items-center gap-3">
          {previous_value !== undefined && (
            <span className="text-xs text-muted-foreground dark:text-slate-400 line-through">
              {previous_value}{unit}
            </span>
          )}
          <span className="text-lg font-bold dark:text-slate-100">{value}{unit}</span>
          {change_percentage !== undefined && (
            <Badge variant={change_percentage > 0 ? 'default' : 'destructive'}>
              {change_percentage > 0 ? '+' : ''}{change_percentage}%
            </Badge>
          )}
        </div>
      </div>
    );
  }

  // Multiple metrics mode
  return (
    <div className="flex items-center gap-6 p-3 rounded-lg hover:bg-muted/50 transition-colors">
      {label && <span className="text-sm font-medium dark:text-slate-200 mr-2">{label}</span>}
      <div className="flex flex-1 items-center gap-6 justify-around">
        {metrics?.map((metric: Metric, idx: number) => (
          <div key={idx} className="flex flex-col items-center gap-1">
            <span className="text-xs text-muted-foreground dark:text-slate-400">{metric.label}</span>
            <span className="text-lg font-bold dark:text-slate-100">
              {metric.value}
              {metric.unit && <span className="text-sm text-muted-foreground dark:text-slate-400 ml-1">{metric.unit}</span>}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MetricRow;
