/**
 * StepCard Component
 *
 * Displays an instructional step with number, title, description, and status indicator.
 * Supports optional icons and status tracking (pending, active, complete).
 */

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export interface StepCardProps {
  /** Step number (1, 2, 3, etc.) */
  stepNumber: number;

  /** Step title */
  title: string;

  /** Step description/instructions */
  description: string;

  /** Optional icon or emoji */
  icon?: string;

  /** Step status (defaults to 'pending') */
  status?: 'pending' | 'active' | 'complete';
}

/**
 * StepCard Component
 *
 * A card component for displaying instructional steps with status indicators,
 * ideal for tutorials, guides, and multi-step processes.
 */
export function StepCard({
  stepNumber,
  title,
  description,
  icon,
  status = 'pending',
}: StepCardProps): React.ReactElement {
  const getStatusColor = () => {
    if (status === 'complete') return 'bg-green-500 dark:bg-green-600';
    if (status === 'active') return 'bg-blue-500 dark:bg-blue-600';
    return 'bg-gray-400 dark:bg-gray-600';
  };

  const getStatusBadge = () => {
    if (status === 'complete') return { variant: 'default' as const, text: 'Complete', color: 'bg-green-500/10 text-green-700 dark:bg-green-500/20 dark:text-green-400' };
    if (status === 'active') return { variant: 'default' as const, text: 'Active', color: 'bg-blue-500/10 text-blue-700 dark:bg-blue-500/20 dark:text-blue-400' };
    return { variant: 'secondary' as const, text: 'Pending', color: 'bg-gray-500/10 text-gray-700 dark:bg-gray-500/20 dark:text-gray-400' };
  };

  const statusBadge = getStatusBadge();

  return (
    <Card className={`dark:bg-slate-900/50 dark:border-slate-700 ${status === 'active' ? 'border-blue-500 dark:border-blue-500' : ''}`}>
      <CardHeader>
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-start gap-3 flex-1">
            <div className={`flex items-center justify-center w-10 h-10 rounded-full ${getStatusColor()} text-white font-bold shrink-0`}>
              {status === 'complete' ? '✓' : stepNumber}
            </div>
            <div className="flex-1">
              <CardTitle className="text-base flex items-center gap-2 dark:text-slate-100">
                {icon && <span>{icon}</span>}
                {title}
              </CardTitle>
            </div>
          </div>
          <Badge variant={statusBadge.variant} className={statusBadge.color}>
            {statusBadge.text}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground dark:text-slate-400 ml-[52px]">{description}</p>
      </CardContent>
    </Card>
  );
}

export default StepCard;
