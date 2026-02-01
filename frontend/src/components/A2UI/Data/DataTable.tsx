/**
 * DataTable Component
 *
 * Displays tabular data with optional sorting functionality.
 * Supports headers, rows, and captions with dark theme.
 */

import React, { useState } from 'react';
import { Card, CardContent } from "@/components/ui/card";

export interface DataTableProps {
  /** Column headers */
  headers: string[];

  /** Table rows (array of arrays) */
  rows: (string | number)[][];

  /** Optional table caption */
  caption?: string;

  /** Enable column sorting (defaults to false) */
  sortable?: boolean;
}

/**
 * DataTable Component
 *
 * A table component with optional sorting capabilities
 * and dark theme support.
 */
export function DataTable({
  headers,
  rows,
  caption,
  sortable = false,
}: DataTableProps): React.ReactElement {
  const [sortColumn, setSortColumn] = useState<number | null>(null);
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc');
  const [sortedRows, setSortedRows] = useState(rows);

  const handleSort = (columnIndex: number) => {
    if (!sortable) return;

    const newDirection =
      sortColumn === columnIndex && sortDirection === 'asc' ? 'desc' : 'asc';

    const sorted = [...rows].sort((a, b) => {
      const aVal = a[columnIndex];
      const bVal = b[columnIndex];

      // Handle numeric sorting
      if (typeof aVal === 'number' && typeof bVal === 'number') {
        return newDirection === 'asc' ? aVal - bVal : bVal - aVal;
      }

      // Handle string sorting
      const aStr = String(aVal).toLowerCase();
      const bStr = String(bVal).toLowerCase();

      if (aStr < bStr) return newDirection === 'asc' ? -1 : 1;
      if (aStr > bStr) return newDirection === 'asc' ? 1 : -1;
      return 0;
    });

    setSortColumn(columnIndex);
    setSortDirection(newDirection);
    setSortedRows(sorted);
  };

  const displayRows = sortable ? sortedRows : rows;

  return (
    <Card className="border-blue-500/20 overflow-hidden">
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full">
            {caption && (
              <caption className="p-4 text-sm text-blue-300/70">
                {caption}
              </caption>
            )}
            <thead className="border-b border-blue-500/20 bg-gradient-to-r from-blue-500/10 to-transparent">
              <tr>
                {headers?.map((header: string, idx: number) => (
                  <th
                    key={idx}
                    className={`px-4 py-3 text-left text-sm font-semibold text-blue-200 ${
                      sortable ? 'cursor-pointer hover:bg-blue-500/10' : ''
                    }`}
                    onClick={() => handleSort(idx)}
                  >
                    <div className="flex items-center gap-2">
                      {header}
                      {sortable && sortColumn === idx && (
                        <span className="text-xs text-blue-400">
                          {sortDirection === 'asc' ? '↑' : '↓'}
                        </span>
                      )}
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {displayRows?.map((row: (string | number)[], rowIdx: number) => (
                <tr
                  key={rowIdx}
                  className={`border-b border-blue-500/10 last:border-0 hover:bg-blue-500/10 transition-colors ${
                    rowIdx % 2 === 0 ? 'bg-secondary/20' : 'bg-transparent'
                  }`}
                >
                  {row.map((cell, cellIdx) => (
                    <td
                      key={cellIdx}
                      className="px-4 py-3 text-sm text-foreground/90"
                    >
                      {cell}
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

export default DataTable;
