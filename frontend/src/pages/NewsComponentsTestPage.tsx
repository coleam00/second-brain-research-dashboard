/**
 * News Components Test Page
 *
 * Test page for verifying all news-related A2UI components
 * render correctly with proper styling and props.
 */

import { A2UIRendererList } from '@/components/A2UIRenderer';
import type { A2UIComponent } from '@/lib/a2ui-catalog';

// Test data for news components
const newsTestComponents: A2UIComponent[] = [
  // HeadlineCard - Positive sentiment with image
  {
    id: 'headline-1',
    type: 'a2ui.HeadlineCard',
    props: {
      title: 'AI Research Breakthrough Announced at Stanford',
      summary: 'Researchers have developed a new approach to natural language understanding that significantly improves model performance on complex reasoning tasks.',
      source: 'TechCrunch',
      published_at: new Date().toISOString(),
      sentiment: 'positive',
      image_url: 'https://via.placeholder.com/800x400/1e293b/cbd5e1?text=AI+Research+News',
    },
  },

  // HeadlineCard - Negative sentiment without image
  {
    id: 'headline-2',
    type: 'a2ui.HeadlineCard',
    props: {
      title: 'Major Tech Company Announces Layoffs',
      summary: 'In response to economic pressures, the company will reduce workforce by 15% across multiple departments.',
      source: 'Reuters',
      published_at: '2026-01-29T10:30:00Z',
      sentiment: 'negative',
    },
  },

  // HeadlineCard - Neutral sentiment
  {
    id: 'headline-3',
    type: 'a2ui.HeadlineCard',
    props: {
      title: 'New JavaScript Framework Released',
      summary: 'The latest version includes improved TypeScript support and better performance optimizations.',
      source: 'Dev.to',
      published_at: '2026-01-28T14:00:00Z',
      sentiment: 'neutral',
    },
  },

  // TrendIndicator - Up trend
  {
    id: 'trend-1',
    type: 'a2ui.TrendIndicator',
    props: {
      metric: 'Daily Active Users',
      value: '45.2K',
      change: '+12.5%',
      trend: 'up',
      period: 'Last 7 days',
    },
  },

  // TrendIndicator - Down trend
  {
    id: 'trend-2',
    type: 'a2ui.TrendIndicator',
    props: {
      metric: 'Server Response Time',
      value: '245ms',
      change: '-8.3%',
      trend: 'down',
      period: 'This week',
    },
  },

  // TrendIndicator - Stable trend
  {
    id: 'trend-3',
    type: 'a2ui.TrendIndicator',
    props: {
      metric: 'Monthly Revenue',
      value: '$125K',
      change: '+0.5%',
      trend: 'stable',
    },
  },

  // TimelineEvent examples
  {
    id: 'timeline-1',
    type: 'a2ui.TimelineEvent',
    props: {
      timestamp: '2026-01-30T09:00:00Z',
      title: 'Project Kickoff Meeting',
      description: 'Initial team meeting to discuss project scope, timeline, and resource allocation.',
      category: 'Meeting',
      status: 'completed',
    },
  },

  {
    id: 'timeline-2',
    type: 'a2ui.TimelineEvent',
    props: {
      timestamp: '2026-01-30T14:30:00Z',
      title: 'Design Review',
      description: 'Stakeholder review of the proposed UI/UX designs and component architecture.',
      category: 'Review',
      status: 'in-progress',
    },
  },

  {
    id: 'timeline-3',
    type: 'a2ui.TimelineEvent',
    props: {
      timestamp: '2026-01-31T10:00:00Z',
      title: 'Code Deployment',
      description: 'Deploy the latest features to the production environment with zero downtime.',
      category: 'Deployment',
    },
  },

  // NewsTicker
  {
    id: 'ticker-1',
    type: 'a2ui.NewsTicker',
    props: {
      items: [
        {
          source: 'BBC',
          headline: 'Global markets reach record highs',
        },
        {
          source: 'CNN',
          headline: 'New climate agreement signed by 50 nations',
        },
        {
          source: 'TechCrunch',
          headline: 'Startup raises $100M in Series B funding',
        },
        {
          source: 'The Verge',
          headline: 'Apple announces new product lineup',
        },
        {
          source: 'Wired',
          headline: 'Quantum computing breakthrough demonstrated',
        },
      ],
    },
  },
];

export default function NewsComponentsTestPage() {
  return (
    <div className="min-h-screen bg-background text-foreground p-8">
      <div className="max-w-5xl mx-auto space-y-8">
        <div>
          <h1 className="text-4xl font-bold mb-2">News Components Test</h1>
          <p className="text-muted-foreground">
            Testing all 4 news-type A2UI components: HeadlineCard, TrendIndicator, TimelineEvent, and NewsTicker
          </p>
        </div>

        <div className="space-y-6">
          <section>
            <h2 className="text-2xl font-bold mb-4">HeadlineCard Components</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <A2UIRendererList
                components={newsTestComponents.filter((c) => c.type === 'a2ui.HeadlineCard')}
                spacing="md"
              />
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">TrendIndicator Components</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <A2UIRendererList
                components={newsTestComponents.filter((c) => c.type === 'a2ui.TrendIndicator')}
                spacing="md"
              />
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">TimelineEvent Components</h2>
            <div className="max-w-2xl">
              <A2UIRendererList
                components={newsTestComponents.filter((c) => c.type === 'a2ui.TimelineEvent')}
                spacing="none"
              />
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-bold mb-4">NewsTicker Component</h2>
            <A2UIRendererList
              components={newsTestComponents.filter((c) => c.type === 'a2ui.NewsTicker')}
              spacing="md"
            />
          </section>
        </div>
      </div>
    </div>
  );
}
