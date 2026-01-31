/**
 * CalloutCard Component
 *
 * Displays informational callouts with type-specific styling and colors.
 * Supports tip, warning, info, and danger variants with appropriate visual indicators.
 */

import React from 'react';
import { Card, CardContent } from "@/components/ui/card";

export interface CalloutCardProps {
  /** Callout type determining color scheme and icon */
  type: 'tip' | 'warning' | 'info' | 'danger';

  /** Callout title */
  title: string;

  /** Callout content/message */
  content: string;

  /** Optional custom icon (overrides default type icon) */
  icon?: string;
}

/**
 * CalloutCard Component
 *
 * A card component for displaying informational callouts with color-coded
 * backgrounds and borders based on the callout type.
 */
export function CalloutCard({
  type,
  title,
  content,
  icon,
}: CalloutCardProps): React.ReactElement {
  const typeConfig = {
    tip: {
      bgColor: 'bg-blue-500/10 dark:bg-blue-500/20',
      borderColor: 'border-blue-500 dark:border-blue-500/50',
      icon: '💡',
      iconBg: 'bg-blue-500/20 dark:bg-blue-500/30',
      titleColor: 'text-blue-700 dark:text-blue-400',
    },
    warning: {
      bgColor: 'bg-yellow-500/10 dark:bg-yellow-500/20',
      borderColor: 'border-yellow-500 dark:border-yellow-500/50',
      icon: '⚠️',
      iconBg: 'bg-yellow-500/20 dark:bg-yellow-500/30',
      titleColor: 'text-yellow-700 dark:text-yellow-400',
    },
    info: {
      bgColor: 'bg-cyan-500/10 dark:bg-cyan-500/20',
      borderColor: 'border-cyan-500 dark:border-cyan-500/50',
      icon: 'ℹ️',
      iconBg: 'bg-cyan-500/20 dark:bg-cyan-500/30',
      titleColor: 'text-cyan-700 dark:text-cyan-400',
    },
    danger: {
      bgColor: 'bg-red-500/10 dark:bg-red-500/20',
      borderColor: 'border-red-500 dark:border-red-500/50',
      icon: '🚨',
      iconBg: 'bg-red-500/20 dark:bg-red-500/30',
      titleColor: 'text-red-700 dark:text-red-400',
    },
  };

  const config = typeConfig[type];
  const displayIcon = icon || config.icon;

  return (
    <Card className={`${config.bgColor} ${config.borderColor}`}>
      <CardContent className="pt-6">
        <div className="flex items-start gap-3">
          <div className={`flex items-center justify-center w-8 h-8 rounded-full ${config.iconBg} shrink-0`}>
            <span className="text-lg">{displayIcon}</span>
          </div>
          <div className="flex-1 space-y-1">
            <div className={`font-semibold ${config.titleColor}`}>{title}</div>
            <p className="text-sm dark:text-slate-300">{content}</p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default CalloutCard;
