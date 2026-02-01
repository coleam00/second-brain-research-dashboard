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
    <Card className="overflow-hidden bg-gradient-to-br from-card to-secondary/30 border-blue-500/20">
      {thumbnail_url && (
        <div className="relative group">
          <img
            src={thumbnail_url}
            alt={title}
            className="w-full h-48 object-cover"
            loading="lazy"
          />
          {/* Blue play button overlay */}
          <div className="absolute inset-0 bg-blue-950/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
            <div className="w-16 h-16 rounded-full bg-blue-500 flex items-center justify-center shadow-lg shadow-blue-500/50">
              <svg className="w-8 h-8 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z" />
              </svg>
            </div>
          </div>
          {duration && (
            <Badge className="absolute bottom-2 right-2 bg-blue-600 hover:bg-blue-600 text-white border-blue-400/30">
              {duration}
            </Badge>
          )}
        </div>
      )}
      <CardHeader>
        <CardTitle className="text-base line-clamp-2 text-white">{title}</CardTitle>
        <CardDescription className="text-blue-300">
          {host}
          {episode_number && ` • Episode ${episode_number}`}
          {published_at && ` • ${formatDate(published_at)}`}
        </CardDescription>
      </CardHeader>
      {(description || categories) && (
        <CardContent className="space-y-3">
          {description && (
            <p className="text-sm text-blue-200/80 line-clamp-3">{description}</p>
          )}
          {categories && categories.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {categories.map((category, idx) => (
                <Badge key={idx} className="text-xs bg-blue-600/50 hover:bg-blue-600/70 text-blue-100 border-blue-400/30">
                  {category}
                </Badge>
              ))}
            </div>
          )}
        </CardContent>
      )}
      {url && (
        <CardFooter>
          <Button asChild className="w-full bg-blue-600 hover:bg-blue-700 text-white shadow-md shadow-blue-500/20">
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
