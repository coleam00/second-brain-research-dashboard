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
        {label && <div className="text-xs text-blue-300/70">{label}</div>}
        <div className="text-xs text-muted-foreground">No data</div>
      </div>
    );
  }

  const maxValue = Math.max(...data);
  const minValue = Math.min(...data);
  const range = maxValue - minValue || 1;

  const getStrokeColor = () => {
    switch (color) {
      case 'success':
        return '#34d399';
      case 'warning':
        return '#fbbf24';
      case 'danger':
        return '#f87171';
      default:
        return '#60a5fa';
    }
  };

  const renderBarChart = () => {
    return (
      <div className="flex items-end gap-1 p-2 rounded-lg bg-secondary/30" style={{ height }}>
        {data.map((value: number, idx: number) => {
          const heightPercent = ((value - minValue) / range) * 100;
          return (
            <div
              key={idx}
              className="flex-1 bg-gradient-to-t from-blue-600 to-blue-400 rounded-t transition-all hover:from-blue-500 hover:to-blue-300 shadow-sm shadow-blue-500/30"
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
      <div className="p-2 rounded-lg bg-secondary/30">
        <svg width={width} height={height} className="w-full">
          <defs>
            <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
              <stop offset="0%" stopColor="#3b82f6" />
              <stop offset="100%" stopColor="#60a5fa" />
            </linearGradient>
          </defs>
          <polyline
            points={points}
            fill="none"
            stroke="url(#lineGradient)"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{ filter: 'drop-shadow(0 0 4px rgba(59, 130, 246, 0.5))' }}
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
                style={{ filter: 'drop-shadow(0 0 3px rgba(59, 130, 246, 0.5))' }}
              >
                <title>{value}</title>
              </circle>
            );
          })}
        </svg>
      </div>
    );
  };

  return (
    <div className="space-y-1">
      {label && (
        <div className="text-xs text-blue-300/70">{label}</div>
      )}
      {type === 'bar' ? renderBarChart() : renderLineChart()}
    </div>
  );
}

export default MiniChart;
