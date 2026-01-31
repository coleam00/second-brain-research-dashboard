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
      className={className}
    >
      {items.map((item, index) => (
        <AccordionItem key={index} value={`item-${index}`}>
          <AccordionTrigger>{item.label}</AccordionTrigger>
          <AccordionContent>{item.content}</AccordionContent>
        </AccordionItem>
      ))}
    </ShadcnAccordion>
  );
}

export default Accordion;
