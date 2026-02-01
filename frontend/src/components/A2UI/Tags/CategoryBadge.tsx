/**
 * CategoryBadge Component
 *
 * Displays a category with color-coded background and optional icon.
 * Supports predefined color schemes for common categories.
 */

import React from 'react';
import { Badge } from "@/components/ui/badge";
import { X } from 'lucide-react';

export type CategorySize = 'sm' | 'md' | 'lg';

/** Predefined category color schemes - Modern dark blue theme */
const CATEGORY_COLORS: Record<string, string> = {
  tech: 'bg-blue-950/60 text-blue-100 border-blue-500/40',
  science: 'bg-blue-900/50 text-blue-200 border-blue-400/30',
  business: 'bg-blue-900/60 text-blue-100 border-blue-500/30',
  health: 'bg-blue-950/50 text-blue-200 border-blue-400/40',
  education: 'bg-blue-900/50 text-blue-100 border-blue-500/30',
  entertainment: 'bg-blue-950/60 text-blue-200 border-blue-400/30',
  sports: 'bg-blue-900/60 text-blue-100 border-blue-500/40',
  politics: 'bg-blue-950/50 text-blue-200 border-blue-400/30',
  finance: 'bg-blue-900/50 text-blue-100 border-blue-500/30',
  lifestyle: 'bg-blue-950/60 text-blue-200 border-blue-400/40',
};

export interface CategoryBadgeProps {
  /** Category name */
  category: string;

  /** Custom color class (overrides predefined colors) */
  color?: string;

  /** Optional icon (emoji or component) */
  icon?: string | React.ReactNode;

  /** Badge size */
  size?: CategorySize;

  /** Show remove button */
  removable?: boolean;

  /** Callback when remove button is clicked */
  onRemove?: () => void;
}

/**
 * CategoryBadge Component
 *
 * A badge component for displaying categories with predefined or custom colors.
 * Supports icons and removable functionality.
 */
export function CategoryBadge({
  category,
  color,
  icon,
  size = 'md',
  removable = false,
  onRemove,
}: CategoryBadgeProps): React.ReactElement {
  // Get color from predefined schemes or use custom
  const categoryKey = category.toLowerCase();
  const badgeColor = color || CATEGORY_COLORS[categoryKey] || 'bg-blue-950/50 text-blue-200 border-blue-500/30';

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
        ${badgeColor}
        ${sizeClasses[size]}
        font-medium
        flex items-center gap-1.5
        w-fit
      `}
    >
      {icon && (
        <span className="flex-shrink-0">
          {typeof icon === 'string' ? icon : icon}
        </span>
      )}
      <span>{category}</span>
      {removable && (
        <button
          onClick={(e) => {
            e.stopPropagation();
            onRemove?.();
          }}
          className="ml-0.5 hover:bg-blue-400/20 rounded-full p-0.5 transition-colors"
          aria-label="Remove category"
        >
          <X className="w-3 h-3" />
        </button>
      )}
    </Badge>
  );
}

export default CategoryBadge;
