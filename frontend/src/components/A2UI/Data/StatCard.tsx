/**
 * StatCard Component
 *
 * Displays a single statistic with label, value, optional unit and trend indicator.
 * Supports dark theme and customizable colors.
 */

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader } from "@/components/ui/card";

export interface StatCardProps {
  /** Label/title for the statistic (accepts both 'label' and 'title' from backend) */
  label?: string;
  title?: string;

  /** The statistic value (number or string) */
  value: string | number;

  /** Optional unit text (e.g., "ms", "%", "users") */
  unit?: string;

  /** Optional trend indicator (e.g., "+12%", "-5%") */
  trend?: string;

  /** Optional change value from backend (will be formatted into trend) */
  change?: number;

  /** Optional change type from backend (positive/negative/neutral) */
  changeType?: string;

  /** Optional icon/emoji */
  icon?: string;

  /** Optional color theme (e.g., "green", "blue", "red") */
  color?: string;

  /** Optional background color class */
  backgroundColor?: string;

  /** Optional highlight flag from backend */
  highlight?: boolean;
}

/**
 * StatCard Component
 *
 * A card component for displaying key statistics and metrics
 * with optional trend indicators and customizable styling.
 */
export function StatCard({
  label,
  title,
  value,
  unit,
  trend,
  change,
  changeType,
  icon,
  color,
  backgroundColor,
  highlight,
}: StatCardProps): React.ReactElement {
  // Support both 'label' and 'title' prop names (backend sends 'title')
  const displayLabel = label || title || 'Metric';

  // Format trend from change/changeType if trend not provided directly
  const computedTrend = trend || (change !== undefined && change !== null
    ? `${change >= 0 ? '+' : ''}${change}${unit === '%' ? '' : '%'}`
    : undefined);

  const getTrendColor = () => {
    // Check explicit trend string first
    if (computedTrend) {
      if (computedTrend.startsWith('+')) return 'text-emerald-400';
      if (computedTrend.startsWith('-')) return 'text-red-400';
    }
    // Fallback to changeType from backend
    if (changeType === 'positive') return 'text-emerald-400';
    if (changeType === 'negative') return 'text-red-400';
    return 'text-muted-foreground';
  };

  return (
    <Card className={`${color ? `border-${color}-500/50` : 'border-blue-500/20'} ${backgroundColor || 'bg-gradient-to-br from-card to-secondary/30'} ${highlight ? 'ring-2 ring-blue-500/50' : ''} group cursor-default hover:border-blue-500/40`}>
      <CardHeader className="pb-2">
        <div className="flex justify-between items-start">
          <CardDescription className="text-blue-300/80">{displayLabel}</CardDescription>
          {icon && <span className="text-2xl transition-transform duration-200 group-hover:scale-110">{icon}</span>}
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent">
          {value}
          {unit && <span className="text-lg text-blue-300/60 ml-1">{unit}</span>}
        </div>
        {computedTrend && (
          <p className={`text-sm mt-1 font-medium ${getTrendColor()}`}>
            {computedTrend}
          </p>
        )}
      </CardContent>
    </Card>
  );
}

export default StatCard;
