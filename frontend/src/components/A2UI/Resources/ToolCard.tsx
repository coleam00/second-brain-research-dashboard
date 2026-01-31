/**
 * ToolCard Component
 *
 * Displays a tool/software resource with name, description, rating, and optional logo.
 * Includes visual star rating representation (1-5 stars).
 */

import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export interface ToolCardProps {
  /** Tool name */
  name: string;

  /** Tool description */
  description: string;

  /** Star rating (1-5) */
  rating: number;

  /** Optional tool icon/logo URL */
  icon?: string;

  /** Optional tool website URL */
  url?: string;

  /** Optional category */
  category?: string;

  /** Optional pricing info */
  pricing?: string;
}

/**
 * ToolCard Component
 *
 * A card component for displaying tool resources with star rating,
 * category, pricing, and link to the tool's website.
 */
export function ToolCard({
  name,
  description,
  rating,
  icon,
  url,
  category,
  pricing,
}: ToolCardProps): React.ReactElement {
  // Clamp rating between 1 and 5
  const clampedRating = Math.min(5, Math.max(1, rating));

  // Generate star rating display
  const renderStars = () => {
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(
        <span key={i} className={i <= clampedRating ? 'text-yellow-500' : 'text-muted-foreground/30'}>
          ★
        </span>
      );
    }
    return stars;
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex items-start gap-3 flex-1">
            {icon && (
              <img
                src={icon}
                alt={name}
                className="w-10 h-10 rounded shrink-0"
                onError={(e) => {
                  (e.target as HTMLImageElement).style.display = 'none';
                }}
              />
            )}
            <div className="flex-1 min-w-0">
              <CardTitle className="text-base">{name}</CardTitle>
              <div className="flex items-center gap-2 mt-1 flex-wrap">
                {category && <CardDescription>{category}</CardDescription>}
                <div className="flex items-center text-lg leading-none">
                  {renderStars()}
                  <span className="text-xs text-muted-foreground ml-1">({rating})</span>
                </div>
              </div>
            </div>
          </div>
          {pricing && <Badge className="shrink-0">{pricing}</Badge>}
        </div>
      </CardHeader>
      {description && (
        <CardContent>
          <p className="text-sm text-muted-foreground">{description}</p>
        </CardContent>
      )}
      {url && (
        <CardFooter>
          <Button asChild variant="outline" className="w-full">
            <a href={url} target="_blank" rel="noopener noreferrer">
              Visit Tool
            </a>
          </Button>
        </CardFooter>
      )}
    </Card>
  );
}

export default ToolCard;
