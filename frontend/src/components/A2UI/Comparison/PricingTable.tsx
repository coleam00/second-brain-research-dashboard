/**
 * PricingTable Component
 *
 * Pricing tier comparison table with multiple plans.
 * Supports highlighting recommended/popular plans and customizable CTAs.
 */

import React from 'react';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

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
          {title && <h2 className="text-2xl font-bold text-white">{title}</h2>}
          {subtitle && <p className="text-blue-200">{subtitle}</p>}
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
            className={`relative bg-gradient-to-br from-card to-secondary/30 ${
              plan.highlighted
                ? 'border-blue-500 border-2 shadow-lg shadow-blue-500/20'
                : 'border-blue-500/20'
            }`}
          >
            {(plan.highlighted || plan.badge) && (
              <div className="bg-blue-600 text-white text-center py-1 text-xs font-semibold rounded-t-lg">
                {plan.badge || 'POPULAR'}
              </div>
            )}

            <CardHeader className="pb-4">
              <CardTitle className="text-base text-white">
                {plan.name}
              </CardTitle>
              {plan.description && (
                <p className="text-sm text-blue-200 mt-1">
                  {plan.description}
                </p>
              )}
              <div className="text-3xl font-bold text-white mt-2">
                {typeof plan.price === 'number' ? (
                  <>
                    {plan.currency || currency}
                    {plan.price}
                  </>
                ) : (
                  plan.price
                )}
                {plan.period && (
                  <span className="text-sm text-blue-300 font-normal">
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
                    className="text-sm flex items-start gap-2 text-slate-200"
                  >
                    <span className="text-blue-400 mt-0.5">✓</span>
                    <span>{feature}</span>
                  </li>
                ))}
              </ul>
            </CardContent>

            <CardFooter className="pt-4">
              <Button
                className={`w-full ${
                  plan.highlighted
                    ? 'bg-blue-600 hover:bg-blue-700 text-white'
                    : 'bg-slate-800 hover:bg-slate-700 text-blue-200 border border-blue-500/30'
                }`}
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
