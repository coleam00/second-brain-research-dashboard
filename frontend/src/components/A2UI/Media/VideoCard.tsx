/**
 * VideoCard Component
 *
 * Displays a video with thumbnail, title, description, duration, and platform.
 * Supports YouTube embeds and external video links.
 */

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export interface VideoCardProps {
  /** Video title */
  title: string;

  /** Video description or summary */
  description?: string;

  /** Video thumbnail URL */
  thumbnail_url?: string;

  /** Video duration (e.g., "10:45", "1h 30m") */
  duration?: string;

  /** Platform name (e.g., "YouTube", "Vimeo") */
  platform?: string;

  /** Video URL or YouTube video ID */
  url?: string;

  /** YouTube video ID for embedding */
  youtube_id?: string;

  /** Whether to show embedded player instead of thumbnail */
  embed?: boolean;
}

/**
 * VideoCard Component
 *
 * A card component for displaying video content with thumbnail,
 * metadata, and optional YouTube embedding.
 */
export function VideoCard({
  title,
  description,
  thumbnail_url,
  duration,
  platform,
  url,
  youtube_id,
  embed = false,
}: VideoCardProps): React.ReactElement {
  // Extract YouTube ID from URL if not provided
  const extractYouTubeId = (videoUrl: string): string | null => {
    const patterns = [
      /(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\s]+)/,
      /youtube\.com\/embed\/([^&\s]+)/,
    ];

    for (const pattern of patterns) {
      const match = videoUrl.match(pattern);
      if (match) return match[1];
    }

    return null;
  };

  const videoId = youtube_id || (url ? extractYouTubeId(url) : null);
  const showEmbed = embed && videoId;

  return (
    <Card className="overflow-hidden">
      {showEmbed ? (
        <div className="relative w-full pt-[56.25%]">
          <iframe
            className="absolute top-0 left-0 w-full h-full"
            src={`https://www.youtube.com/embed/${videoId}`}
            title={title}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
          />
        </div>
      ) : (
        <div className="relative">
          {thumbnail_url && (
            <img
              src={thumbnail_url}
              alt={title}
              className="w-full h-48 object-cover"
              loading="lazy"
            />
          )}
          {duration && (
            <Badge className="absolute bottom-2 right-2 bg-black/70 hover:bg-black/70" variant="secondary">
              {duration}
            </Badge>
          )}
        </div>
      )}
      <CardHeader>
        <CardTitle className="text-base line-clamp-2">{title}</CardTitle>
        {platform && <CardDescription>{platform}</CardDescription>}
      </CardHeader>
      {description && (
        <CardContent>
          <p className="text-sm text-muted-foreground line-clamp-2">{description}</p>
        </CardContent>
      )}
      {url && !showEmbed && (
        <CardFooter>
          <Button asChild variant="outline" className="w-full">
            <a href={url} target="_blank" rel="noopener noreferrer">
              Watch Video
            </a>
          </Button>
        </CardFooter>
      )}
    </Card>
  );
}

export default VideoCard;
