/**
 * CompanyCard Component
 *
 * Displays company information with logo, name, description, and metrics
 * (employees, founded year, industry).
 */

import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

export interface CompanyCardProps {
  /** Company name */
  name: string;

  /** Company description */
  description?: string;

  /** Industry or sector */
  industry?: string;

  /** Company size (number of employees or range) */
  size?: string;

  /** Company logo URL or text fallback */
  logo_url?: string;

  /** Year founded */
  founded?: string | number;

  /** Company location */
  location?: string;

  /** Company website URL */
  url?: string;
}

/**
 * CompanyCard Component
 *
 * A card component for displaying company information with logo,
 * name, description, and key metrics.
 */
export function CompanyCard({
  name,
  description,
  industry,
  size,
  logo_url,
  founded,
  location,
  url,
}: CompanyCardProps): React.ReactElement {
  return (
    <Card className="bg-gradient-to-br from-card to-secondary/30 border-blue-500/20">
      <CardHeader>
        <div className="flex items-start gap-3">
          {logo_url ? (
            <img
              src={logo_url}
              alt={name}
              className="w-12 h-12 rounded object-contain bg-blue-950/30 p-1 border border-blue-500/20"
            />
          ) : (
            <div className="w-12 h-12 rounded bg-blue-950/50 border border-blue-500/20 flex items-center justify-center">
              <span className="text-lg font-bold text-blue-300">
                {name.substring(0, 2).toUpperCase()}
              </span>
            </div>
          )}
          <div className="flex-1">
            <CardTitle className="text-base text-white">{name}</CardTitle>
            <CardDescription className="text-blue-300 flex flex-wrap gap-1 items-center">
              {industry && <span>{industry}</span>}
              {size && industry && <span>•</span>}
              {size && <span>{size} employees</span>}
              {location && (industry || size) && <span>•</span>}
              {location && <span>{location}</span>}
            </CardDescription>
          </div>
        </div>
      </CardHeader>
      {description && (
        <CardContent className="space-y-2">
          <p className="text-sm text-slate-200">{description}</p>
          {founded && (
            <div className="flex gap-2">
              <Badge variant="secondary" className="bg-blue-950/50 text-blue-200 border border-blue-500/30">
                Founded {founded}
              </Badge>
            </div>
          )}
        </CardContent>
      )}
      {url && (
        <CardFooter>
          <Button
            asChild
            variant="outline"
            className="w-full border-blue-500/30 text-blue-300 hover:bg-blue-500/10 hover:text-blue-200 hover:border-blue-400/50"
          >
            <a href={url} target="_blank" rel="noopener noreferrer">
              Visit Website
            </a>
          </Button>
        </CardFooter>
      )}
    </Card>
  );
}

export default CompanyCard;
