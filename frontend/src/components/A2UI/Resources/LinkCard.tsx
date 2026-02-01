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
      className="bg-gradient-to-br from-card to-secondary/30 border-blue-500/20 hover:border-blue-400/40 transition-all cursor-pointer group"
      onClick={handleClick}
    >
      <CardHeader>
        <div className="flex items-start gap-3">
          {favicon ? (
            <img
              src={favicon}
              alt=""
              className="w-6 h-6 rounded shrink-0"
              onError={(e) => {
                // Hide image if it fails to load
                (e.target as HTMLImageElement).style.display = 'none';
              }}
            />
          ) : (
            <span className="text-blue-400 text-xl shrink-0">🔗</span>
          )}
          <div className="flex-1 min-w-0">
            <CardTitle className="text-base line-clamp-2 text-white group-hover:text-blue-300 transition-colors">{title}</CardTitle>
            {domain && <CardDescription className="mt-1 text-blue-300/80">{domain}</CardDescription>}
          </div>
        </div>
      </CardHeader>
      {description && (
        <CardContent>
          <p className="text-sm text-blue-200/70 line-clamp-2">{description}</p>
        </CardContent>
      )}
    </Card>
  );
}

export default LinkCard;
