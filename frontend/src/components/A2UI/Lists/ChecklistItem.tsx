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
      className={`flex items-center gap-3 p-3 rounded-lg hover:bg-muted/50 transition-all duration-200 hover:shadow-sm ${
        disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:scale-[1.01]'
      }`}
      onClick={handleClick}
    >
      <div
        className={`w-5 h-5 rounded border-2 flex items-center justify-center shrink-0 transition-all duration-200 ${
          checked
            ? 'bg-primary border-primary scale-100'
            : 'border-muted-foreground hover:border-primary/50'
        }`}
      >
        {checked && (
          <span className="text-primary-foreground text-xs font-bold">✓</span>
        )}
      </div>
      <span
        className={`flex-1 transition-all duration-200 ${
          checked ? 'line-through text-muted-foreground' : ''
        }`}
      >
        {label}
      </span>
      {category && (
        <Badge variant="outline" className="text-xs shrink-0">
          {category}
        </Badge>
      )}
    </div>
  );
}

export default ChecklistItem;
