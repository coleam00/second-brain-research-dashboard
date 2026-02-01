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
    <Card className="overflow-hidden bg-gradient-to-br from-card to-secondary/30 border-blue-500/20">
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
        <div className="relative group">
          {thumbnail_url && (
            <img
              src={thumbnail_url}
              alt={title}
              className="w-full h-48 object-cover"
              loading="lazy"
            />
          )}
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
        {platform && <CardDescription className="text-blue-300">{platform}</CardDescription>}
      </CardHeader>
      {description && (
        <CardContent>
          <p className="text-sm text-blue-200/80 line-clamp-2">{description}</p>
        </CardContent>
      )}
      {url && !showEmbed && (
        <CardFooter>
          <Button asChild variant="outline" className="w-full border-blue-500/30 text-blue-300 hover:bg-blue-500/10 hover:text-blue-200">
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
