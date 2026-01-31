/**
 * ProgressRing Component
 *
 * Displays a circular SVG progress indicator with percentage.
 * Supports color variants (success, warning, danger) and custom sizing.
 */

import React from 'react';

export interface ProgressRingProps {
  /** Progress percentage (0-100) */
  percentage: number;

  /** Optional label below the ring */
  label?: string;

  /** Color variant */
  color?: 'success' | 'warning' | 'danger' | string;

  /** Optional custom size (defaults to 100px) */
  size?: number;
}

/**
 * ProgressRing Component
 *
 * A circular SVG-based progress indicator showing percentage
 * with customizable colors and optional label.
 */
export function ProgressRing({
  percentage,
  label,
  color = 'primary',
  size = 100,
}: ProgressRingProps): React.ReactElement {
  const radius = 45;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference * (1 - percentage / 100);

  const getColorClass = () => {
    switch (color) {
      case 'success':
        return 'text-green-500';
      case 'warning':
        return 'text-yellow-500';
      case 'danger':
        return 'text-red-500';
      default:
        return color ? `text-${color}-500` : 'text-primary';
    }
  };

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: size, height: size }}>
        <svg
          className="transform -rotate-90"
          width="100%"
          height="100%"
          viewBox="0 0 100 100"
        >
          {/* Background circle */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className="text-muted opacity-20"
          />
          {/* Progress circle */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className={getColorClass()}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
          />
        </svg>
        {/* Center text */}
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-xl font-bold dark:text-slate-100">{Math.round(percentage)}%</span>
        </div>
      </div>
      {label && (
        <span className="text-sm text-muted-foreground dark:text-slate-400">{label}</span>
      )}
    </div>
  );
}

export default ProgressRing;
