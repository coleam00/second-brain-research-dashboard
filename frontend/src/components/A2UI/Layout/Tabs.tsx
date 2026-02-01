/**
 * Tabs Component
 *
 * A tabbed interface using Shadcn Tabs component.
 * Supports keyboard navigation (arrow keys) and customizable tab content.
 */

import React from 'react';
import { Tabs as ShadcnTabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent } from "@/components/ui/card";

export interface TabItem {
  /** Unique identifier for the tab */
  id: string;

  /** Display label for the tab */
  label: string;

  /** Content to display when tab is active */
  content: React.ReactNode;
}

export interface TabsProps {
  /** Array of tab items */
  tabs: TabItem[];

  /** Index of the default active tab (0-based) */
  defaultTab?: number;

  /** Additional CSS classes */
  className?: string;
}

/**
 * Tabs Component
 *
 * Tabbed interface with keyboard navigation support.
 * Built on Shadcn UI Tabs component for accessibility.
 */
export function Tabs({
  tabs,
  defaultTab = 0,
  className,
}: TabsProps): React.ReactElement {
  const defaultValue = tabs[defaultTab]?.id || tabs[0]?.id || 'tab-0';

  return (
    <ShadcnTabs defaultValue={defaultValue} className={className}>
      <TabsList className="w-full justify-start bg-slate-900/50 border border-blue-500/20 p-1">
        {tabs.map((tab) => (
          <TabsTrigger
            key={tab.id}
            value={tab.id}
            className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-600 data-[state=active]:to-blue-500 data-[state=active]:text-white data-[state=active]:shadow-lg data-[state=active]:shadow-blue-500/20 data-[state=inactive]:text-blue-200/60 hover:text-blue-100 transition-all"
          >
            {tab.label}
          </TabsTrigger>
        ))}
      </TabsList>
      {tabs.map((tab) => (
        <TabsContent key={tab.id} value={tab.id}>
          <Card className="bg-gradient-to-br from-card to-secondary/30 border-blue-500/20">
            <CardContent className="pt-6">
              {tab.content}
            </CardContent>
          </Card>
        </TabsContent>
      ))}
    </ShadcnTabs>
  );
}

export default Tabs;
