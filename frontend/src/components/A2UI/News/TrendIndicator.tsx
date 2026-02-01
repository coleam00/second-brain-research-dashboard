/**
 * TrendIndicator Component
 *
 * Displays a metric with its current value, change percentage,
 * and trend direction (up, down, or stable).
 */

import React from 'react';

export interface TrendIndicatorProps {
  /** Name of the metric being tracked (accepts both 'metric' and 'label' from backend) */
  metric?: string;
  label?: string;

  /** Current value of the metric */
  value: string | number;

  /** Change amount or percentage (can be string or number) */
  change?: string | number;

  /** Trend direction */
  trend: 'up' | 'down' | 'stable';

  /** Optional time period for the trend */
  period?: string;

  /** Optional unit from backend */
  unit?: string;
}

/**
 * TrendIndicator Component
 *
 * A compact component showing metric trends with visual indicators
 * for up/down/stable changes.
 */
export function TrendIndicator({
  metric,
  label,
  value,
  change,
  trend,
  period,
  unit,
}: TrendIndicatorProps): React.ReactElement {
  // Support both 'metric' and 'label' prop names (backend sends 'label')
  const displayMetric = metric || label || 'Metric';

  // Format change as string with optional unit
  const formatChange = () => {
    if (change === undefined || change === null) return '';
    const changeStr = typeof change === 'number' ? change.toString() : change;
    const prefix = typeof change === 'number' && change > 0 ? '+' : '';
    return `${prefix}${changeStr}${unit || ''}`;
  };

  const getTrendColor = () => {
    if (trend === 'up') return 'text-blue-400';
    if (trend === 'down') return 'text-blue-300';
    return 'text-blue-400/60';
  };

  const getTrendIcon = () => {
    if (trend === 'up') return '↑';
    if (trend === 'down') return '↓';
    return '→';
  };

  return (
    <div className="flex items-center gap-2 p-3 rounded-lg bg-gradient-to-br from-card to-secondary/30 border border-blue-500/20 hover:border-blue-400/40 transition-all duration-300">
      <div className="flex-1">
        <div className="text-sm font-medium text-blue-200">{displayMetric}</div>
        <div className="text-2xl font-bold text-white">{value}{unit && <span className="text-lg text-blue-300/60 ml-1">{unit}</span>}</div>
      </div>
      <div className={`flex items-center gap-1 ${getTrendColor()}`}>
        <span className="text-lg animate-pulse" aria-label={`Trend ${trend}`}>
          {getTrendIcon()}
        </span>
        {formatChange() && <span className="font-semibold">{formatChange()}</span>}
      </div>
      {period && (
        <div className="text-xs text-blue-300/70">{period}</div>
      )}
    </div>
  );
}

export default TrendIndicator;
