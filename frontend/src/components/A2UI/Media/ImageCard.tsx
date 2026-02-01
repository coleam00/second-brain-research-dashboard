/**
 * ImageCard Component
 *
 * Displays an image with title, description, source attribution, and lazy loading.
 * Includes fallback handling for broken images.
 */

import React, { useState } from 'react';
import { Card, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export interface ImageCardProps {
  /** Image title */
  title?: string;

  /** Image description or caption */
  description?: string;

  /** Image URL */
  image_url: string;

  /** Alt text for accessibility */
  alt_text?: string;

  /** Image source attribution */
  source?: string;

  /** Link to original image or article */
  url?: string;

  /** Custom height class (default: h-64) */
  height?: string;
}

/**
 * ImageCard Component
 *
 * A card component for displaying images with lazy loading,
 * optional metadata, and source attribution.
 */
export function ImageCard({
  title,
  description,
  image_url,
  alt_text,
  source,
  url,
  height = 'h-64',
}: ImageCardProps): React.ReactElement {
  const [imageError, setImageError] = useState(false);
  const [imageLoaded, setImageLoaded] = useState(false);

  const handleImageError = () => {
    setImageError(true);
  };

  const handleImageLoad = () => {
    setImageLoaded(true);
  };

  return (
    <Card className="overflow-hidden bg-gradient-to-br from-card to-secondary/30 border-blue-500/20">
      {/* Image Section */}
      <div className={`relative ${height} bg-blue-950/20 border-2 border-blue-500/10`}>
        {!imageError ? (
          <>
            {!imageLoaded && (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
              </div>
            )}
            <img
              src={image_url}
              alt={alt_text || title || 'Image'}
              className={`w-full h-full object-cover transition-opacity duration-300 ${
                imageLoaded ? 'opacity-100' : 'opacity-0'
              }`}
              loading="lazy"
              onError={handleImageError}
              onLoad={handleImageLoad}
            />
          </>
        ) : (
          <div className="w-full h-full flex items-center justify-center bg-blue-950/20">
            <div className="text-center text-blue-300/60 p-4">
              <svg
                className="w-16 h-16 mx-auto mb-2 opacity-50"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                />
              </svg>
              <p className="text-sm">Image not available</p>
            </div>
          </div>
        )}
      </div>

      {/* Metadata Section */}
      {(title || description || source) && (
        <CardHeader>
          {title && <CardTitle className="text-base text-white">{title}</CardTitle>}
          {(description || source) && (
            <CardDescription className="text-blue-300">
              {description}
              {description && source && ' • '}
              {source && `Source: ${source}`}
            </CardDescription>
          )}
        </CardHeader>
      )}

      {/* Footer with Link */}
      {url && (
        <CardFooter>
          <Button asChild variant="outline" className="w-full border-blue-500/30 text-blue-300 hover:bg-blue-500/10 hover:text-blue-200">
            <a href={url} target="_blank" rel="noopener noreferrer">
              View Original
            </a>
          </Button>
        </CardFooter>
      )}
    </Card>
  );
}

export default ImageCard;
