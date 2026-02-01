/**
 * ExecutiveSummary Component
 *
 * Displays a comprehensive summary with optional title, overview text,
 * metrics array, and recommendations list.
 */

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export interface SummaryMetric {
  /** Metric label */
  label: string;

  /** Metric value */
  value: string | number;

  /** Optional unit (%, $, etc.) */
  unit?: string;

  /** Optional trend indicator */
  trend?: 'up' | 'down' | 'neutral';
}

export interface ExecutiveSummaryProps {
  /** Main title */
  title?: string;

  /** Overview/summary text */
  summary: string;

  /** Optional array of metrics */
  metrics?: SummaryMetric[];

  /** Optional array of recommendation strings */
  recommendations?: string[];
}

/**
 * ExecutiveSummary Component
 *
 * A comprehensive summary card with title, summary text,
 * metrics display, and actionable recommendations.
 */
export function ExecutiveSummary({
  title = 'Executive Summary',
  summary,
  metrics,
  recommendations,
}: ExecutiveSummaryProps): React.ReactElement {
  const getTrendIcon = (trend?: 'up' | 'down' | 'neutral') => {
    switch (trend) {
      case 'up':
        return <span className="text-green-500">↑</span>;
      case 'down':
        return <span className="text-red-500">↓</span>;
      case 'neutral':
        return <span className="text-yellow-500">→</span>;
      default:
        return null;
    }
  };

  return (
    <Card className="bg-gradient-to-br from-card to-secondary/30 border-blue-500/20">
      <CardHeader>
        <CardTitle className="text-blue-300">{title}</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm text-white">{summary}</p>

        {metrics && metrics.length > 0 && (
          <div>
            <h4 className="font-semibold text-sm mb-3 text-blue-300">Key Metrics</h4>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
              {metrics.map((metric, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-lg bg-blue-950/30 border border-blue-500/10 space-y-1"
                >
                  <div className="text-xs text-blue-300">
                    {metric.label}
                  </div>
                  <div className="flex items-baseline gap-1">
                    <span className="text-lg font-bold text-white">
                      {metric.value}
                    </span>
                    {metric.unit && (
                      <span className="text-sm text-blue-200">
                        {metric.unit}
                      </span>
                    )}
                    {metric.trend && getTrendIcon(metric.trend)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {recommendations && recommendations.length > 0 && (
          <div>
            <h4 className="font-semibold text-sm mb-2 text-blue-300">Recommendations</h4>
            <ul className="space-y-2">
              {recommendations.map((rec, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <Badge variant="outline" className="shrink-0 mt-0.5 border-blue-500/30 text-blue-300 bg-blue-500/10">
                    {idx + 1}
                  </Badge>
                  <span className="text-sm text-blue-100">
                    {rec}
                  </span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

export default ExecutiveSummary;
