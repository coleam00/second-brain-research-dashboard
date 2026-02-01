/**
 * VsCard Component
 *
 * Head-to-head VS comparison card with visual styling.
 * Displays two items side-by-side with comparison metrics and optional winner highlight.
 */

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export interface ComparisonPoint {
  /** Metric name (e.g., "Speed", "Price") */
  metric: string;

  /** Value for left item */
  value_a: string | number;

  /** Value for right item */
  value_b: string | number;

  /** Optional winner indicator for this metric */
  winner?: 'left' | 'right' | 'tie';
}

export interface VsCardItem {
  /** Item name */
  name: string;

  /** Optional item image URL */
  image_url?: string;

  /** Optional item description */
  description?: string;
}

export interface VsCardProps {
  /** Left item to compare */
  leftItem?: string;
  item_a?: VsCardItem;

  /** Right item to compare */
  rightItem?: string;
  item_b?: VsCardItem;

  /** Optional image for left item */
  leftImage?: string;

  /** Optional image for right item */
  rightImage?: string;

  /** Overall winner */
  winner?: 'left' | 'right' | 'tie';

  /** Comparison points/metrics */
  comparison_points?: ComparisonPoint[];
}

/**
 * VsCard Component
 *
 * Displays a head-to-head comparison between two items
 * with VS badge and optional metrics.
 */
export function VsCard({
  leftItem,
  rightItem,
  leftImage,
  rightImage,
  winner,
  item_a,
  item_b,
  comparison_points,
}: VsCardProps): React.ReactElement {
  // Support both simple string items and complex item objects
  const itemA = item_a || { name: leftItem || 'Item A', image_url: leftImage };
  const itemB = item_b || { name: rightItem || 'Item B', image_url: rightImage };

  return (
    <Card className={`bg-gradient-to-br from-card to-secondary/30 border-blue-500/20 ${
      winner === 'left' ? 'border-l-4 border-l-blue-500' :
      winner === 'right' ? 'border-r-4 border-r-blue-500' : ''
    }`}>
      <CardHeader>
        <div className="flex items-center justify-between gap-4">
          <div className="flex-1 text-center">
            {itemA.image_url && (
              <img
                src={itemA.image_url}
                alt={itemA.name}
                className="w-16 h-16 object-cover rounded-full mx-auto mb-2 border border-blue-500/30"
              />
            )}
            <CardTitle className="text-base text-white">
              {itemA.name}
            </CardTitle>
            {winner === 'left' && (
              <Badge className="mt-1 bg-blue-600 hover:bg-blue-700 text-white border-0">Winner</Badge>
            )}
          </div>

          <Badge variant="outline" className="bg-blue-600 border-blue-500 text-white px-3 py-1 text-sm font-bold">
            VS
          </Badge>

          <div className="flex-1 text-center">
            {itemB.image_url && (
              <img
                src={itemB.image_url}
                alt={itemB.name}
                className="w-16 h-16 object-cover rounded-full mx-auto mb-2 border border-blue-500/30"
              />
            )}
            <CardTitle className="text-base text-white">
              {itemB.name}
            </CardTitle>
            {winner === 'right' && (
              <Badge className="mt-1 bg-blue-600 hover:bg-blue-700 text-white border-0">Winner</Badge>
            )}
          </div>
        </div>
      </CardHeader>

      {comparison_points && comparison_points.length > 0 && (
        <CardContent>
          <div className="space-y-3">
            {comparison_points.map((point: ComparisonPoint, idx: number) => (
              <div key={idx} className="grid grid-cols-3 gap-4 items-center">
                <div className={`text-sm text-right text-slate-200 ${
                  point.winner === 'left' ? 'font-bold text-blue-400' : ''
                }`}>
                  {point.value_a}
                </div>
                <div className="text-xs text-center text-blue-300 font-medium">
                  {point.metric}
                </div>
                <div className={`text-sm text-slate-200 ${
                  point.winner === 'right' ? 'font-bold text-blue-400' : ''
                }`}>
                  {point.value_b}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      )}
    </Card>
  );
}

export default VsCard;
