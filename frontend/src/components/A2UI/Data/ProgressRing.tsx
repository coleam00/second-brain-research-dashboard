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
        return 'text-emerald-400';
      case 'warning':
        return 'text-amber-400';
      case 'danger':
        return 'text-red-400';
      default:
        return 'text-blue-400';
    }
  };

  return (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: size, height: size }}>
        <svg
          className="transform -rotate-90 drop-shadow-lg"
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
            className="text-secondary"
          />
          {/* Progress circle */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="none"
            stroke="url(#blueGradient)"
            strokeWidth="8"
            className={getColorClass()}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            style={{ filter: 'drop-shadow(0 0 6px rgba(59, 130, 246, 0.5))' }}
          />
          <defs>
            <linearGradient id="blueGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#3b82f6" />
              <stop offset="100%" stopColor="#60a5fa" />
            </linearGradient>
          </defs>
        </svg>
        {/* Center text */}
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-xl font-bold text-white">{Math.round(percentage)}%</span>
        </div>
      </div>
      {label && (
        <span className="text-sm text-blue-300/70">{label}</span>
      )}
    </div>
  );
}

export default ProgressRing;
