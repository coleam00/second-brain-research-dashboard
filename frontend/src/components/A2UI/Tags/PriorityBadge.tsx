/**
 * PriorityBadge Component
 *
 * Displays priority level with blue scale color-coding and optional icons.
 * Supports low, medium, high, and critical priority levels.
 */

import React from 'react';
import { Badge } from "@/components/ui/badge";
import { ArrowUp, ArrowDown, Minus, AlertTriangle } from 'lucide-react';

export type PriorityLevel = 'low' | 'medium' | 'high' | 'critical';

/** Priority configuration */
interface PriorityConfig {
  label: string;
  color: string;
  icon: React.ReactNode;
}

const PRIORITY_CONFIGS: Record<PriorityLevel, PriorityConfig> = {
  low: {
    label: 'Low',
    color: 'bg-blue-900/30 text-blue-300 border-blue-400/20',
    icon: <ArrowDown className="w-3.5 h-3.5" />,
  },
  medium: {
    label: 'Medium',
    color: 'bg-blue-900/50 text-blue-200 border-blue-500/30',
    icon: <Minus className="w-3.5 h-3.5" />,
  },
  high: {
    label: 'High',
    color: 'bg-blue-950/70 text-blue-100 border-blue-500/50',
    icon: <ArrowUp className="w-3.5 h-3.5" />,
  },
  critical: {
    label: 'Critical',
    color: 'bg-blue-950/80 text-white border-blue-400/60',
    icon: <AlertTriangle className="w-3.5 h-3.5" />,
  },
};

export interface PriorityBadgeProps {
  /** Priority level */
  priority: PriorityLevel;

  /** Show icon representation */
  showIcon?: boolean;

  /** Show text label */
  showLabel?: boolean;

  /** Size variant */
  size?: 'sm' | 'md' | 'lg';
}

/**
 * PriorityBadge Component
 *
 * A badge component for displaying priority levels with blue scale color-coding and optional icons.
 */
export function PriorityBadge({
  priority,
  showIcon = true,
  showLabel = true,
  size = 'md',
}: PriorityBadgeProps): React.ReactElement {
  const config = PRIORITY_CONFIGS[priority];

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
      {showIcon && (
        <span className="flex-shrink-0">
          {config.icon}
        </span>
      )}
      {showLabel && <span>{config.label}</span>}
    </Badge>
  );
}

export default PriorityBadge;
