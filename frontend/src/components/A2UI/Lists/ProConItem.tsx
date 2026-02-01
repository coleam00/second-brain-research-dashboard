/**
 * ProConItem Component
 *
 * Displays a pro or con item with icon, text, and optional weight/importance.
 * Shows green checkmark for pros, red X for cons.
 */

import React from 'react';
import { Badge } from "@/components/ui/badge";

export interface ProConItemProps {
  /** Type of item: 'pro' (positive) or 'con' (negative) */
  type: 'pro' | 'con';

  /** Item text/description */
  label: string;

  /** Optional description for more details */
  description?: string;

  /** Optional weight/importance indicator */
  weight?: string | number;
}

/**
 * ProConItem Component
 *
 * A component for displaying pros and cons with color-coded icons.
 * Green checkmark for pros, red X for cons. Perfect for decision matrices,
 * comparisons, and analysis.
 */
export function ProConItem({
  type,
  label,
  description,
  weight,
}: ProConItemProps): React.ReactElement {
  const isPro = type === 'pro';

  const bgColor = isPro ? 'bg-gradient-to-br from-emerald-500/20 to-blue-500/10' : 'bg-gradient-to-br from-red-500/20 to-secondary/30';
  const borderColor = isPro ? 'border-emerald-500/30' : 'border-red-500/30';
  const textColor = isPro ? 'text-emerald-400' : 'text-red-400';
  const icon = isPro ? '✓' : '✗';

  return (
    <div className={`flex items-start gap-2 p-3 rounded-lg ${bgColor} border ${borderColor} hover:border-opacity-60 transition-all duration-200`}>
      <span className={`text-lg ${textColor} shrink-0 mt-0.5 font-bold`}>
        {icon}
      </span>
      <div className="flex-1 min-w-0">
        <span className="text-sm block text-white font-medium">{label}</span>
        {description && (
          <p className="text-xs text-blue-200 mt-1">{description}</p>
        )}
      </div>
      {weight !== undefined && weight !== null && (
        <Badge variant="secondary" className="shrink-0 bg-blue-500/20 text-blue-300 border-blue-500/30">
          {weight}
        </Badge>
      )}
    </div>
  );
}

export default ProConItem;
