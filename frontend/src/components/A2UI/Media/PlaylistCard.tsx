/**
 * PlaylistCard Component
 *
 * Displays a playlist or collection of media items with thumbnail,
 * item count, platform, and description.
 */

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export interface PlaylistCardProps {
  /** Playlist title */
  title: string;

  /** Playlist description */
  description?: string;

  /** Number of items in playlist */
  item_count?: number;

  /** Playlist thumbnail URL */
  thumbnail_url?: string;

  /** Platform name (e.g., "YouTube", "Spotify") */
  platform?: string;

  /** Playlist URL */
  url?: string;

  /** Creator or channel name */
  creator?: string;

  /** Total duration (e.g., "2h 30m") */
  total_duration?: string;
}

/**
 * PlaylistCard Component
 *
 * A card component for displaying playlists with thumbnail,
 * item count badge, and metadata.
 */
export function PlaylistCard({
  title,
  description,
  item_count,
  thumbnail_url,
  platform,
  url,
  creator,
  total_duration,
}: PlaylistCardProps): React.ReactElement {
  return (
    <Card className="overflow-hidden">
      {thumbnail_url && (
        <div className="relative">
          <img
            src={thumbnail_url}
            alt={title}
            className="w-full h-40 object-cover"
            loading="lazy"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
          {item_count !== undefined && (
            <Badge className="absolute top-2 right-2 bg-black/70 hover:bg-black/70">
              {item_count} {item_count === 1 ? 'item' : 'items'}
            </Badge>
          )}
          {total_duration && (
            <Badge className="absolute bottom-2 left-2 bg-black/70 hover:bg-black/70" variant="secondary">
              {total_duration}
            </Badge>
          )}
        </div>
      )}
      <CardHeader>
        <CardTitle className="text-base line-clamp-2">{title}</CardTitle>
        <CardDescription>
          {platform && <span>{platform}</span>}
          {platform && creator && ' • '}
          {creator && <span>{creator}</span>}
        </CardDescription>
      </CardHeader>
      {description && (
        <CardContent>
          <p className="text-sm text-muted-foreground line-clamp-2">{description}</p>
        </CardContent>
      )}
      {url && (
        <CardFooter>
          <Button asChild variant="outline" className="w-full">
            <a href={url} target="_blank" rel="noopener noreferrer">
              Open Playlist
            </a>
          </Button>
        </CardFooter>
      )}
    </Card>
  );
}

export default PlaylistCard;
