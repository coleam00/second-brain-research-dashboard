/**
 * ComparisonTable Component
 *
 * Side-by-side table comparison for displaying features/items in tabular format.
 * Includes alternating row colors for readability and dark theme support.
 */

import React from 'react';
import { Card, CardContent } from "@/components/ui/card";

export interface ComparisonTableProps {
  /** Table column headers */
  headers: string[];

  /** Table rows, each row is an array of cell values */
  rows: Array<string[] | any[]>;

  /** Optional table title */
  title?: string;

  /** Optional table subtitle/description */
  subtitle?: string;

  /** Optional table caption */
  caption?: string;
}

/**
 * ComparisonTable Component
 *
 * Displays a comparison table with headers and rows.
 * Supports boolean values (rendered as checkmarks/X marks).
 */
export function ComparisonTable({
  headers,
  rows,
  title,
  subtitle,
  caption,
}: ComparisonTableProps): React.ReactElement {
  return (
    <Card className="dark:bg-slate-900">
      {(title || subtitle) && (
        <div className="p-4 border-b dark:border-slate-700">
          {title && <h3 className="text-lg font-semibold dark:text-slate-100">{title}</h3>}
          {subtitle && <p className="text-sm text-muted-foreground dark:text-slate-400">{subtitle}</p>}
        </div>
      )}
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full">
            {caption && (
              <caption className="p-4 text-sm font-semibold dark:text-slate-200">
                {caption}
              </caption>
            )}
            <thead className="bg-muted dark:bg-slate-800">
              <tr>
                {headers?.map((header: string, idx: number) => (
                  <th
                    key={idx}
                    className="px-4 py-3 text-left text-sm font-semibold dark:text-slate-200"
                  >
                    {header}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows?.map((row: any, rowIdx: number) => (
                <tr
                  key={rowIdx}
                  className={`border-b last:border-0 dark:border-slate-700 ${
                    rowIdx % 2 === 0 ? 'bg-white dark:bg-slate-900' : 'bg-slate-50 dark:bg-slate-800/50'
                  }`}
                >
                  {row.map((cell: any, cellIdx: number) => (
                    <td key={cellIdx} className="px-4 py-3 text-sm dark:text-slate-300">
                      {typeof cell === 'boolean' ? (
                        <span className={cell ? 'text-green-500' : 'text-red-500'}>
                          {cell ? '✓' : '✗'}
                        </span>
                      ) : (
                        cell
                      )}
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

export default ComparisonTable;
