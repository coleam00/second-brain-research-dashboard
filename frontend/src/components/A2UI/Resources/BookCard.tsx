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

  /** Book cover image URL */
  coverImage: string;

  /** Star rating (1-5) */
  rating: number;

  /** Optional publication year */
  year?: number;

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
  rating,
  year,
  description,
  url,
}: BookCardProps): React.ReactElement {
  const [imageError, setImageError] = React.useState(false);

  // Generate star rating display
  const renderStars = () => {
    const clampedRating = Math.min(5, Math.max(1, rating));
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
    <Card className="overflow-hidden">
      {!imageError && coverImage ? (
        <img
          src={coverImage}
          alt={title}
          loading="lazy"
          className="w-full h-64 object-cover"
          onError={() => setImageError(true)}
        />
      ) : (
        <div className="w-full h-64 bg-muted flex items-center justify-center">
          <div className="text-center p-4">
            <span className="text-6xl text-muted-foreground/30">📚</span>
            <p className="text-xs text-muted-foreground mt-2">No cover available</p>
          </div>
        </div>
      )}
      <CardHeader>
        <CardTitle className="text-base line-clamp-2">{title}</CardTitle>
        <CardDescription>
          <div className="space-y-1">
            <div>by {author}</div>
            <div className="flex items-center gap-2">
              <div className="flex items-center text-base leading-none">
                {renderStars()}
              </div>
              <span className="text-xs">
                {rating}/5
              </span>
              {year && (
                <>
                  <span className="text-xs">•</span>
                  <span className="text-xs">{year}</span>
                </>
              )}
            </div>
          </div>
        </CardDescription>
      </CardHeader>
      {description && (
        <CardContent>
          <p className="text-sm text-muted-foreground line-clamp-3">{description}</p>
        </CardContent>
      )}
      {url && (
        <CardFooter>
          <Button asChild variant="outline" className="w-full">
            <a href={url} target="_blank" rel="noopener noreferrer">
              View Book
            </a>
          </Button>
        </CardFooter>
      )}
    </Card>
  );
}

export default BookCard;
