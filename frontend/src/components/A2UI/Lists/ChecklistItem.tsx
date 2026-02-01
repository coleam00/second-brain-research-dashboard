/**
 * ChecklistItem Component
 *
 * Displays a checkbox with label and optional category badge.
 * Supports checked/unchecked states with strike-through styling.
 */

import React from 'react';
import { Badge } from "@/components/ui/badge";

export interface ChecklistItemProps {
  /** Item label/text */
  label: string;

  /** Checked state */
  checked: boolean;

  /** Callback when checkbox is toggled */
  onChange?: (checked: boolean) => void;

  /** Whether the item is disabled */
  disabled?: boolean;

  /** Optional category badge */
  category?: string;
}

/**
 * ChecklistItem Component
 *
 * A checkbox list item with label, optional category badge, and strike-through
 * when checked. Perfect for task lists, todo items, and checklists.
 */
export function ChecklistItem({
  label,
  checked,
  onChange,
  disabled = false,
  category,
}: ChecklistItemProps): React.ReactElement {
  const handleClick = () => {
    if (!disabled && onChange) {
      onChange(!checked);
    }
  };

  return (
    <div
      className={`flex items-center gap-3 p-3 rounded-lg bg-secondary/30 border border-blue-500/20 hover:border-blue-500/40 transition-all duration-200 hover:shadow-sm ${
        disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:scale-[1.01]'
      }`}
      onClick={handleClick}
    >
      <div
        className={`w-5 h-5 rounded border-2 flex items-center justify-center shrink-0 transition-all duration-200 ${
          checked
            ? 'bg-blue-500 border-blue-500 scale-100 shadow-lg shadow-blue-500/30'
            : 'border-blue-400/50 hover:border-blue-400'
        }`}
      >
        {checked && (
          <span className="text-white text-xs font-bold">✓</span>
        )}
      </div>
      <span
        className={`flex-1 transition-all duration-200 ${
          checked ? 'line-through text-blue-200/60' : 'text-white'
        }`}
      >
        {label}
      </span>
      {category && (
        <Badge variant="outline" className="text-xs shrink-0 bg-blue-500/20 text-blue-300 border-blue-500/30">
          {category}
        </Badge>
      )}
    </div>
  );
}

export default ChecklistItem;
