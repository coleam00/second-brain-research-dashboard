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
  source: string;

  /** Publication date in ISO format or Date object */
  published_at: string | Date;

  /** Sentiment of the article (positive, negative, neutral) */
  sentiment?: 'positive' | 'negative' | 'neutral';

  /** Optional image URL for the headline */
  image_url?: string;
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
  sentiment,
  image_url,
}: HeadlineCardProps): React.ReactElement {
  const getBorderColor = () => {
    if (sentiment === 'positive') return 'border-green-500';
    if (sentiment === 'negative') return 'border-red-500';
    return '';
  };

  const getSentimentVariant = () => {
    if (sentiment === 'positive') return 'default' as const;
    if (sentiment === 'negative') return 'destructive' as const;
    return 'secondary' as const;
  };

  const formatDate = (date: string | Date): string => {
    try {
      return new Date(date).toLocaleDateString();
    } catch {
      return String(date);
    }
  };

  return (
    <Card className={`${getBorderColor()} group cursor-pointer`}>
      {image_url && (
        <div className="overflow-hidden rounded-t-lg">
          <img
            src={image_url}
            alt={title}
            className="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105"
          />
        </div>
      )}
      <CardHeader>
        <div className="flex justify-between items-start gap-2">
          <CardTitle className="text-lg group-hover:text-primary transition-colors duration-200">{title}</CardTitle>
          {sentiment && sentiment !== 'neutral' && (
            <Badge variant={getSentimentVariant()} className="shrink-0">
              {sentiment}
            </Badge>
          )}
        </div>
        <CardDescription>
          {source} • {formatDate(published_at)}
        </CardDescription>
      </CardHeader>
      {summary && (
        <CardContent>
          <p className="text-sm text-muted-foreground">{summary}</p>
        </CardContent>
      )}
    </Card>
  );
}

export default HeadlineCard;
