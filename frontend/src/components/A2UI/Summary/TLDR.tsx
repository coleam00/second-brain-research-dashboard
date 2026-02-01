/**
 * TLDR Component
 *
 * Displays a quick summary in a highlighted box with optional key points.
 * Max 300 chars for summary text, with optional icon customization.
 */

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export interface TLDRProps {
  /** Main summary text (max 300 chars recommended) */
  summary: string;

  /** Optional array of key points */
  key_points?: string[];

  /** Optional icon or emoji (defaults to ⚡) */
  icon?: string;
}

/**
 * TLDR Component
 *
 * A highlighted card component for displaying quick summaries
 * with optional bulleted key points.
 */
export function TLDR({
  summary,
  key_points,
  icon = '⚡',
}: TLDRProps): React.ReactElement {
  return (
    <Card className="bg-gradient-to-br from-card to-secondary/30 border-blue-500/20">
      <CardHeader>
        <CardTitle className="text-sm flex items-center gap-2">
          <span className="bg-blue-500/20 px-2 py-1 rounded text-blue-300 border border-blue-500/30">
            {icon} TL;DR
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-2">
        <p className="text-sm font-medium text-white">{summary}</p>
        {key_points && key_points.length > 0 && (
          <ul className="space-y-1 mt-2">
            {key_points.map((point: string, idx: number) => (
              <li key={idx} className="text-sm text-blue-200 flex gap-2">
                <span className="text-blue-400">•</span>
                <span>{point}</span>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}

export default TLDR;
