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
    <Card>
      <CardHeader>
        <CardTitle className="text-base flex items-center gap-2">
          <span className="text-muted-foreground shrink-0">📦</span>
          {owner && (
            <span className="text-sm text-muted-foreground font-normal">
              {owner} /
            </span>
          )}
          <span className="truncate">{name}</span>
        </CardTitle>
        <CardDescription className="flex items-center gap-3 flex-wrap">
          {language && (
            <Badge variant="outline" className="shrink-0">
              {language}
            </Badge>
          )}
          {stars !== undefined && stars !== null && (
            <span className="text-xs flex items-center gap-1">
              <span className="text-yellow-500">⭐</span>
              {formatNumber(stars)}
            </span>
          )}
          {forks !== undefined && forks !== null && (
            <span className="text-xs flex items-center gap-1">
              <span>🔀</span>
              {formatNumber(forks)}
            </span>
          )}
        </CardDescription>
      </CardHeader>
      {description && (
        <CardContent>
          <p className="text-sm text-muted-foreground line-clamp-2">{description}</p>
        </CardContent>
      )}
      {url && (
        <CardFooter>
          <Button asChild variant="outline" className="w-full">
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
