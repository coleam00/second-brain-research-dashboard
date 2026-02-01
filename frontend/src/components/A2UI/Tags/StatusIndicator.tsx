/**
 * StatusIndicator Component
 *
 * Displays status with appropriate color-coding and optional icons.
 * Supports various status types with blue theme for active states.
 */

import React from 'react';
import { Badge } from "@/components/ui/badge";
import { Circle } from 'lucide-react';

export type StatusType = 'active' | 'inactive' | 'pending' | 'completed' | 'error' | 'warning';

/** Status configuration */
interface StatusConfig {
  label: string;
  color: string;
  dotColor: string;
}

const STATUS_CONFIGS: Record<StatusType, StatusConfig> = {
  active: {
    label: 'Active',
    color: 'bg-blue-950/60 text-blue-100 border-blue-500/40',
    dotColor: 'text-blue-400',
  },
  inactive: {
    label: 'Inactive',
    color: 'bg-slate-900/60 text-slate-300 border-slate-600/40',
    dotColor: 'text-slate-500',
  },
  pending: {
    label: 'Pending',
    color: 'bg-blue-900/50 text-blue-200 border-blue-400/30',
    dotColor: 'text-blue-300',
  },
  completed: {
    label: 'Completed',
    color: 'bg-emerald-950/60 text-emerald-200 border-emerald-500/40',
    dotColor: 'text-emerald-400',
  },
  error: {
    label: 'Error',
    color: 'bg-red-950/60 text-red-200 border-red-500/40',
    dotColor: 'text-red-400',
  },
  warning: {
    label: 'Warning',
    color: 'bg-amber-950/60 text-amber-200 border-amber-500/40',
    dotColor: 'text-amber-400',
  },
};

export interface StatusIndicatorProps {
  /** Status type */
  status: StatusType;

  /** Custom label (overrides default) */
  label?: string;

  /** Show pulsing animation for active status */
  pulse?: boolean;

  /** Show dot indicator */
  showDot?: boolean;

  /** Size variant */
  size?: 'sm' | 'md' | 'lg';
}

/**
 * StatusIndicator Component
 *
 * A badge component for displaying status with color-coding and optional animations.
 */
export function StatusIndicator({
  status,
  label,
  pulse = false,
  showDot = true,
  size = 'md',
}: StatusIndicatorProps): React.ReactElement {
  const config = STATUS_CONFIGS[status];
  const displayLabel = label || config.label;

  // Size classes
  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-sm px-2.5 py-1',
    lg: 'text-base px-3 py-1.5',
  };

  return (
    <Badge
      variant="outline"
      className={`
        ${config.color}
        ${sizeClasses[size]}
        font-medium
        flex items-center gap-1.5
        w-fit
      `}
    >
      {showDot && (
        <span className="relative flex-shrink-0">
          <Circle
            className={`
              w-2 h-2
              fill-current
              ${config.dotColor}
              ${pulse && status === 'active' ? 'animate-pulse' : ''}
            `}
          />
        </span>
      )}
      <span>{displayLabel}</span>
    </Badge>
  );
}

export default StatusIndicator;
