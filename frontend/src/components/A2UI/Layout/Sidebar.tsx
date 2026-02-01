/**
 * Sidebar Component
 *
 * Two-column layout with sticky sidebar.
 * Responsive layout that stacks sidebar on mobile.
 */

import React from 'react';
import { cn } from "@/lib/utils";

export interface SidebarProps {
  /** Sidebar content */
  sidebar: React.ReactNode;

  /** Main content area */
  content: React.ReactNode;

  /** Sidebar width preset */
  sidebarWidth?: 'sm' | 'md' | 'lg';

  /** Position sidebar on left or right */
  position?: 'left' | 'right';

  /** Additional CSS classes */
  className?: string;
}

/**
 * Sidebar Component
 *
 * Two-column layout with sticky sidebar.
 * Automatically stacks on mobile for responsive behavior.
 */
export function Sidebar({
  sidebar,
  content,
  sidebarWidth = 'md',
  position = 'left',
  className,
}: SidebarProps): React.ReactElement {
  const widthClasses = {
    sm: 'md:w-48',
    md: 'md:w-64',
    lg: 'md:w-80',
  };

  return (
    <div
      className={cn(
        'flex flex-col md:flex-row gap-6',
        position === 'right' && 'md:flex-row-reverse',
        className
      )}
    >
      {/* Sidebar */}
      <aside
        className={cn(
          'w-full',
          widthClasses[sidebarWidth],
          'md:sticky md:top-4 md:self-start md:max-h-[calc(100vh-2rem)] md:overflow-y-auto'
        )}
      >
        <div className="p-4 bg-gradient-to-br from-slate-900/80 to-blue-950/50 rounded-lg border border-blue-500/20 backdrop-blur-sm">
          {sidebar}
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 min-w-0">
        {content}
      </main>
    </div>
  );
}

export default Sidebar;
