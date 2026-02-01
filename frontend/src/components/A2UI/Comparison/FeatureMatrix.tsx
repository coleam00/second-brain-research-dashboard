/**
 * FeatureMatrix Component
 *
 * Matrix-style table showing feature availability across multiple items/products.
 * Uses green checkmarks for available features and red X marks for unavailable ones.
 */

import React from 'react';
import { Card, CardContent } from "@/components/ui/card";

export interface FeatureAvailability {
  /** Feature name */
  name: string;

  /** Feature description (optional) */
  description?: string;

  /** Boolean array indicating availability for each product/item */
  availability: boolean[];
}

export interface MatrixItem {
  /** Item/product name */
  name: string;

  /** Feature availability array (boolean values) */
  features: boolean[];

  /** Optional highlight flag */
  highlighted?: boolean;
}

export interface FeatureMatrixProps {
  /** Array of feature names or feature objects */
  features: string[] | FeatureAvailability[];

  /** Array of product/item names (column headers) */
  products?: string[];

  /** Array of items with their feature availability (alternative format) */
  items?: MatrixItem[];

  /** Optional title */
  title?: string;

  /** Optional subtitle */
  subtitle?: string;
}

/**
 * FeatureMatrix Component
 *
 * Displays a feature comparison matrix with checkmarks and X marks.
 * Supports both features-based and items-based data formats.
 */
export function FeatureMatrix({
  features,
  products,
  items,
  title,
  subtitle,
}: FeatureMatrixProps): React.ReactElement {
  // Normalize data format
  let featureList: FeatureAvailability[];
  let productList: string[];

  if (items && items.length > 0) {
    // Items-based format: convert to features-based format
    productList = items.map(item => item.name);
    const featureCount = items[0]?.features.length || 0;
    featureList = Array.from({ length: featureCount }, (_, i) => ({
      name: typeof features[i] === 'string' ? features[i] as string : (features[i] as FeatureAvailability)?.name || `Feature ${i + 1}`,
      availability: items.map(item => item.features[i] || false),
    }));
  } else {
    // Features-based format
    productList = products || [];
    featureList = features.map(f =>
      typeof f === 'string'
        ? { name: f, availability: [] }
        : f
    );
  }

  return (
    <Card className="bg-gradient-to-br from-card to-secondary/30 border-blue-500/20">
      {(title || subtitle) && (
        <div className="p-4 border-b border-blue-500/20">
          {title && <h3 className="text-lg font-semibold text-white">{title}</h3>}
          {subtitle && <p className="text-sm text-blue-200">{subtitle}</p>}
        </div>
      )}
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-blue-950/50 border-b border-blue-500/20">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-semibold text-blue-200">
                  Feature
                </th>
                {productList?.map((product: string, idx: number) => (
                  <th
                    key={idx}
                    className="px-4 py-3 text-center text-sm font-semibold text-blue-200"
                  >
                    {product}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {featureList?.map((feature: FeatureAvailability, idx: number) => (
                <tr
                  key={idx}
                  className={`border-b last:border-0 border-blue-500/10 ${
                    idx % 2 === 0 ? 'bg-slate-950/40' : 'bg-slate-900/60'
                  }`}
                >
                  <td className="px-4 py-3 text-sm font-medium text-slate-200">
                    <div>
                      {feature.name}
                      {feature.description && (
                        <div className="text-xs text-blue-300 mt-1">
                          {feature.description}
                        </div>
                      )}
                    </div>
                  </td>
                  {feature.availability.map((avail: boolean, pIdx: number) => (
                    <td key={pIdx} className="px-4 py-3 text-center">
                      <span
                        className={`text-lg ${
                          avail ? 'text-blue-400' : 'text-slate-600'
                        }`}
                      >
                        {avail ? '✓' : '✗'}
                      </span>
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}

export default FeatureMatrix;
