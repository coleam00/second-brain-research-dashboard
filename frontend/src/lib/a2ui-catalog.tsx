/**
 * A2UI Catalog - Component Type Registry
 *
 * This catalog maps backend A2UI component types (a2ui.*) to React components.
 * The A2UIRenderer uses this catalog to dynamically render components based on
 * backend-generated specs.
 */

import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { HeadlineCard, TrendIndicator, TimelineEvent, NewsTicker } from "@/components/A2UI/News";
import { ProfileCard, CompanyCard, QuoteCard, ExpertTip } from "@/components/A2UI/People";
import { TLDR, KeyTakeaways, ExecutiveSummary, TableOfContents } from "@/components/A2UI/Summary";
import { VideoCard, ImageCard, PlaylistCard, PodcastCard } from "@/components/A2UI/Media";

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
  "a2ui.StatCard": ({ label, value, unit, trend, icon, color }: any) => (
    <Card className={color ? `border-${color}-500` : ''}>
      <CardHeader className="pb-2">
        <div className="flex justify-between items-start">
          <CardDescription>{label}</CardDescription>
          {icon && <span className="text-2xl">{icon}</span>}
        </div>
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold">
          {value}
          {unit && <span className="text-lg text-muted-foreground ml-1">{unit}</span>}
        </div>
        {trend && (
          <p className={`text-sm mt-1 ${trend.startsWith('+') ? 'text-green-500' : trend.startsWith('-') ? 'text-red-500' : 'text-muted-foreground'}`}>
            {trend}
          </p>
        )}
      </CardContent>
    </Card>
  ),

  "a2ui.MetricRow": ({ label, value, previous_value, unit, change_percentage }: any) => (
    <div className="flex items-center justify-between p-3 rounded-lg hover:bg-muted/50 transition-colors">
      <span className="text-sm font-medium">{label}</span>
      <div className="flex items-center gap-3">
        {previous_value && (
          <span className="text-xs text-muted-foreground line-through">{previous_value}{unit}</span>
        )}
        <span className="text-lg font-bold">{value}{unit}</span>
        {change_percentage && (
          <Badge variant={change_percentage > 0 ? 'default' : 'destructive'}>
            {change_percentage > 0 ? '+' : ''}{change_percentage}%
          </Badge>
        )}
      </div>
    </div>
  ),

  "a2ui.ProgressRing": ({ label, percentage, color, size }: any) => (
    <div className="flex flex-col items-center gap-2">
      <div className="relative" style={{ width: size || 100, height: size || 100 }}>
        <svg className="transform -rotate-90" width="100%" height="100%" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="45" fill="none" stroke="currentColor" strokeWidth="8" className="text-muted" />
          <circle
            cx="50"
            cy="50"
            r="45"
            fill="none"
            stroke="currentColor"
            strokeWidth="8"
            className={color ? `text-${color}-500` : 'text-primary'}
            strokeDasharray={`${2 * Math.PI * 45}`}
            strokeDashoffset={`${2 * Math.PI * 45 * (1 - percentage / 100)}`}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-xl font-bold">{percentage}%</span>
        </div>
      </div>
      {label && <span className="text-sm text-muted-foreground">{label}</span>}
    </div>
  ),

  "a2ui.ComparisonBar": ({ label, value_a, value_b, label_a, label_b, max_value }: any) => {
    const maxVal = max_value || Math.max(value_a, value_b);
    const percentA = (value_a / maxVal) * 100;
    const percentB = (value_b / maxVal) * 100;

    return (
      <div className="space-y-2">
        <div className="text-sm font-medium">{label}</div>
        <div className="flex items-center gap-2">
          <span className="text-xs w-20 text-right text-muted-foreground">{label_a}</span>
          <div className="flex-1 h-6 bg-muted rounded-full overflow-hidden flex">
            <div className="bg-blue-500 h-full transition-all" style={{ width: `${percentA}%` }} />
          </div>
          <span className="text-xs w-12 font-semibold">{value_a}</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs w-20 text-right text-muted-foreground">{label_b}</span>
          <div className="flex-1 h-6 bg-muted rounded-full overflow-hidden flex">
            <div className="bg-purple-500 h-full transition-all" style={{ width: `${percentB}%` }} />
          </div>
          <span className="text-xs w-12 font-semibold">{value_b}</span>
        </div>
      </div>
    );
  },

  "a2ui.DataTable": ({ headers, rows, caption }: any) => (
    <Card>
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full">
            {caption && <caption className="p-4 text-sm text-muted-foreground">{caption}</caption>}
            <thead className="border-b">
              <tr>
                {headers?.map((header: string, idx: number) => (
                  <th key={idx} className="px-4 py-3 text-left text-sm font-semibold">{header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows?.map((row: any[], rowIdx: number) => (
                <tr key={rowIdx} className="border-b last:border-0 hover:bg-muted/50">
                  {row.map((cell, cellIdx) => (
                    <td key={cellIdx} className="px-4 py-3 text-sm">{cell}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  ),

  "a2ui.MiniChart": ({ data, label, color }: any) => (
    <div className="space-y-1">
      {label && <div className="text-xs text-muted-foreground">{label}</div>}
      <div className="flex items-end gap-1 h-12">
        {data?.map((value: number, idx: number) => {
          const maxValue = Math.max(...data);
          const height = (value / maxValue) * 100;
          return (
            <div
              key={idx}
              className={`flex-1 ${color ? `bg-${color}-500` : 'bg-primary'} rounded-t`}
              style={{ height: `${height}%` }}
            />
          );
        })}
      </div>
    </div>
  ),

  // ===== LIST COMPONENTS =====
  "a2ui.RankedItem": ({ rank, title, description, score, badge }: any) => (
    <div className="flex items-start gap-3 p-3 rounded-lg hover:bg-muted/50 transition-colors">
      <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground font-bold text-sm">
        {rank}
      </div>
      <div className="flex-1">
        <div className="flex items-center gap-2 mb-1">
          <span className="font-semibold">{title}</span>
          {badge && <Badge variant="secondary">{badge}</Badge>}
        </div>
        {description && <p className="text-sm text-muted-foreground">{description}</p>}
      </div>
      {score && <div className="text-lg font-bold text-muted-foreground">{score}</div>}
    </div>
  ),

  "a2ui.ChecklistItem": ({ text, checked, category }: any) => (
    <div className="flex items-center gap-3 p-2 rounded hover:bg-muted/50 transition-colors">
      <div className={`w-5 h-5 rounded border-2 flex items-center justify-center ${checked ? 'bg-primary border-primary' : 'border-muted-foreground'}`}>
        {checked && <span className="text-primary-foreground text-xs">✓</span>}
      </div>
      <span className={`flex-1 ${checked ? 'line-through text-muted-foreground' : ''}`}>{text}</span>
      {category && <Badge variant="outline" className="text-xs">{category}</Badge>}
    </div>
  ),

  "a2ui.ProConItem": ({ text, type, weight }: any) => (
    <div className={`flex items-start gap-2 p-2 rounded-lg ${type === 'pro' ? 'bg-green-500/10' : 'bg-red-500/10'}`}>
      <span className={`text-lg ${type === 'pro' ? 'text-green-500' : 'text-red-500'}`}>
        {type === 'pro' ? '✓' : '✗'}
      </span>
      <span className="flex-1 text-sm">{text}</span>
      {weight && <Badge variant="secondary">{weight}</Badge>}
    </div>
  ),

  "a2ui.BulletPoint": ({ text, level, icon, color }: any) => (
    <div className="flex items-start gap-2" style={{ marginLeft: `${(level || 0) * 1.5}rem` }}>
      <span className={`mt-1 ${color ? `text-${color}-500` : 'text-primary'}`}>
        {icon || '•'}
      </span>
      <span className="text-sm">{text}</span>
    </div>
  ),

  // ===== RESOURCE COMPONENTS =====
  "a2ui.LinkCard": ({ title, description, url, favicon_url, domain }: any) => (
    <Card className="hover:bg-muted/50 transition-colors cursor-pointer" onClick={() => window.open(url, '_blank')}>
      <CardHeader>
        <div className="flex items-start gap-3">
          {favicon_url && <img src={favicon_url} alt="" className="w-6 h-6 rounded" />}
          <div className="flex-1">
            <CardTitle className="text-base">{title}</CardTitle>
            {domain && <CardDescription>{domain}</CardDescription>}
          </div>
        </div>
      </CardHeader>
      {description && (
        <CardContent>
          <p className="text-sm text-muted-foreground line-clamp-2">{description}</p>
        </CardContent>
      )}
    </Card>
  ),

  "a2ui.ToolCard": ({ name, description, category, pricing, url, logo_url }: any) => (
    <Card>
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex items-start gap-3 flex-1">
            {logo_url && <img src={logo_url} alt={name} className="w-10 h-10 rounded" />}
            <div>
              <CardTitle className="text-base">{name}</CardTitle>
              {category && <CardDescription>{category}</CardDescription>}
            </div>
          </div>
          {pricing && <Badge>{pricing}</Badge>}
        </div>
      </CardHeader>
      {description && (
        <CardContent>
          <p className="text-sm text-muted-foreground">{description}</p>
        </CardContent>
      )}
      {url && (
        <CardFooter>
          <Button asChild variant="outline" className="w-full">
            <a href={url} target="_blank" rel="noopener noreferrer">Visit Tool</a>
          </Button>
        </CardFooter>
      )}
    </Card>
  ),

  "a2ui.BookCard": ({ title, author, description, cover_url, rating, url }: any) => (
    <Card>
      {cover_url && (
        <img src={cover_url} alt={title} className="w-full h-64 object-cover rounded-t-lg" />
      )}
      <CardHeader>
        <CardTitle className="text-base">{title}</CardTitle>
        <CardDescription>
          by {author}
          {rating && ` • ${rating}/5 ⭐`}
        </CardDescription>
      </CardHeader>
      {description && (
        <CardContent>
          <p className="text-sm text-muted-foreground line-clamp-3">{description}</p>
        </CardContent>
      )}
      {url && (
        <CardFooter>
          <Button asChild variant="outline" className="w-full">
            <a href={url} target="_blank" rel="noopener noreferrer">View Book</a>
          </Button>
        </CardFooter>
      )}
    </Card>
  ),

  "a2ui.RepoCard": ({ name, description, language, stars, forks, url, owner }: any) => (
    <Card>
      <CardHeader>
        <CardTitle className="text-base flex items-center gap-2">
          <span className="text-muted-foreground">📦</span>
          {owner && <span className="text-sm text-muted-foreground">{owner} /</span>}
          {name}
        </CardTitle>
        <CardDescription className="flex items-center gap-3">
          {language && <Badge variant="outline">{language}</Badge>}
          {stars !== undefined && <span className="text-xs">⭐ {stars}</span>}
          {forks !== undefined && <span className="text-xs">🔀 {forks}</span>}
        </CardDescription>
      </CardHeader>
      {description && (
        <CardContent>
          <p className="text-sm text-muted-foreground">{description}</p>
        </CardContent>
      )}
      {url && (
        <CardFooter>
          <Button asChild variant="outline" className="w-full">
            <a href={url} target="_blank" rel="noopener noreferrer">View Repository</a>
          </Button>
        </CardFooter>
      )}
    </Card>
  ),

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
  "a2ui.ComparisonTable": ({ headers, rows, caption }: any) => (
    <Card>
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full">
            {caption && <caption className="p-4 text-sm font-semibold">{caption}</caption>}
            <thead className="bg-muted">
              <tr>
                {headers?.map((header: string, idx: number) => (
                  <th key={idx} className="px-4 py-3 text-left text-sm font-semibold">{header}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {rows?.map((row: any, rowIdx: number) => (
                <tr key={rowIdx} className="border-b last:border-0">
                  {row.map((cell: any, cellIdx: number) => (
                    <td key={cellIdx} className="px-4 py-3 text-sm">
                      {typeof cell === 'boolean' ? (cell ? '✓' : '✗') : cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  ),

  "a2ui.VsCard": ({ item_a, item_b, comparison_points }: any) => (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-base">{item_a.name}</CardTitle>
          <Badge variant="outline">VS</Badge>
          <CardTitle className="text-base">{item_b.name}</CardTitle>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {comparison_points?.map((point: any, idx: number) => (
            <div key={idx} className="grid grid-cols-3 gap-4 items-center">
              <div className="text-sm text-right">{point.value_a}</div>
              <div className="text-xs text-center text-muted-foreground font-medium">{point.metric}</div>
              <div className="text-sm">{point.value_b}</div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  ),

  "a2ui.FeatureMatrix": ({ features, products }: any) => (
    <Card>
      <CardContent className="p-0">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-muted">
              <tr>
                <th className="px-4 py-3 text-left text-sm font-semibold">Feature</th>
                {products?.map((product: string, idx: number) => (
                  <th key={idx} className="px-4 py-3 text-center text-sm font-semibold">{product}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {features?.map((feature: any, idx: number) => (
                <tr key={idx} className="border-b last:border-0">
                  <td className="px-4 py-3 text-sm font-medium">{feature.name}</td>
                  {feature.availability.map((avail: boolean, pIdx: number) => (
                    <td key={pIdx} className="px-4 py-3 text-center">
                      <span className={avail ? 'text-green-500' : 'text-red-500'}>
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
  ),

  "a2ui.PricingTable": ({ plans }: any) => (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {plans?.map((plan: any, idx: number) => (
        <Card key={idx} className={plan.highlighted ? 'border-primary border-2' : ''}>
          {plan.highlighted && (
            <div className="bg-primary text-primary-foreground text-center py-1 text-xs font-semibold">
              POPULAR
            </div>
          )}
          <CardHeader>
            <CardTitle className="text-base">{plan.name}</CardTitle>
            <div className="text-3xl font-bold">
              {plan.price}
              {plan.period && <span className="text-sm text-muted-foreground">/{plan.period}</span>}
            </div>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {plan.features?.map((feature: string, fIdx: number) => (
                <li key={fIdx} className="text-sm flex items-center gap-2">
                  <span className="text-primary">✓</span>
                  {feature}
                </li>
              ))}
            </ul>
          </CardContent>
          <CardFooter>
            <Button className="w-full" variant={plan.highlighted ? 'default' : 'outline'}>
              {plan.cta || 'Get Started'}
            </Button>
          </CardFooter>
        </Card>
      ))}
    </div>
  ),

  // ===== INSTRUCTIONAL COMPONENTS =====
  "a2ui.StepCard": ({ step_number, title, description, image_url, tips }: any) => (
    <Card>
      <CardHeader>
        <div className="flex items-start gap-3">
          <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground font-bold">
            {step_number}
          </div>
          <CardTitle className="text-base">{title}</CardTitle>
        </div>
      </CardHeader>
      {image_url && (
        <img src={image_url} alt={title} className="w-full h-48 object-cover" />
      )}
      <CardContent className="space-y-2">
        <p className="text-sm text-muted-foreground">{description}</p>
        {tips && tips.length > 0 && (
          <div className="mt-3 p-3 bg-blue-500/10 rounded-lg">
            <p className="text-xs font-semibold mb-1">Tips:</p>
            <ul className="space-y-1">
              {tips.map((tip: string, idx: number) => (
                <li key={idx} className="text-xs text-muted-foreground">• {tip}</li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  ),

  "a2ui.CodeBlock": ({ code, language, filename }: any) => (
    <Card>
      {filename && (
        <CardHeader className="pb-2">
          <CardDescription className="font-mono text-xs">{filename}</CardDescription>
        </CardHeader>
      )}
      <CardContent className="p-0">
        <pre className="p-4 overflow-x-auto bg-muted/50 rounded-b-lg">
          <code className={`text-sm language-${language || 'text'}`}>{code}</code>
        </pre>
      </CardContent>
    </Card>
  ),

  "a2ui.CalloutCard": ({ message, type, title, icon }: any) => {
    const colors = {
      info: 'bg-blue-500/10 border-blue-500',
      warning: 'bg-yellow-500/10 border-yellow-500',
      error: 'bg-red-500/10 border-red-500',
      success: 'bg-green-500/10 border-green-500',
    };
    const icons = {
      info: 'ℹ️',
      warning: '⚠️',
      error: '❌',
      success: '✅',
    };

    return (
      <Card className={colors[type as keyof typeof colors] || colors.info}>
        <CardContent className="pt-6">
          <div className="flex items-start gap-3">
            <span className="text-xl">{icon || icons[type as keyof typeof icons] || icons.info}</span>
            <div className="flex-1">
              {title && <div className="font-semibold mb-1">{title}</div>}
              <p className="text-sm">{message}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  },

  "a2ui.CommandCard": ({ command, description, platform, copy_button }: any) => (
    <Card>
      <CardContent className="pt-6">
        <div className="space-y-2">
          {description && <p className="text-sm text-muted-foreground">{description}</p>}
          <div className="flex items-center gap-2 bg-muted p-3 rounded-lg font-mono text-sm">
            {platform && <Badge variant="outline" className="text-xs">{platform}</Badge>}
            <code className="flex-1">{command}</code>
            {copy_button && (
              <Button size="sm" variant="ghost" onClick={() => navigator.clipboard.writeText(command)}>
                Copy
              </Button>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  ),

  // ===== LAYOUT COMPONENTS =====
  "a2ui.Section": ({ title, description }: any, childComponents?: React.ReactNode) => (
    <section className="space-y-4">
      {(title || description) && (
        <div className="space-y-1">
          {title && <h2 className="text-2xl font-bold">{title}</h2>}
          {description && <p className="text-muted-foreground">{description}</p>}
        </div>
      )}
      {childComponents && <div className="space-y-4">{childComponents}</div>}
    </section>
  ),

  "a2ui.Grid": ({ columns, gap }: any, childComponents?: React.ReactNode) => (
    <div
      className={`grid gap-${gap || 4}`}
      style={{ gridTemplateColumns: `repeat(${columns || 2}, minmax(0, 1fr))` }}
    >
      {childComponents}
    </div>
  ),

  "a2ui.Columns": ({ column_count }: any, childComponents?: React.ReactNode) => (
    <div className={`grid grid-cols-${column_count || 2} gap-4`}>
      {childComponents}
    </div>
  ),

  "a2ui.Tabs": ({ tabs }: any) => (
    <Tabs defaultValue={tabs?.[0]?.id || 'tab-0'}>
      <TabsList>
        {tabs?.map((tab: any) => (
          <TabsTrigger key={tab.id} value={tab.id}>
            {tab.label}
          </TabsTrigger>
        ))}
      </TabsList>
      {tabs?.map((tab: any) => (
        <TabsContent key={tab.id} value={tab.id}>
          <Card>
            <CardContent className="pt-6">
              {tab.content}
            </CardContent>
          </Card>
        </TabsContent>
      ))}
    </Tabs>
  ),

  "a2ui.Accordion": ({ items }: any) => (
    <Accordion type="single" collapsible>
      {items?.map((item: any, idx: number) => (
        <AccordionItem key={idx} value={`item-${idx}`}>
          <AccordionTrigger>{item.title}</AccordionTrigger>
          <AccordionContent>{item.content}</AccordionContent>
        </AccordionItem>
      ))}
    </Accordion>
  ),

  "a2ui.Carousel": ({ items }: any) => (
    <Card>
      <CardContent className="p-0">
        <div className="relative overflow-hidden">
          {items?.[0] && (
            <div className="p-6">
              {items[0].image_url && (
                <img src={items[0].image_url} alt={items[0].title} className="w-full h-64 object-cover rounded-lg mb-4" />
              )}
              <h3 className="font-semibold mb-2">{items[0].title}</h3>
              <p className="text-sm text-muted-foreground">{items[0].description}</p>
            </div>
          )}
          <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-2">
            {items?.map((_: any, idx: number) => (
              <div key={idx} className={`w-2 h-2 rounded-full ${idx === 0 ? 'bg-primary' : 'bg-muted'}`} />
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  ),

  "a2ui.Sidebar": ({ title, items, position }: any) => (
    <aside className={`w-64 p-4 bg-muted/30 rounded-lg ${position === 'right' ? 'ml-auto' : ''}`}>
      {title && <h3 className="font-semibold mb-3">{title}</h3>}
      <nav>
        <ul className="space-y-2">
          {items?.map((item: any, idx: number) => (
            <li key={idx}>
              <a href={item.url || '#'} className="text-sm hover:text-primary transition-colors">
                {item.label}
              </a>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  ),

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
