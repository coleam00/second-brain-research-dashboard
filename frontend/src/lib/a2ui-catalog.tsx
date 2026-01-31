/**
 * A2UI Catalog - Component Type Registry
 *
 * This catalog maps backend A2UI component types (a2ui.*) to React components.
 * The A2UIRenderer uses this catalog to dynamically render components based on
 * backend-generated specs.
 */

import React from 'react';
import { Badge } from "@/components/ui/badge";
import { HeadlineCard, TrendIndicator, TimelineEvent, NewsTicker } from "@/components/A2UI/News";
import { ProfileCard, CompanyCard, QuoteCard, ExpertTip } from "@/components/A2UI/People";
import { TLDR, KeyTakeaways, ExecutiveSummary, TableOfContents } from "@/components/A2UI/Summary";
import { VideoCard, ImageCard, PlaylistCard, PodcastCard } from "@/components/A2UI/Media";
import { StatCard, MetricRow, ProgressRing, ComparisonBar, DataTable, MiniChart } from "@/components/A2UI/Data";
import { RankedItem, ChecklistItem, ProConItem, BulletPoint } from "@/components/A2UI/Lists";
import { LinkCard, ToolCard, BookCard, RepoCard } from "@/components/A2UI/Resources";
import { ComparisonTable, VsCard, FeatureMatrix, PricingTable } from "@/components/A2UI/Comparison";
import { StepCard, CodeBlock, CalloutCard, CommandCard } from "@/components/A2UI/Instructional";
import { Section, Grid, Columns, Tabs, Accordion, Carousel, Sidebar } from "@/components/A2UI/Layout";

/**
 * A2UI Component Specification
 * Matches the backend A2UIComponent structure
 */
export interface A2UIComponent {
  id: string;
  type: string; // e.g., "a2ui.StatCard", "a2ui.HeadlineCard"
  props: Record<string, any>;
  children?: A2UIComponent[];
  layout?: {
    width?: string;
    height?: string;
    position?: "relative" | "absolute" | "fixed" | "sticky";
    className?: string;
  };
  styling?: {
    variant?: string;
    theme?: string;
    className?: string;
  };
}

/**
 * Component renderer function signature
 */
export type ComponentRenderer = (props: any, children?: React.ReactNode) => React.ReactElement;

/**
 * A2UI Component Catalog
 * Maps a2ui.* types to React component renderers
 */
export const a2uiCatalog: Record<string, ComponentRenderer> = {
  // ===== NEWS COMPONENTS =====
  "a2ui.HeadlineCard": (props: any) => <HeadlineCard {...props} />,
  "a2ui.TrendIndicator": (props: any) => <TrendIndicator {...props} />,
  "a2ui.TimelineEvent": (props: any) => <TimelineEvent {...props} />,
  "a2ui.NewsTicker": (props: any) => <NewsTicker {...props} />,

  // ===== MEDIA COMPONENTS =====
  "a2ui.VideoCard": (props: any) => <VideoCard {...props} />,
  "a2ui.ImageCard": (props: any) => <ImageCard {...props} />,
  "a2ui.PlaylistCard": (props: any) => <PlaylistCard {...props} />,
  "a2ui.PodcastCard": (props: any) => <PodcastCard {...props} />,

  // ===== DATA COMPONENTS =====
  "a2ui.StatCard": (props: any) => <StatCard {...props} />,
  "a2ui.MetricRow": (props: any) => <MetricRow {...props} />,
  "a2ui.ProgressRing": (props: any) => <ProgressRing {...props} />,
  "a2ui.ComparisonBar": (props: any) => <ComparisonBar {...props} />,
  "a2ui.DataTable": (props: any) => <DataTable {...props} />,
  "a2ui.MiniChart": (props: any) => <MiniChart {...props} />,

  // ===== LIST COMPONENTS =====
  "a2ui.RankedItem": (props: any) => <RankedItem {...props} />,
  "a2ui.ChecklistItem": (props: any) => <ChecklistItem {...props} />,
  "a2ui.ProConItem": (props: any) => <ProConItem {...props} />,
  "a2ui.BulletPoint": (props: any) => <BulletPoint {...props} />,

  // ===== RESOURCE COMPONENTS =====
  "a2ui.LinkCard": (props: any) => <LinkCard {...props} />,
  "a2ui.ToolCard": (props: any) => <ToolCard {...props} />,
  "a2ui.BookCard": (props: any) => <BookCard {...props} />,
  "a2ui.RepoCard": (props: any) => <RepoCard {...props} />,

  // ===== PEOPLE COMPONENTS =====
  "a2ui.ProfileCard": (props: any) => <ProfileCard {...props} />,
  "a2ui.CompanyCard": (props: any) => <CompanyCard {...props} />,
  "a2ui.QuoteCard": (props: any) => <QuoteCard {...props} />,

  // ===== SUMMARY COMPONENTS =====
  "a2ui.ExpertTip": (props: any) => <ExpertTip {...props} />,
  "a2ui.TLDR": (props: any) => <TLDR {...props} />,
  "a2ui.KeyTakeaways": (props: any) => <KeyTakeaways {...props} />,
  "a2ui.ExecutiveSummary": (props: any) => <ExecutiveSummary {...props} />,
  "a2ui.TableOfContents": (props: any) => <TableOfContents {...props} />,

  // ===== COMPARISON COMPONENTS =====
  "a2ui.ComparisonTable": (props: any) => <ComparisonTable {...props} />,
  "a2ui.VsCard": (props: any) => <VsCard {...props} />,
  "a2ui.FeatureMatrix": (props: any) => <FeatureMatrix {...props} />,
  "a2ui.PricingTable": (props: any) => <PricingTable {...props} />,

  // ===== INSTRUCTIONAL COMPONENTS =====
  "a2ui.StepCard": (props: any) => <StepCard {...props} />,
  "a2ui.CodeBlock": (props: any) => <CodeBlock {...props} />,
  "a2ui.CalloutCard": (props: any) => <CalloutCard {...props} />,
  "a2ui.CommandCard": (props: any) => <CommandCard {...props} />,

  // ===== LAYOUT COMPONENTS =====
  "a2ui.Section": (props: any, children?: React.ReactNode) => (
    <Section {...props}>{children}</Section>
  ),

  "a2ui.Grid": (props: any, children?: React.ReactNode) => (
    <Grid {...props}>{children}</Grid>
  ),

  "a2ui.Columns": (props: any, children?: React.ReactNode) => (
    <Columns {...props}>{children}</Columns>
  ),

  "a2ui.Tabs": (props: any) => <Tabs {...props} />,

  "a2ui.Accordion": (props: any) => <Accordion {...props} />,

  "a2ui.Carousel": (props: any) => <Carousel {...props} />,

  "a2ui.Sidebar": (props: any) => <Sidebar {...props} />,

  // ===== TAG COMPONENTS =====
  "a2ui.Tag": ({ label, color, removable }: any) => (
    <Badge variant="secondary" className={color ? `bg-${color}-500/20 text-${color}-700` : ''}>
      {label}
      {removable && <span className="ml-1 cursor-pointer">×</span>}
    </Badge>
  ),

  "a2ui.Badge": ({ label, variant, icon }: any) => (
    <Badge variant={variant || 'default'}>
      {icon && <span className="mr-1">{icon}</span>}
      {label}
    </Badge>
  ),

  "a2ui.CategoryTag": ({ category, count }: any) => (
    <Badge variant="outline">
      {category}
      {count !== undefined && <span className="ml-1 text-xs">({count})</span>}
    </Badge>
  ),

  "a2ui.StatusIndicator": ({ status, label, pulse }: any) => {
    const colors = {
      active: 'bg-green-500',
      inactive: 'bg-gray-500',
      pending: 'bg-yellow-500',
      error: 'bg-red-500',
    };

    return (
      <div className="flex items-center gap-2">
        <div className="relative">
          <div className={`w-2 h-2 rounded-full ${colors[status as keyof typeof colors] || colors.inactive}`} />
          {pulse && (
            <div className={`absolute inset-0 w-2 h-2 rounded-full ${colors[status as keyof typeof colors] || colors.inactive} animate-ping opacity-75`} />
          )}
        </div>
        {label && <span className="text-sm">{label}</span>}
      </div>
    );
  },

  "a2ui.PriorityBadge": ({ priority }: any) => {
    const variants = {
      low: { variant: 'secondary' as const, label: 'Low', color: 'text-blue-500' },
      medium: { variant: 'default' as const, label: 'Medium', color: 'text-yellow-500' },
      high: { variant: 'destructive' as const, label: 'High', color: 'text-red-500' },
      critical: { variant: 'destructive' as const, label: 'Critical', color: 'text-red-700' },
    };

    const config = variants[priority as keyof typeof variants] || variants.medium;

    return (
      <Badge variant={config.variant} className={config.color}>
        {config.label}
      </Badge>
    );
  },

  // ===== ADDITIONAL COMPONENTS =====
  "a2ui.TagCloud": ({ tags }: any) => (
    <div className="flex flex-wrap gap-2">
      {tags?.map((tag: any, idx: number) => (
        <Badge key={idx} variant="secondary" style={{ fontSize: `${tag.size || 1}rem` }}>
          {tag.label}
        </Badge>
      ))}
    </div>
  ),

  "a2ui.CategoryBadge": ({ category, color }: any) => (
    <Badge variant="outline" className={color ? `border-${color}-500 text-${color}-700` : ''}>
      {category}
    </Badge>
  ),

  "a2ui.DifficultyBadge": ({ level }: any) => {
    const variants = {
      beginner: { variant: 'secondary' as const, label: 'Beginner', icon: '●' },
      intermediate: { variant: 'default' as const, label: 'Intermediate', icon: '●●' },
      advanced: { variant: 'destructive' as const, label: 'Advanced', icon: '●●●' },
    };

    const config = variants[level as keyof typeof variants] || variants.beginner;

    return (
      <Badge variant={config.variant}>
        {config.icon} {config.label}
      </Badge>
    );
  },
};

/**
 * Get component renderer from catalog
 */
export function getComponentRenderer(type: string): ComponentRenderer | undefined {
  return a2uiCatalog[type];
}

/**
 * Check if component type is registered
 */
export function isComponentRegistered(type: string): boolean {
  return type in a2uiCatalog;
}

/**
 * Get all registered component types
 */
export function getRegisteredTypes(): string[] {
  return Object.keys(a2uiCatalog);
}
