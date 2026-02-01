/**
 * Component Showcase Page
 *
 * A test page to display all A2UI components with sample data
 * to verify the dark blue theme styling.
 */

import { A2UIRenderer } from '@/components/A2UIRenderer';
import type { A2UIComponent } from '@/lib/a2ui-catalog';

const sampleComponents: A2UIComponent[] = [
  // Summary Components
  {
    type: 'a2ui.TLDR',
    id: 'tldr-1',
    props: {
      summary: 'This research explores the impact of AI on modern software development, finding that teams using AI tools are 40% more productive.',
      bullets: [
        'AI coding assistants reduce debugging time by 30%',
        'Code quality metrics improved by 25%',
        'Developer satisfaction increased significantly'
      ]
    }
  },
  {
    type: 'a2ui.KeyTakeaways',
    id: 'takeaways-1',
    props: {
      title: 'Key Takeaways',
      items: [
        'AI-assisted development is becoming mainstream',
        'Best results come from human-AI collaboration',
        'Training and onboarding are essential for adoption'
      ]
    }
  },

  // Data Components
  {
    type: 'a2ui.Section',
    id: 'data-section',
    props: {
      title: 'Key Metrics',
      subtitle: 'Performance indicators from Q4 2024'
    },
    children: [
      {
        type: 'a2ui.Grid',
        id: 'stats-grid',
        props: { columns: 3 },
        children: [
          {
            type: 'a2ui.StatCard',
            id: 'stat-1',
            props: {
              label: 'Total Users',
              value: '2.4M',
              trend: '+12%',
              icon: '👥'
            }
          },
          {
            type: 'a2ui.StatCard',
            id: 'stat-2',
            props: {
              label: 'Revenue',
              value: '$4.2M',
              trend: '+8%',
              icon: '💰'
            }
          },
          {
            type: 'a2ui.StatCard',
            id: 'stat-3',
            props: {
              label: 'Growth Rate',
              value: '156%',
              trend: '+24%',
              icon: '📈'
            }
          }
        ]
      }
    ]
  },

  // Progress and Charts
  {
    type: 'a2ui.Section',
    id: 'charts-section',
    props: {
      title: 'Progress Overview'
    },
    children: [
      {
        type: 'a2ui.Grid',
        id: 'charts-grid',
        props: { columns: 2 },
        children: [
          {
            type: 'a2ui.ProgressRing',
            id: 'progress-1',
            props: {
              percentage: 78,
              label: 'Project Completion'
            }
          },
          {
            type: 'a2ui.MiniChart',
            id: 'chart-1',
            props: {
              data: [12, 19, 15, 25, 22, 30, 28],
              label: 'Weekly Activity',
              type: 'bar'
            }
          }
        ]
      }
    ]
  },

  // Comparison Bar
  {
    type: 'a2ui.ComparisonBar',
    id: 'comparison-1',
    props: {
      label: 'Market Share Comparison',
      value_a: 65,
      value_b: 45,
      label_a: 'Our Product',
      label_b: 'Competitor'
    }
  },

  // Data Table
  {
    type: 'a2ui.DataTable',
    id: 'table-1',
    props: {
      headers: ['Feature', 'Status', 'Progress', 'Due Date'],
      rows: [
        ['Authentication', 'Complete', '100%', 'Jan 15'],
        ['Dashboard', 'In Progress', '75%', 'Feb 1'],
        ['API Integration', 'Pending', '30%', 'Feb 15'],
        ['Testing', 'Not Started', '0%', 'Mar 1']
      ],
      sortable: true,
      caption: 'Project Feature Status'
    }
  },

  // Lists
  {
    type: 'a2ui.Section',
    id: 'lists-section',
    props: {
      title: 'Top Technologies for 2025'
    },
    children: [
      {
        type: 'a2ui.RankedItem',
        id: 'rank-1',
        props: { rank: 1, label: 'AI/Machine Learning', description: 'Leading innovation across industries', score: 98 }
      },
      {
        type: 'a2ui.RankedItem',
        id: 'rank-2',
        props: { rank: 2, label: 'Cloud Computing', description: 'Essential infrastructure for modern apps', score: 95 }
      },
      {
        type: 'a2ui.RankedItem',
        id: 'rank-3',
        props: { rank: 3, label: 'Cybersecurity', description: 'Critical for data protection', score: 92 }
      }
    ]
  },

  // Checklist
  {
    type: 'a2ui.Section',
    id: 'checklist-section',
    props: {
      title: 'Implementation Checklist'
    },
    children: [
      {
        type: 'a2ui.ChecklistItem',
        id: 'check-1',
        props: { label: 'Set up development environment', checked: true }
      },
      {
        type: 'a2ui.ChecklistItem',
        id: 'check-2',
        props: { label: 'Configure CI/CD pipeline', checked: true }
      },
      {
        type: 'a2ui.ChecklistItem',
        id: 'check-3',
        props: { label: 'Deploy to staging', checked: false }
      },
      {
        type: 'a2ui.ChecklistItem',
        id: 'check-4',
        props: { label: 'Production release', checked: false }
      }
    ]
  },

  // Code Block
  {
    type: 'a2ui.CodeBlock',
    id: 'code-1',
    props: {
      code: `const greeting = (name: string) => {
  return \`Hello, \${name}!\`;
};

// Using the function
console.log(greeting("World"));`,
      language: 'typescript',
      title: 'Example Function'
    }
  },

  // Step Cards
  {
    type: 'a2ui.Section',
    id: 'steps-section',
    props: {
      title: 'Getting Started Guide'
    },
    children: [
      {
        type: 'a2ui.StepCard',
        id: 'step-1',
        props: { step: 1, title: 'Install Dependencies', description: 'Run npm install to set up the project', status: 'completed' }
      },
      {
        type: 'a2ui.StepCard',
        id: 'step-2',
        props: { step: 2, title: 'Configure Environment', description: 'Set up your .env file with API keys', status: 'active' }
      },
      {
        type: 'a2ui.StepCard',
        id: 'step-3',
        props: { step: 3, title: 'Run the Application', description: 'Start the development server', status: 'pending' }
      }
    ]
  },

  // Callout
  {
    type: 'a2ui.CalloutCard',
    id: 'callout-1',
    props: {
      type: 'info',
      title: 'Pro Tip',
      content: 'Use environment variables for all sensitive configuration values to keep your codebase secure.'
    }
  },

  // Command
  {
    type: 'a2ui.CommandCard',
    id: 'command-1',
    props: {
      command: 'npm run dev',
      description: 'Start the development server'
    }
  },

  // News/Headlines
  {
    type: 'a2ui.Section',
    id: 'news-section',
    props: {
      title: 'Latest News'
    },
    children: [
      {
        type: 'a2ui.HeadlineCard',
        id: 'headline-1',
        props: {
          title: 'AI Adoption Reaches New Heights in Enterprise',
          summary: 'Major corporations report significant ROI from AI implementations across operations.',
          source: 'Tech Weekly',
          published_at: '2025-01-30',
          sentiment: 'positive'
        }
      },
      {
        type: 'a2ui.HeadlineCard',
        id: 'headline-2',
        props: {
          title: 'New Framework Simplifies Cloud Development',
          summary: 'Open-source project gains traction among developers for its intuitive API design.',
          source: 'Dev News',
          published_at: '2025-01-29',
          sentiment: 'neutral'
        }
      }
    ]
  },

  // Quote
  {
    type: 'a2ui.QuoteCard',
    id: 'quote-1',
    props: {
      quote: 'The best way to predict the future is to create it.',
      author: 'Peter Drucker',
      title: 'Management Consultant',
      context: 'On innovation and leadership'
    }
  },

  // Expert Tip
  {
    type: 'a2ui.ExpertTip',
    id: 'tip-1',
    props: {
      tip: 'Always write tests before implementing new features. This approach, known as TDD, leads to more maintainable and reliable code.',
      expert: 'Jane Smith',
      title: 'Senior Software Engineer',
      category: 'Best Practices'
    }
  },

  // Comparison Table
  {
    type: 'a2ui.VsCard',
    id: 'vs-1',
    props: {
      title_a: 'React',
      title_b: 'Vue',
      metrics: [
        { label: 'Learning Curve', value_a: 'Moderate', value_b: 'Easy' },
        { label: 'Performance', value_a: 'Excellent', value_b: 'Excellent' },
        { label: 'Community', value_a: 'Massive', value_b: 'Large' },
        { label: 'Ecosystem', value_a: 'Extensive', value_b: 'Growing' }
      ]
    }
  },

  // Tags
  {
    type: 'a2ui.Section',
    id: 'tags-section',
    props: {
      title: 'Technology Tags'
    },
    children: [
      {
        type: 'a2ui.TagCloud',
        id: 'tags-1',
        props: {
          tags: [
            { name: 'React', count: 156 },
            { name: 'TypeScript', count: 142 },
            { name: 'Node.js', count: 98 },
            { name: 'Python', count: 87 },
            { name: 'Docker', count: 76 },
            { name: 'Kubernetes', count: 54 }
          ]
        }
      }
    ]
  },

  // Resources
  {
    type: 'a2ui.Section',
    id: 'resources-section',
    props: {
      title: 'Recommended Resources'
    },
    children: [
      {
        type: 'a2ui.Grid',
        id: 'resources-grid',
        props: { columns: 2 },
        children: [
          {
            type: 'a2ui.ToolCard',
            id: 'tool-1',
            props: {
              name: 'VS Code',
              description: 'Powerful code editor with extensive extensions',
              features: ['IntelliSense', 'Debugging', 'Git Integration'],
              url: 'https://code.visualstudio.com'
            }
          },
          {
            type: 'a2ui.RepoCard',
            id: 'repo-1',
            props: {
              name: 'awesome-react',
              description: 'A collection of awesome things regarding React ecosystem',
              stars: 58000,
              forks: 7200,
              language: 'JavaScript'
            }
          }
        ]
      }
    ]
  }
];

export function ComponentShowcase() {
  return (
    <div className="min-h-screen bg-background text-foreground p-8">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-white to-blue-200 bg-clip-text text-transparent mb-2">
            Component Showcase
          </h1>
          <p className="text-muted-foreground">
            Preview all A2UI components with the dark blue theme
          </p>
        </header>

        <div className="space-y-8">
          {sampleComponents.map((component) => (
            <A2UIRenderer key={component.id} component={component} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default ComponentShowcase;
