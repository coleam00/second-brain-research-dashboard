/**
 * TagCloud Component
 *
 * Displays multiple tags in a word cloud or fluid layout with optional size variation
 * based on frequency/count. Supports clickable tags.
 */

import React from 'react';
import { Badge } from "@/components/ui/badge";

/** Tag type for cloud display */
export interface TagItem {
  /** Tag name */
  name: string;

  /** Optional frequency count for sizing */
  count?: number;
}

export interface TagCloudProps {
  /** Array of tags (strings or tag objects with count) */
  tags: string[] | TagItem[];

  /** Maximum number of tags to display */
  maxTags?: number;

  /** Callback when a tag is clicked */
  onTagClick?: (tag: string) => void;

  /** Size variation based on count */
  sizeVariation?: boolean;

  /** Minimum font size multiplier */
  minSize?: number;

  /** Maximum font size multiplier */
  maxSize?: number;
}

/**
 * TagCloud Component
 *
 * Displays tags in a fluid, word-cloud layout with optional size scaling
 * based on frequency/count.
 */
export function TagCloud({
  tags,
  maxTags,
  onTagClick,
  sizeVariation = true,
  minSize = 0.75,
  maxSize = 1.5,
}: TagCloudProps): React.ReactElement {
  // Normalize tags to TagItem format
  const normalizedTags: TagItem[] = tags.map(tag =>
    typeof tag === 'string' ? { name: tag, count: 1 } : tag
  );

  // Limit tags if maxTags is specified
  const displayedTags = maxTags
    ? normalizedTags.slice(0, maxTags)
    : normalizedTags;

  // Calculate size scaling
  const counts = displayedTags.map(t => t.count || 1);
  const minCount = Math.min(...counts);
  const maxCount = Math.max(...counts);

  const getTagSize = (count: number = 1): number => {
    if (!sizeVariation || minCount === maxCount) {
      return 1;
    }
    const normalized = (count - minCount) / (maxCount - minCount);
    return minSize + normalized * (maxSize - minSize);
  };

  return (
    <div className="flex flex-wrap gap-2 items-center">
      {displayedTags.map((tag, idx) => {
        const tagName = typeof tag === 'string' ? tag : tag.name;
        const tagCount = typeof tag === 'string' ? 1 : tag.count;
        const size = getTagSize(tagCount);

        return (
          <Badge
            key={idx}
            variant="secondary"
            className={`
              bg-blue-950/40
              text-blue-100
              border border-blue-500/20
              hover:bg-blue-900/50
              hover:border-blue-400/30
              ${onTagClick ? 'cursor-pointer transition-all duration-200' : ''}
            `}
            style={{ fontSize: `${size}rem` }}
            onClick={() => onTagClick?.(tagName)}
          >
            {tagName}
            {tagCount !== undefined && tagCount > 1 && (
              <span className="ml-1.5 text-xs text-blue-300/70">
                ({tagCount})
              </span>
            )}
          </Badge>
        );
      })}
    </div>
  );
}

export default TagCloud;
