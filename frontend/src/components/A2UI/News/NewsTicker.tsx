/**
 * NewsTicker Component
 *
 * Displays a scrolling ticker of news items with source badges.
 * Items scroll horizontally in a continuous loop.
 */

import React from 'react';
import { Badge } from "@/components/ui/badge";

export interface NewsTickerItem {
  /** News source */
  source: string;

  /** Headline text */
  headline: string;
}

export interface NewsTickerProps {
  /** Array of news items to display in the ticker */
  items: NewsTickerItem[];
}

/**
 * NewsTicker Component
 *
 * A horizontally scrolling news ticker that displays multiple
 * news items with their sources.
 *
 * Note: Animation is CSS-based. For production use, consider adding
 * duplicate items for seamless infinite scrolling.
 */
export function NewsTicker({ items }: NewsTickerProps): React.ReactElement {
  if (!items || items.length === 0) {
    return (
      <div className="overflow-hidden bg-gradient-to-br from-card to-secondary/30 border border-blue-500/20 rounded-lg p-3">
        <div className="text-sm text-blue-300/70 text-center">
          No news items available
        </div>
      </div>
    );
  }

  return (
    <div className="overflow-hidden bg-gradient-to-br from-card to-secondary/30 border border-blue-500/20 rounded-lg p-3 hover:border-blue-400/40 transition-all duration-300">
      <div className="flex gap-6 animate-scroll whitespace-nowrap">
        {items.map((item, idx) => (
          <span key={idx} className="inline-flex items-center gap-2 animate-pulse">
            <Badge variant="outline" className="bg-blue-500/20 text-blue-300 border-blue-400/50 hover:bg-blue-500/30">
              {item.source}
            </Badge>
            <span className="text-sm text-blue-100">{item.headline}</span>
          </span>
        ))}
      </div>
    </div>
  );
}

export default NewsTicker;
