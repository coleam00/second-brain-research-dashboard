/**
 * RepoCard Component
 *
 * Displays a GitHub repository resource with GitHub-style formatting.
 * Shows repository name, owner, description, language, stars, and forks.
 */

import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export interface RepoCardProps {
  /** Repository name */
  name: string;

  /** Repository URL */
  url: string;

  /** Repository description */
  description: string;

  /** Primary programming language */
  language: string;

  /** Star count */
  stars: number;

  /** Repository owner/organization */
  owner: string;

  /** Optional fork count */
  forks?: number;
}

/**
 * RepoCard Component
 *
 * A GitHub-styled card component for displaying repository resources
 * with language badge, star count, fork count, and owner information.
 */
export function RepoCard({
  name,
  url,
  description,
  language,
  stars,
  owner,
  forks,
}: RepoCardProps): React.ReactElement {
  const formatNumber = (num: number): string => {
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}k`;
    }
    return num.toString();
  };

  return (
    <Card className="bg-gradient-to-br from-card to-secondary/30 border-blue-500/20">
      <CardHeader>
        <CardTitle className="text-base flex items-center gap-2 text-white">
          <span className="text-blue-400 shrink-0">📦</span>
          {owner && (
            <span className="text-sm text-blue-300/80 font-normal">
              {owner} /
            </span>
          )}
          <span className="truncate">{name}</span>
        </CardTitle>
        <CardDescription className="flex items-center gap-3 flex-wrap">
          {language && (
            <Badge variant="outline" className="shrink-0 bg-blue-500/20 text-blue-300 border-blue-400/30">
              {language}
            </Badge>
          )}
          {stars !== undefined && stars !== null && (
            <span className="text-xs flex items-center gap-1 text-blue-200/70">
              <span className="text-blue-400">⭐</span>
              {formatNumber(stars)}
            </span>
          )}
          {forks !== undefined && forks !== null && (
            <span className="text-xs flex items-center gap-1 text-blue-200/70">
              <span className="text-blue-400">🔀</span>
              {formatNumber(forks)}
            </span>
          )}
        </CardDescription>
      </CardHeader>
      {description && (
        <CardContent>
          <p className="text-sm text-blue-200/70 line-clamp-2">{description}</p>
        </CardContent>
      )}
      {url && (
        <CardFooter>
          <Button asChild variant="outline" className="w-full border-blue-500/30 text-blue-300 hover:bg-blue-500/20 hover:text-blue-200 hover:border-blue-400/50">
            <a href={url} target="_blank" rel="noopener noreferrer">
              View Repository
            </a>
          </Button>
        </CardFooter>
      )}
    </Card>
  );
}

export default RepoCard;
