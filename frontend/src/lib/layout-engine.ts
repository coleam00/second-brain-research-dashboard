/**
 * Layout Engine - Component width and grid span calculation
 *
 * This module handles the conversion of width hints from the backend
 * to CSS grid column spans for responsive layout.
 */

import type { A2UIComponent } from './a2ui-catalog';

/**
 * Maps width hint values to Tailwind CSS grid column span classes.
 * Uses a 12-column grid system with responsive breakpoints.
 */
const WIDTH_TO_SPAN: Record<string, string> = {
  full: 'col-span-12',
  half: 'col-span-12 md:col-span-6',
  third: 'col-span-12 sm:col-span-6 lg:col-span-4',
  quarter: 'col-span-6 sm:col-span-3',
};

/**
 * Default width hints for each component type.
 * Used when the backend doesn't specify a width_hint.
 */
const TYPE_DEFAULT_WIDTHS: Record<string, string> = {
  // Full width components
  'a2ui.TLDR': 'full',
  'a2ui.ExecutiveSummary': 'full',
  'a2ui.CodeBlock': 'full',
  'a2ui.DataTable': 'full',
  'a2ui.TableOfContents': 'full',
  'a2ui.Section': 'full',
  'a2ui.ComparisonTable': 'full',
  'a2ui.FeatureMatrix': 'full',
  'a2ui.PricingTable': 'full',
  'a2ui.BulletPoint': 'full',
  'a2ui.StepCard': 'full',
  'a2ui.CommandCard': 'full',
  'a2ui.TimelineEvent': 'full',

  // Half width components
  'a2ui.KeyTakeaways': 'half',
  'a2ui.QuoteCard': 'half',
  'a2ui.CalloutCard': 'half',
  'a2ui.VsCard': 'half',
  'a2ui.ExpertTip': 'half',
  'a2ui.RankedItem': 'half',
  'a2ui.ProConItem': 'half',
  'a2ui.ChecklistItem': 'half',
  'a2ui.HeadlineCard': 'half',

  // Third width components (3-column grid on desktop)
  'a2ui.StatCard': 'third',
  'a2ui.LinkCard': 'third',
  'a2ui.RepoCard': 'third',
  'a2ui.VideoCard': 'third',
  'a2ui.ToolCard': 'third',
  'a2ui.BookCard': 'third',
  'a2ui.ProfileCard': 'third',
  'a2ui.CompanyCard': 'third',
  'a2ui.TrendIndicator': 'third',
  'a2ui.MetricRow': 'third',
  'a2ui.ImageCard': 'third',

  // Quarter width (small items)
  'a2ui.Badge': 'quarter',
  'a2ui.Tag': 'quarter',
};

/**
 * Get the CSS grid span class for a component based on its layout hints.
 *
 * Priority:
 * 1. Explicit width from component.layout.width
 * 2. Default width for the component type
 * 3. Full width as fallback
 *
 * @param component - The A2UI component to get grid span for
 * @returns Tailwind CSS classes for grid column span
 */
export function getGridSpan(component: A2UIComponent): string {
  // Check for explicit width hint from backend
  const explicitWidth = component.layout?.width;

  // Get default width for this component type
  const defaultWidth = TYPE_DEFAULT_WIDTHS[component.type];

  // Use explicit width, or fall back to default, or use 'full'
  const width = explicitWidth || defaultWidth || 'full';

  // Map to CSS grid span classes
  return WIDTH_TO_SPAN[width] || WIDTH_TO_SPAN.full;
}

/**
 * Get all available width options for documentation/debugging
 */
export function getAvailableWidths(): string[] {
  return Object.keys(WIDTH_TO_SPAN);
}

/**
 * Check if a component has an explicit width hint
 */
export function hasExplicitWidth(component: A2UIComponent): boolean {
  return !!component.layout?.width;
}
