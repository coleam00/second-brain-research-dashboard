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
      <TabsList className="w-full justify-start">
        {tabs.map((tab) => (
          <TabsTrigger key={tab.id} value={tab.id}>
            {tab.label}
          </TabsTrigger>
        ))}
      </TabsList>
      {tabs.map((tab) => (
        <TabsContent key={tab.id} value={tab.id}>
          <Card>
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
