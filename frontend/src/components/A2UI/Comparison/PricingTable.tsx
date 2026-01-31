/**
 * PricingTable Component
 *
 * Pricing tier comparison table with multiple plans.
 * Supports highlighting recommended/popular plans and customizable CTAs.
 */

import React from 'react';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export interface PricingPlan {
  /** Plan name (e.g., "Basic", "Pro", "Enterprise") */
  name: string;

  /** Price (can be number or string like "$9.99" or "Free") */
  price: string | number;

  /** Billing period (e.g., "month", "year") */
  period?: string;

  /** Array of feature descriptions */
  features: string[];

  /** Whether this plan is highlighted/recommended */
  highlighted?: boolean;

  /** Custom badge text (e.g., "POPULAR", "BEST VALUE") */
  badge?: string;

  /** Call-to-action button text */
  cta?: string;

  /** Optional plan description */
  description?: string;

  /** Optional currency symbol */
  currency?: string;
}

export interface PricingTableProps {
  /** Array of pricing tiers/plans */
  tiers?: PricingPlan[];
  plans?: PricingPlan[];

  /** Default currency symbol (overridden by per-plan currency) */
  currency?: string;

  /** Optional title */
  title?: string;

  /** Optional subtitle */
  subtitle?: string;

  /** Number of columns (default: auto-responsive) */
  columns?: number;
}

/**
 * PricingTable Component
 *
 * Displays multiple pricing plans in a responsive grid layout.
 * Highlights recommended plans and includes feature lists and CTAs.
 */
export function PricingTable({
  tiers,
  plans,
  currency = '$',
  title,
  subtitle,
  columns,
}: PricingTableProps): React.ReactElement {
  // Support both 'tiers' and 'plans' prop names
  const pricingPlans = tiers || plans || [];

  return (
    <div className="space-y-4">
      {(title || subtitle) && (
        <div className="text-center space-y-2">
          {title && <h2 className="text-2xl font-bold dark:text-slate-100">{title}</h2>}
          {subtitle && <p className="text-muted-foreground dark:text-slate-400">{subtitle}</p>}
        </div>
      )}

      <div
        className={`grid gap-4 ${
          columns
            ? `grid-cols-1 md:grid-cols-${columns}`
            : `grid-cols-1 md:grid-cols-${Math.min(pricingPlans.length, 3)}`
        }`}
        style={
          !columns
            ? { gridTemplateColumns: `repeat(auto-fit, minmax(280px, 1fr))` }
            : undefined
        }
      >
        {pricingPlans.map((plan: PricingPlan, idx: number) => (
          <Card
            key={idx}
            className={`relative dark:bg-slate-900 ${
              plan.highlighted
                ? 'border-primary border-2 shadow-lg dark:border-primary dark:shadow-primary/20'
                : 'dark:border-slate-700'
            }`}
          >
            {(plan.highlighted || plan.badge) && (
              <div className="bg-primary text-primary-foreground text-center py-1 text-xs font-semibold rounded-t-lg">
                {plan.badge || 'POPULAR'}
              </div>
            )}

            <CardHeader className="pb-4">
              <CardTitle className="text-base dark:text-slate-100">
                {plan.name}
              </CardTitle>
              {plan.description && (
                <p className="text-sm text-muted-foreground dark:text-slate-400 mt-1">
                  {plan.description}
                </p>
              )}
              <div className="text-3xl font-bold dark:text-slate-100 mt-2">
                {typeof plan.price === 'number' ? (
                  <>
                    {plan.currency || currency}
                    {plan.price}
                  </>
                ) : (
                  plan.price
                )}
                {plan.period && (
                  <span className="text-sm text-muted-foreground dark:text-slate-400 font-normal">
                    /{plan.period}
                  </span>
                )}
              </div>
            </CardHeader>

            <CardContent className="flex-1">
              <ul className="space-y-2">
                {plan.features?.map((feature: string, fIdx: number) => (
                  <li
                    key={fIdx}
                    className="text-sm flex items-start gap-2 dark:text-slate-300"
                  >
                    <span className="text-primary dark:text-primary/80 mt-0.5">✓</span>
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
            </CardContent>

            <CardFooter className="pt-4">
              <Button
                className="w-full"
                variant={plan.highlighted ? 'default' : 'outline'}
              >
                {plan.cta || 'Get Started'}
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
}

export default PricingTable;
