/**
 * QuoteCard Component
 *
 * Displays a quote with attribution, author title, and optional avatar.
 * Features subtle border and background styling.
 */

import React from 'react';
import { Card, CardContent } from "@/components/ui/card";

export interface QuoteCardProps {
  /** The quote text */
  quote: string;

  /** Author name */
  author: string;

  /** Author's title or role */
  title?: string;

  /** Optional context or source information */
  context?: string;

  /** Optional avatar URL for the author */
  avatar_url?: string;
}

/**
 * QuoteCard Component
 *
 * A card component for displaying quotes with attribution and styling.
 * Features a left border accent and elegant typography.
 */
export function QuoteCard({
  quote,
  author,
  title,
  context,
  avatar_url,
}: QuoteCardProps): React.ReactElement {
  return (
    <Card className="border-l-4 border-blue-500 bg-gradient-to-br from-card to-secondary/30 border-blue-500/20">
      <CardContent className="pt-6">
        <blockquote className="text-lg italic mb-4 text-white relative">
          <span className="text-blue-400 text-3xl absolute -top-2 -left-1 opacity-50">"</span>
          <span className="pl-6">{quote}</span>
          <span className="text-blue-400 text-3xl opacity-50">"</span>
        </blockquote>
        <div className="flex items-center gap-3">
          {avatar_url ? (
            <img
              src={avatar_url}
              alt={author}
              className="w-10 h-10 rounded-full border border-blue-500/30"
            />
          ) : (
            <div className="w-10 h-10 rounded-full bg-blue-950/50 border border-blue-500/30 flex items-center justify-center">
              <span className="text-sm font-semibold text-blue-300">
                {author.charAt(0).toUpperCase()}
              </span>
            </div>
          )}
          <div>
            <div className="font-semibold text-white">{author}</div>
            {title && (
              <div className="text-sm text-blue-300">{title}</div>
            )}
          </div>
        </div>
        {context && (
          <p className="text-sm text-blue-200 mt-3 pt-3 border-t border-blue-500/20">
            {context}
          </p>
        )}
      </CardContent>
    </Card>
  );
}

export default QuoteCard;
