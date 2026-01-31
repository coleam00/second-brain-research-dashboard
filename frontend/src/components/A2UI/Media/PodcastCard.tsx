/**
 * PodcastCard Component
 *
 * Displays a podcast episode with thumbnail, host, episode number,
 * duration, and description.
 */

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export interface PodcastCardProps {
  /** Episode title */
  title: string;

  /** Episode description */
  description?: string;

  /** Podcast host or show name */
  host: string;

  /** Episode number */
  episode_number?: number | string;

  /** Episode duration (e.g., "45:30", "1h 15m") */
  duration?: string;

  /** Podcast thumbnail or cover art URL */
  thumbnail_url?: string;

  /** Episode URL or audio link */
  url?: string;

  /** Publication date */
  published_at?: string | Date;

  /** Categories or tags */
  categories?: string[];
}

/**
 * PodcastCard Component
 *
 * A card component for displaying podcast episodes with metadata,
 * cover art, and playback link.
 */
export function PodcastCard({
  title,
  description,
  host,
  episode_number,
  duration,
  thumbnail_url,
  url,
  published_at,
  categories,
}: PodcastCardProps): React.ReactElement {
  const formatDate = (date: string | Date): string => {
    try {
      return new Date(date).toLocaleDateString();
    } catch {
      return String(date);
    }
  };

  return (
    <Card className="overflow-hidden">
      {thumbnail_url && (
        <div className="relative">
          <img
            src={thumbnail_url}
            alt={title}
            className="w-full h-48 object-cover"
            loading="lazy"
          />
          {duration && (
            <Badge className="absolute bottom-2 right-2 bg-black/70 hover:bg-black/70" variant="secondary">
              {duration}
            </Badge>
          )}
        </div>
      )}
      <CardHeader>
        <CardTitle className="text-base line-clamp-2">{title}</CardTitle>
        <CardDescription>
          {host}
          {episode_number && ` • Episode ${episode_number}`}
          {published_at && ` • ${formatDate(published_at)}`}
        </CardDescription>
      </CardHeader>
      {(description || categories) && (
        <CardContent className="space-y-3">
          {description && (
            <p className="text-sm text-muted-foreground line-clamp-3">{description}</p>
          )}
          {categories && categories.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {categories.map((category, idx) => (
                <Badge key={idx} variant="secondary" className="text-xs">
                  {category}
                </Badge>
              ))}
            </div>
          )}
        </CardContent>
      )}
      {url && (
        <CardFooter>
          <Button asChild className="w-full">
            <a href={url} target="_blank" rel="noopener noreferrer">
              Listen Now
            </a>
          </Button>
        </CardFooter>
      )}
    </Card>
  );
}

export default PodcastCard;
