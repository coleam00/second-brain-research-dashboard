/**
 * TimelineEvent Component
 *
 * Displays a single event in a timeline with timestamp,
 * title, description, and optional category/status badges.
 */

import React from 'react';
import { Badge } from "@/components/ui/badge";

export interface TimelineEventProps {
  /** Event timestamp in ISO format or Date object */
  timestamp: string | Date;

  /** Event title */
  title: string;

  /** Detailed description of the event */
  description: string;

  /** Optional category/type of event */
  category?: string;

  /** Optional status (e.g., "completed", "in-progress") */
  status?: string;
}

/**
 * TimelineEvent Component
 *
 * A component for displaying timeline entries with a vertical
 * line connector and timestamp marker.
 */
export function TimelineEvent({
  timestamp,
  title,
  description,
  category,
  status,
}: TimelineEventProps): React.ReactElement {
  const formatTimestamp = (ts: string | Date): string => {
    try {
      return new Date(ts).toLocaleString();
    } catch {
      return String(ts);
    }
  };

  return (
    <div className="flex gap-4 pb-4 border-l-2 border-blue-500/30 pl-4 relative group">
      {/* Timeline marker dot */}
      <div
        className="absolute -left-2 top-0 w-4 h-4 rounded-full bg-blue-500 border-4 border-background shadow-lg shadow-blue-500/50 group-hover:shadow-blue-400/70 transition-shadow duration-300"
        aria-hidden="true"
      />

      <div className="flex-1 bg-gradient-to-br from-card to-secondary/30 border border-blue-500/20 rounded-lg p-3 hover:border-blue-400/40 transition-all duration-300">
        <div className="flex items-center gap-2 mb-1 flex-wrap">
          <span className="text-sm font-semibold text-white">{title}</span>
          {category && (
            <Badge variant="outline" className="text-xs bg-blue-500/20 text-blue-300 border-blue-400/50">
              {category}
            </Badge>
          )}
          {status && (
            <Badge variant="outline" className="text-xs bg-blue-600/20 text-blue-200 border-blue-500/50">
              {status}
            </Badge>
          )}
        </div>

        <div className="text-xs text-blue-300/70 mb-1">
          {formatTimestamp(timestamp)}
        </div>

        <p className="text-sm text-blue-100/70">{description}</p>
      </div>
    </div>
  );
}

export default TimelineEvent;
