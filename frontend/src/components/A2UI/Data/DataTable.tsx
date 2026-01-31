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
    <Card>
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full">
            {caption && (
              <caption className="p-4 text-sm text-muted-foreground dark:text-slate-400">
                {caption}
              </caption>
            )}
            <thead className="border-b dark:border-slate-700">
              <tr>
                {headers?.map((header: string, idx: number) => (
                  <th
                    key={idx}
                    className={`px-4 py-3 text-left text-sm font-semibold dark:text-slate-200 ${
                      sortable ? 'cursor-pointer hover:bg-muted/50 dark:hover:bg-slate-800' : ''
                    }`}
                    onClick={() => handleSort(idx)}
                  >
                    <div className="flex items-center gap-2">
                      {header}
                      {sortable && sortColumn === idx && (
                        <span className="text-xs text-muted-foreground dark:text-slate-400">
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
                  className="border-b last:border-0 hover:bg-muted/50 dark:border-slate-700 dark:hover:bg-slate-800/50"
                >
                  {row.map((cell, cellIdx) => (
                    <td
                      key={cellIdx}
                      className="px-4 py-3 text-sm dark:text-slate-300"
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
