/**
 * StatCard Component
 *
 * Displays a single statistic with label, value, optional unit and trend indicator.
 * Supports dark theme and customizable colors.
 */

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader } from "@/components/ui/card";

export interface StatCardProps {
  /** Label/title for the statistic */
  label: string;

  /** The statistic value (number or string) */
  value: string | number;

  /** Optional unit text (e.g., "ms", "%", "users") */
  unit?: string;

  /** Optional trend indicator (e.g., "+12%", "-5%") */
  trend?: string;

  /** Optional icon/emoji */
  icon?: string;

  /** Optional color theme (e.g., "green", "blue", "red") */
  color?: string;

  /** Optional background color class */
  backgroundColor?: string;
}

/**
 * StatCard Component
 *
 * A card component for displaying key statistics and metrics
 * with optional trend indicators and customizable styling.
 */
export function StatCard({
  label,
  value,
  unit,
  trend,
  icon,
  color,
  backgroundColor,
}: StatCardProps): React.ReactElement {
  const getTrendColor = () => {
    if (!trend) return '';
    if (trend.startsWith('+')) return 'text-green-500';
    if (trend.startsWith('-')) return 'text-red-500';
    return 'text-muted-foreground';
  };

  return (
    <Card className={`${color ? `border-${color}-500` : ''} ${backgroundColor || ''} group cursor-default`}>
      <CardHeader className="pb-2">
        <div className="flex justify-between items-start">
          <CardDescription>{label}</CardDescription>
          {icon && <span className="text-2xl transition-transform duration-200 group-hover:scale-110">{icon}</span>}
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold">
          {value}
          {unit && <span className="text-lg text-muted-foreground ml-1">{unit}</span>}
        </div>
        {trend && (
          <p className={`text-sm mt-1 ${getTrendColor()}`}>
            {trend}
          </p>
        )}
      </CardContent>
    </Card>
  );
}

export default StatCard;
