/**
 * TableOfContents Component
 *
 * Displays a hierarchical outline with up to 4 levels of nesting.
 * Supports optional page numbers and anchor links.
 */

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export interface TOCItem {
  /** Item title/text */
  title: string;

  /** Nesting level (0-3) */
  level?: number;

  /** Optional anchor link */
  anchor?: string;

  /** Optional page number */
  page?: number;
}

export interface TableOfContentsProps {
  /** Array of table of contents items */
  items: TOCItem[];

  /** Optional title override */
  title?: string;

  /** Whether to show page numbers */
  show_page_numbers?: boolean;
}

/**
 * TableOfContents Component
 *
 * A hierarchical navigation component with support for
 * up to 4 levels of nesting, anchor links, and page numbers.
 */
export function TableOfContents({
  items,
  title = 'Table of Contents',
  show_page_numbers = false,
}: TableOfContentsProps): React.ReactElement {
  const getIndentation = (level: number = 0) => {
    // Limit to 4 levels (0-3)
    const safeLevel = Math.min(Math.max(level, 0), 3);
    return `${safeLevel * 1.5}rem`;
  };

  const getAnchor = (item: TOCItem): string => {
    if (item.anchor) {
      return item.anchor;
    }
    // Generate anchor from title
    return `#${item.title.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '')}`;
  };

  return (
    <Card className="bg-gradient-to-br from-card to-secondary/30 border-blue-500/20">
      <CardHeader>
        <CardTitle className="text-base text-blue-300">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <nav>
          <ul className="space-y-2">
            {items.map((item, idx) => (
              <li
                key={idx}
                style={{ marginLeft: getIndentation(item.level) }}
                className="flex items-start justify-between gap-2 group"
              >
                <a
                  href={getAnchor(item)}
                  className="text-sm text-blue-400 hover:text-blue-300 hover:underline flex-1 leading-relaxed transition-colors relative before:absolute before:left-0 before:top-1/2 before:-translate-y-1/2 before:w-0.5 before:h-0 group-hover:before:h-full before:bg-blue-400 before:transition-all before:-ml-2"
                >
                  {item.title}
                </a>
                {show_page_numbers && item.page !== undefined && (
                  <span className="text-xs text-blue-300 shrink-0 font-mono">
                    {item.page}
                  </span>
                )}
              </li>
            ))}
          </ul>
        </nav>
      </CardContent>
    </Card>
  );
}

export default TableOfContents;
