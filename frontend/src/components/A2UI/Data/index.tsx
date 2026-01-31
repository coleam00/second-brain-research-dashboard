/**
 * Data Components - Barrel Export
 *
 * Exports all data visualization and metrics components:
 * - StatCard: Single statistic display
 * - MetricRow: Multiple metrics in horizontal row
 * - ProgressRing: Circular SVG progress indicator
 * - ComparisonBar: Horizontal bar comparison
 * - DataTable: Table with sorting
 * - MiniChart: Simple SVG chart (line/bar)
 */

export { StatCard } from './StatCard';
export type { StatCardProps } from './StatCard';

export { MetricRow } from './MetricRow';
export type { MetricRowProps, Metric } from './MetricRow';

export { ProgressRing } from './ProgressRing';
export type { ProgressRingProps } from './ProgressRing';

export { ComparisonBar } from './ComparisonBar';
export type { ComparisonBarProps } from './ComparisonBar';

export { DataTable } from './DataTable';
export type { DataTableProps } from './DataTable';

export { MiniChart } from './MiniChart';
export type { MiniChartProps } from './MiniChart';
