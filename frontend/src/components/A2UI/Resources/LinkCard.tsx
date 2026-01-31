/**
 * LinkCard Component
 *
 * Displays a clickable link resource card with title, description, and optional favicon.
 * Perfect for bookmarks, references, and external resources.
 */

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export interface LinkCardProps {
  /** Link title */
  title: string;

  /** Link URL */
  url: string;

  /** Optional link description */
  description?: string;

  /** Optional favicon URL */
  favicon?: string;

  /** Optional domain name */
  domain?: string;
}

/**
 * LinkCard Component
 *
 * A clickable card for displaying link resources with optional favicon,
 * title, description, and domain. Opens links in a new tab.
 */
export function LinkCard({
  title,
  url,
  description,
  favicon,
  domain,
}: LinkCardProps): React.ReactElement {
  const handleClick = () => {
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  return (
    <Card
      className="hover:bg-muted/50 transition-colors cursor-pointer"
      onClick={handleClick}
    >
      <CardHeader>
        <div className="flex items-start gap-3">
          {favicon && (
            <img
              src={favicon}
              alt=""
              className="w-6 h-6 rounded shrink-0"
              onError={(e) => {
                // Hide image if it fails to load
                (e.target as HTMLImageElement).style.display = 'none';
              }}
            />
          )}
          <div className="flex-1 min-w-0">
            <CardTitle className="text-base line-clamp-2">{title}</CardTitle>
            {domain && <CardDescription className="mt-1">{domain}</CardDescription>}
          </div>
        </div>
      </CardHeader>
      {description && (
        <CardContent>
          <p className="text-sm text-muted-foreground line-clamp-2">{description}</p>
        </CardContent>
      )}
    </Card>
  );
}

export default LinkCard;
