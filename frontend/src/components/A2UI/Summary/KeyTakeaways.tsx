/**
 * KeyTakeaways Component
 *
 * Displays a bulleted list of key points with optional category badges.
 * Supports categorization: insights, learnings, conclusions, recommendations.
 */

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export interface TakeawayItem {
  /** The takeaway text */
  text: string;

  /** Category badge type */
  category?: 'insights' | 'learnings' | 'conclusions' | 'recommendations';
}

export interface KeyTakeawaysProps {
  /** Array of takeaway items */
  items: (string | TakeawayItem)[];

  /** Optional title override */
  title?: string;
}

/**
 * KeyTakeaways Component
 *
 * A card component for displaying key takeaways with optional
 * category badges for each item.
 */
export function KeyTakeaways({
  items,
  title = 'Key Takeaways',
}: KeyTakeawaysProps): React.ReactElement {
  const getCategoryColor = (category?: string) => {
    switch (category) {
      case 'insights':
        return 'bg-blue-500/20 text-blue-700 dark:bg-blue-500/30 dark:text-blue-300';
      case 'learnings':
        return 'bg-green-500/20 text-green-700 dark:bg-green-500/30 dark:text-green-300';
      case 'conclusions':
        return 'bg-purple-500/20 text-purple-700 dark:bg-purple-500/30 dark:text-purple-300';
      case 'recommendations':
        return 'bg-orange-500/20 text-orange-700 dark:bg-orange-500/30 dark:text-orange-300';
      default:
        return '';
    }
  };

  return (
    <Card className="bg-gradient-to-br from-card to-secondary/30 border-blue-500/20">
      <CardHeader>
        <CardTitle className="text-base text-blue-300">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2">
          {items.map((item, idx) => {
            const isString = typeof item === 'string';
            const text = isString ? item : item.text;
            const category = isString ? undefined : item.category;

            return (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-blue-400 mt-1">✓</span>
                <div className="flex-1 flex items-start gap-2 flex-wrap">
                  <span className="text-sm text-white">{text}</span>
                  {category && (
                    <Badge variant="secondary" className={getCategoryColor(category)}>
                      {category}
                    </Badge>
                  )}
                </div>
              </li>
            );
          })}
        </ul>
      </CardContent>
    </Card>
  );
}

export default KeyTakeaways;
