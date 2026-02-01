/**
 * BulletPoint Component
 *
 * Displays a bullet point item with text, optional indentation levels,
 * and customizable icon. Supports hierarchical lists.
 */

import React from 'react';

export interface BulletPointProps {
  /** Bullet point text content */
  text: string;

  /** Indentation level (0, 1, 2, 3) for nested lists */
  level?: number;

  /** Custom icon/bullet character (default: '•') */
  icon?: string;

  /** Optional color for the bullet icon */
  color?: string;
}

/**
 * BulletPoint Component
 *
 * A flexible bullet point component supporting multiple indentation levels
 * and custom icons. Perfect for lists, hierarchical content, and structured notes.
 */
export function BulletPoint({
  text,
  level = 0,
  icon = '•',
  color,
}: BulletPointProps): React.ReactElement {
  const getIconColor = () => {
    if (color) return `text-${color}-500`;
    return 'text-blue-400';
  };

  const leftMargin = level * 1.5; // 1.5rem per level

  return (
    <div
      className="flex items-start gap-2 py-1"
      style={{ marginLeft: `${leftMargin}rem` }}
    >
      <span className={`mt-1 ${getIconColor()} shrink-0 font-bold`}>
        {icon}
      </span>
      <span className="text-sm flex-1 text-white leading-relaxed">{text}</span>
    </div>
  );
}

export default BulletPoint;
