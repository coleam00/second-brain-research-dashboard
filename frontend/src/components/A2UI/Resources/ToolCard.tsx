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
  description?: string;

  /** Star rating (1-5) - optional, defaults to not showing stars if not provided */
  rating?: number;

  /** Optional tool icon/logo URL (accepts both 'icon' and 'iconUrl' from backend) */
  icon?: string;
  iconUrl?: string;

  /** Optional tool website URL */
  url?: string;

  /** Optional category */
  category?: string;

  /** Optional pricing info */
  pricing?: string;

  /** Optional features list from backend */
  features?: string[];
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
  iconUrl,
  url,
  category,
  pricing,
  features,
}: ToolCardProps): React.ReactElement {
  // Support both 'icon' and 'iconUrl' prop names (backend sends 'iconUrl')
  const displayIcon = icon || iconUrl;

  // Generate star rating display (only if rating is provided)
  const renderStars = () => {
    if (rating === undefined || rating === null) return null;
    const clampedRating = Math.min(5, Math.max(1, rating));
    const stars = [];
    for (let i = 1; i <= 5; i++) {
      stars.push(
        <span key={i} className={i <= clampedRating ? 'text-yellow-500' : 'text-muted-foreground/30'}>
          ★
        </span>
      );
    }
    return (
      <div className="flex items-center text-lg leading-none">
        {stars}
        <span className="text-xs text-blue-200/60 ml-1">({rating})</span>
      </div>
    );
  };

  return (
    <Card className="bg-gradient-to-br from-card to-secondary/30 border-blue-500/20">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex items-start gap-3 flex-1">
            {displayIcon && (
              <img
                src={displayIcon}
                alt={name}
                className="w-10 h-10 rounded shrink-0"
                onError={(e) => {
                  (e.target as HTMLImageElement).style.display = 'none';
                }}
              />
            )}
            <div className="flex-1 min-w-0">
              <CardTitle className="text-base text-white">{name}</CardTitle>
              <div className="flex items-center gap-2 mt-1 flex-wrap">
                {category && <CardDescription className="text-blue-300/80">{category}</CardDescription>}
                {renderStars()}
              </div>
            </div>
          </div>
          {pricing && <Badge className="shrink-0 bg-blue-500/20 text-blue-300 border-blue-400/30 hover:bg-blue-500/30">{pricing}</Badge>}
        </div>
      </CardHeader>
      {(description || features) && (
        <CardContent className="space-y-2">
          {description && <p className="text-sm text-blue-200/70">{description}</p>}
          {features && features.length > 0 && (
            <ul className="text-xs text-blue-300/80 space-y-1">
              {features.slice(0, 5).map((feature, i) => (
                <li key={i} className="flex items-start gap-1">
                  <span className="text-blue-400">•</span>
                  <span>{feature}</span>
                </li>
              ))}
            </ul>
          )}
        </CardContent>
      )}
      {url && (
        <CardFooter>
          <Button asChild variant="outline" className="w-full border-blue-500/30 text-blue-300 hover:bg-blue-500/20 hover:text-blue-200 hover:border-blue-400/50">
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
