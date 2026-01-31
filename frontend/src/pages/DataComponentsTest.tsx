/**
 * Data Components Test Page (DYN-211)
 * Tests all 6 data visualization components
 */

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { A2UIRendererList } from "@/components/A2UIRenderer";
import { type A2UIComponent } from "@/lib/a2ui-catalog";

// Sample data components for testing
const dataTestComponents: A2UIComponent[] = [
  // StatCard Tests
  {
    id: 'stat-1',
    type: 'a2ui.StatCard',
    props: {
      label: 'Total Revenue',
      value: 125000,
      unit: 'USD',
      trend: '+15.3%',
      icon: '💰',
    },
  },
  {
    id: 'stat-2',
    type: 'a2ui.StatCard',
    props: {
      label: 'Active Users',
      value: 8432,
      unit: 'users',
      trend: '+8.7%',
      icon: '👥',
    },
  },
  {
    id: 'stat-3',
    type: 'a2ui.StatCard',
    props: {
      label: 'Response Time',
      value: 245,
      unit: 'ms',
      trend: '-12%',
      icon: '⚡',
    },
  },

  // MetricRow Tests
  {
    id: 'metric-1',
    type: 'a2ui.MetricRow',
    props: {
      label: 'Performance Score',
      value: 95,
      previous_value: 87,
      unit: '%',
      change_percentage: 9.2,
    },
  },
  {
    id: 'metric-2',
    type: 'a2ui.MetricRow',
    props: {
      label: 'Server Load',
      value: 68,
      previous_value: 72,
      unit: '%',
      change_percentage: -5.6,
    },
  },

  // ProgressRing Tests
  {
    id: 'progress-1',
    type: 'a2ui.ProgressRing',
    props: {
      percentage: 75,
      label: 'Project Completion',
      color: 'success',
      size: 120,
    },
  },
  {
    id: 'progress-2',
    type: 'a2ui.ProgressRing',
    props: {
      percentage: 45,
      label: 'Storage Used',
      color: 'warning',
      size: 120,
    },
  },
  {
    id: 'progress-3',
    type: 'a2ui.ProgressRing',
    props: {
      percentage: 92,
      label: 'CPU Usage',
      color: 'danger',
      size: 120,
    },
  },

  // ComparisonBar Tests
  {
    id: 'comparison-1',
    type: 'a2ui.ComparisonBar',
    props: {
      label: 'Revenue Comparison',
      value_a: 85000,
      value_b: 62000,
      label_a: 'Q4 2024',
      label_b: 'Q3 2024',
    },
  },
  {
    id: 'comparison-2',
    type: 'a2ui.ComparisonBar',
    props: {
      label: 'User Growth',
      value_a: 12500,
      value_b: 18200,
      label_a: 'Last Month',
      label_b: 'This Month',
    },
  },

  // DataTable Test
  {
    id: 'table-1',
    type: 'a2ui.DataTable',
    props: {
      headers: ['Name', 'Role', 'Score', 'Status'],
      rows: [
        ['Alice Johnson', 'Engineer', 95, 'Active'],
        ['Bob Smith', 'Designer', 88, 'Active'],
        ['Carol Davis', 'Manager', 92, 'Active'],
        ['David Lee', 'Developer', 87, 'Pending'],
        ['Emma Wilson', 'Analyst', 91, 'Active'],
      ],
      caption: 'Team Performance Report',
      sortable: true,
    },
  },

  // MiniChart Tests (Bar)
  {
    id: 'chart-bar-1',
    type: 'a2ui.MiniChart',
    props: {
      data: [12, 19, 15, 25, 22, 18, 30],
      label: 'Weekly Activity (Bar)',
      type: 'bar',
      color: 'success',
      height: 60,
    },
  },
  {
    id: 'chart-bar-2',
    type: 'a2ui.MiniChart',
    props: {
      data: [45, 52, 48, 55, 60, 58, 65],
      label: 'Sales Trend (Bar)',
      type: 'bar',
      color: 'primary',
      height: 60,
    },
  },

  // MiniChart Tests (Line)
  {
    id: 'chart-line-1',
    type: 'a2ui.MiniChart',
    props: {
      data: [10, 15, 12, 20, 18, 25, 22],
      label: 'Trend Analysis (Line)',
      type: 'line',
      color: 'primary',
      height: 60,
    },
  },
  {
    id: 'chart-line-2',
    type: 'a2ui.MiniChart',
    props: {
      data: [30, 35, 32, 38, 42, 40, 45],
      label: 'Growth Pattern (Line)',
      type: 'line',
      color: 'success',
      height: 60,
    },
  },
];

export default function DataComponentsTest() {
  return (
    <div className="min-h-screen bg-background text-foreground p-8">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-2">Data Components Test (DYN-211)</h1>
          <p className="text-muted-foreground">
            Testing all 6 data visualization components
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Component List</CardTitle>
            <CardDescription>All data components being tested</CardDescription>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              <li className="flex items-center gap-2">
                <span className="text-green-500">✓</span>
                <strong>StatCard</strong> - Single statistic display with trend
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500">✓</span>
                <strong>MetricRow</strong> - Horizontal metrics with change indicators
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500">✓</span>
                <strong>ProgressRing</strong> - Circular SVG progress indicator
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500">✓</span>
                <strong>ComparisonBar</strong> - Side-by-side bar comparison
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500">✓</span>
                <strong>DataTable</strong> - Sortable data table
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500">✓</span>
                <strong>MiniChart</strong> - Bar and line charts
              </li>
            </ul>
          </CardContent>
        </Card>

        <div>
          <h2 className="text-2xl font-bold mb-4">Component Examples</h2>
          <A2UIRendererList components={dataTestComponents} spacing="md" />
        </div>
      </div>
    </div>
  );
}
