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
    <div className="flex gap-4 pb-4 border-l-2 border-muted pl-4 relative">
      {/* Timeline marker dot */}
      <div
        className="absolute -left-2 top-0 w-4 h-4 rounded-full bg-primary border-4 border-background"
        aria-hidden="true"
      />

      <div className="flex-1">
        <div className="flex items-center gap-2 mb-1 flex-wrap">
          <span className="text-sm font-semibold">{title}</span>
          {category && (
            <Badge variant="outline" className="text-xs">
              {category}
            </Badge>
          )}
          {status && (
            <Badge variant="secondary" className="text-xs">
              {status}
            </Badge>
          )}
        </div>

        <div className="text-xs text-muted-foreground mb-1">
          {formatTimestamp(timestamp)}
        </div>

        <p className="text-sm text-muted-foreground">{description}</p>
      </div>
    </div>
  );
}

export default TimelineEvent;
