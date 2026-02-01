/**
 * BookCard Component
 *
 * Displays a book resource with cover image, title, author, rating, and description.
 * Supports lazy image loading and fallback for missing covers.
 */

import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export interface BookCardProps {
  /** Book title */
  title: string;

  /** Book author */
  author: string;

  /** Book cover image URL (accepts both 'coverImage' and 'coverImageUrl' from backend) */
  coverImage?: string;
  coverImageUrl?: string;

  /** Star rating (1-5) - optional */
  rating?: number;

  /** Optional publication year */
  year?: number;

  /** Optional ISBN from backend */
  isbn?: string;

  /** Optional book description */
  description?: string;

  /** Optional link to book details/purchase */
  url?: string;
}

/**
 * BookCard Component
 *
 * A card component for displaying book resources with cover image,
 * metadata, and rating. Images are lazy-loaded with fallback support.
 */
export function BookCard({
  title,
  author,
  coverImage,
  coverImageUrl,
  rating,
  year,
  isbn,
  description,
  url,
}: BookCardProps): React.ReactElement {
  const [imageError, setImageError] = React.useState(false);

  // Support both 'coverImage' and 'coverImageUrl' prop names (backend sends 'coverImageUrl')
  const displayCoverImage = coverImage || coverImageUrl;

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
      <>
        <div className="flex items-center text-base leading-none">
          {stars}
        </div>
        <span className="text-xs text-blue-200/60">
          {rating}/5
        </span>
      </>
    );
  };

  return (
    <Card className="overflow-hidden bg-gradient-to-br from-card to-secondary/30 border-blue-500/20">
      {!imageError && displayCoverImage ? (
        <img
          src={displayCoverImage}
          alt={title}
          loading="lazy"
          className="w-full h-64 object-cover"
          onError={() => setImageError(true)}
        />
      ) : (
        <div className="w-full h-48 bg-blue-950/30 flex items-center justify-center">
          <div className="text-center p-4">
            <span className="text-5xl text-blue-400/30">📚</span>
            <p className="text-xs text-blue-300/50 mt-2">No cover available</p>
          </div>
        </div>
      )}
      <CardHeader>
        <CardTitle className="text-base line-clamp-2 text-white">{title}</CardTitle>
        <CardDescription>
          <div className="space-y-1">
            <div className="text-blue-300/80">by {author}</div>
            <div className="flex items-center gap-2 flex-wrap">
              {renderStars()}
              {year && (
                <>
                  {rating && <span className="text-xs text-blue-200/60">•</span>}
                  <span className="text-xs text-blue-200/60">{year}</span>
                </>
              )}
              {isbn && (
                <>
                  <span className="text-xs text-blue-200/60">•</span>
                  <span className="text-xs text-blue-200/40">ISBN: {isbn}</span>
                </>
              )}
            </div>
          </div>
        </CardDescription>
      </CardHeader>
      {description && (
        <CardContent>
          <p className="text-sm text-blue-200/70 line-clamp-3">{description}</p>
        </CardContent>
      )}
      {url && (
        <CardFooter>
          <Button asChild variant="outline" className="w-full border-blue-500/30 text-blue-300 hover:bg-blue-500/20 hover:text-blue-200 hover:border-blue-400/50">
            <a href={url} target="_blank" rel="noopener noreferrer">
              Read More
            </a>
          </Button>
        </CardFooter>
      )}
    </Card>
  );
}

export default BookCard;
