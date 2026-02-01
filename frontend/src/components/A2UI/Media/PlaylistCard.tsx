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
    <Card className="overflow-hidden bg-gradient-to-br from-card to-secondary/30 border-blue-500/20 hover:border-blue-500/40 transition-colors">
      {thumbnail_url && (
        <div className="relative group">
          <img
            src={thumbnail_url}
            alt={title}
            className="w-full h-40 object-cover"
            loading="lazy"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-blue-950/80 to-transparent" />
          {/* Blue play icon overlay on hover */}
          <div className="absolute inset-0 bg-blue-600/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
            <div className="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center shadow-lg shadow-blue-500/50">
              <svg className="w-6 h-6 text-white ml-0.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z" />
              </svg>
            </div>
          </div>
          {item_count !== undefined && (
            <Badge className="absolute top-2 right-2 bg-blue-600 hover:bg-blue-600 text-white border-blue-400/30">
              {item_count} {item_count === 1 ? 'item' : 'items'}
            </Badge>
          )}
          {total_duration && (
            <Badge className="absolute bottom-2 left-2 bg-blue-600 hover:bg-blue-600 text-white border-blue-400/30">
              {total_duration}
            </Badge>
          )}
        </div>
      )}
      <CardHeader>
        <CardTitle className="text-base line-clamp-2 text-white">{title}</CardTitle>
        <CardDescription className="text-blue-300">
          {platform && <span>{platform}</span>}
          {platform && creator && ' • '}
          {creator && <span>{creator}</span>}
        </CardDescription>
      </CardHeader>
      {description && (
        <CardContent>
          <p className="text-sm text-blue-200/80 line-clamp-2">{description}</p>
        </CardContent>
      )}
      {url && (
        <CardFooter>
          <Button asChild variant="outline" className="w-full border-blue-500/30 text-blue-300 hover:bg-blue-500/10 hover:text-blue-200">
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
