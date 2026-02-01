/**
 * HeadlineCard Component
 *
 * Displays a news headline with title, summary, source, date, and optional image.
 * Supports sentiment indicators (positive, negative, neutral).
 */

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export interface HeadlineCardProps {
  /** Main headline title */
  title: string;

  /** Brief summary or description of the article */
  summary?: string;

  /** News source (e.g., "TechCrunch", "Reuters") */
  source?: string;

  /** Publication date in ISO format or Date object (accepts both snake_case and camelCase) */
  published_at?: string | Date;
  publishedAt?: string | Date;

  /** Sentiment of the article (positive, negative, neutral) */
  sentiment?: 'positive' | 'negative' | 'neutral';

  /** Optional image URL for the headline (accepts both snake_case and camelCase) */
  image_url?: string;
  imageUrl?: string;
}

/**
 * HeadlineCard Component
 *
 * A card component for displaying news headlines with optional image,
 * sentiment indicator, source, and publication date.
 */
export function HeadlineCard({
  title,
  summary,
  source,
  published_at,
  publishedAt,
  sentiment,
  image_url,
  imageUrl,
}: HeadlineCardProps): React.ReactElement {
  // Support both snake_case and camelCase (backend sends camelCase)
  const displayImageUrl = image_url || imageUrl;
  const displayPublishedAt = published_at || publishedAt;

  const getBorderColor = () => {
    if (sentiment === 'positive') return 'border-blue-400/40';
    if (sentiment === 'negative') return 'border-blue-500/30';
    return 'border-blue-500/20';
  };

  const getSentimentBadgeClasses = () => {
    if (sentiment === 'positive') return 'bg-blue-500/20 text-blue-300 border-blue-400/50 hover:bg-blue-500/30';
    if (sentiment === 'negative') return 'bg-blue-600/20 text-blue-200 border-blue-500/50 hover:bg-blue-600/30';
    return 'bg-blue-500/10 text-blue-400 border-blue-500/30';
  };

  const formatDate = (date: string | Date | undefined): string => {
    if (!date) return '';
    try {
      return new Date(date).toLocaleDateString();
    } catch {
      return String(date);
    }
  };

  return (
    <Card className={`${getBorderColor()} bg-gradient-to-br from-card to-secondary/30 group cursor-pointer hover:border-blue-400/60 transition-all duration-300 hover:shadow-lg hover:shadow-blue-500/10`}>
      {displayImageUrl && (
        <div className="overflow-hidden rounded-t-lg">
          <img
            src={displayImageUrl}
            alt={title}
            className="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105"
          />
        </div>
      )}
      <CardHeader>
        <div className="flex justify-between items-start gap-2">
          <CardTitle className="text-lg text-white group-hover:text-blue-300 transition-colors duration-200">{title}</CardTitle>
          {sentiment && sentiment !== 'neutral' && (
            <Badge variant="outline" className={`shrink-0 ${getSentimentBadgeClasses()}`}>
              {sentiment}
            </Badge>
          )}
        </div>
        {(source || displayPublishedAt) && (
          <CardDescription className="text-blue-300/80">
            {source}{source && displayPublishedAt ? ' • ' : ''}{formatDate(displayPublishedAt)}
          </CardDescription>
        )}
      </CardHeader>
      {summary && (
        <CardContent>
          <p className="text-sm text-blue-100/70">{summary}</p>
        </CardContent>
      )}
    </Card>
  );
}

export default HeadlineCard;
