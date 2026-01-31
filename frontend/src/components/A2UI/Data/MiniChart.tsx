/**
 * MiniChart Component
 *
 * Displays a simple inline SVG chart (line or bar type).
 * Auto-scales to data range and supports customizable colors.
 */

import React from 'react';

export interface MiniChartProps {
  /** Array of numeric data points */
  data: number[];

  /** Optional label for the chart */
  label?: string;

  /** Chart type (defaults to 'bar') */
  type?: 'line' | 'bar';

  /** Optional color theme */
  color?: string;

  /** Optional height in pixels (defaults to 48) */
  height?: number;
}

/**
 * MiniChart Component
 *
 * A compact SVG-based chart component for displaying
 * simple data visualizations inline.
 */
export function MiniChart({
  data,
  label,
  type = 'bar',
  color = 'primary',
  height = 48,
}: MiniChartProps): React.ReactElement {
  if (!data || data.length === 0) {
    return (
      <div className="space-y-1">
        {label && <div className="text-xs text-muted-foreground dark:text-slate-400">{label}</div>}
        <div className="text-xs text-muted-foreground dark:text-slate-400">No data</div>
      </div>
    );
  }

  const maxValue = Math.max(...data);
  const minValue = Math.min(...data);
  const range = maxValue - minValue || 1;

  const getColorClass = () => {
    return color ? `bg-${color}-500` : 'bg-primary';
  };

  const getStrokeColor = () => {
    switch (color) {
      case 'success':
        return '#22c55e';
      case 'warning':
        return '#eab308';
      case 'danger':
        return '#ef4444';
      default:
        return 'currentColor';
    }
  };

  const renderBarChart = () => {
    return (
      <div className="flex items-end gap-1" style={{ height }}>
        {data.map((value: number, idx: number) => {
          const heightPercent = ((value - minValue) / range) * 100;
          return (
            <div
              key={idx}
              className={`flex-1 ${getColorClass()} rounded-t transition-all hover:opacity-80`}
              style={{ height: `${heightPercent}%`, minHeight: '2px' }}
              title={`${value}`}
            />
          );
        })}
      </div>
    );
  };

  const renderLineChart = () => {
    const width = 200;
    const padding = 4;
    const segmentWidth = (width - padding * 2) / (data.length - 1 || 1);

    const points = data.map((value, idx) => {
      const x = padding + idx * segmentWidth;
      const y = height - padding - ((value - minValue) / range) * (height - padding * 2);
      return `${x},${y}`;
    }).join(' ');

    return (
      <svg width={width} height={height} className="w-full">
        <polyline
          points={points}
          fill="none"
          stroke={getStrokeColor()}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className={color ? `text-${color}-500` : 'text-primary'}
        />
        {data.map((value, idx) => {
          const x = padding + idx * segmentWidth;
          const y = height - padding - ((value - minValue) / range) * (height - padding * 2);
          return (
            <circle
              key={idx}
              cx={x}
              cy={y}
              r="3"
              fill={getStrokeColor()}
              className={color ? `text-${color}-500` : 'text-primary'}
            >
              <title>{value}</title>
            </circle>
          );
        })}
      </svg>
    );
  };

  return (
    <div className="space-y-1">
      {label && (
        <div className="text-xs text-muted-foreground dark:text-slate-400">{label}</div>
      )}
      {type === 'bar' ? renderBarChart() : renderLineChart()}
    </div>
  );
}

export default MiniChart;
