/**
 * Accordion Component
 *
 * Expandable sections using Shadcn Accordion component.
 * Supports single or multiple open items with smooth animations.
 */

import React from 'react';
import {
  Accordion as ShadcnAccordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { cn } from "@/lib/utils";

export interface AccordionItemData {
  /** Display label for the accordion item */
  label: string;

  /** Content to display when item is expanded */
  content: React.ReactNode;
}

export interface AccordionProps {
  /** Array of accordion items */
  items: AccordionItemData[];

  /** Allow multiple items to be open simultaneously */
  multiple?: boolean;

  /** Allow all items to be closed (no default open item) */
  allowEmpty?: boolean;

  /** Additional CSS classes */
  className?: string;
}

/**
 * Accordion Component
 *
 * Expandable sections with smooth animations.
 * Built on Shadcn UI Accordion for accessibility.
 */
export function Accordion({
  items,
  multiple = false,
  allowEmpty = true,
  className,
}: AccordionProps): React.ReactElement {
  // Shadcn Accordion uses "type" prop: "single" or "multiple"
  // For "single" type, we can use "collapsible" to allow all items to be closed
  return (
    <ShadcnAccordion
      type={multiple ? "multiple" : "single"}
      collapsible={allowEmpty}
      className={cn('bg-slate-900/30 rounded-lg border border-blue-500/20', className)}
    >
      {items.map((item, index) => (
        <AccordionItem
          key={index}
          value={`item-${index}`}
          className="border-b border-blue-500/10 last:border-0"
        >
          <AccordionTrigger className="px-4 text-white hover:text-blue-200 hover:no-underline hover:bg-blue-500/10 transition-colors [&>svg]:text-blue-400">
            {item.label}
          </AccordionTrigger>
          <AccordionContent className="px-4 text-blue-100/80">
            {item.content}
          </AccordionContent>
        </AccordionItem>
      ))}
    </ShadcnAccordion>
  );
}

export default Accordion;
