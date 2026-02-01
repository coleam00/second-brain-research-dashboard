/**
 * ProfileCard Component
 *
 * Displays user profile information with avatar, name, title, bio, and social links.
 * Supports circular avatar with border and up to 5 social links.
 */

import React from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export interface SocialLink {
  /** Platform name (e.g., "Twitter", "LinkedIn", "GitHub") */
  platform: string;

  /** URL to the social profile */
  url: string;
}

export interface ProfileCardProps {
  /** User's full name */
  name: string;

  /** Job title or role */
  title?: string;

  /** Short biography or description */
  bio?: string;

  /** Avatar image URL */
  avatar_url?: string;

  /** Company name */
  company?: string;

  /** Location */
  location?: string;

  /** List of social links (max 5) */
  social_links?: SocialLink[];
}

/**
 * ProfileCard Component
 *
 * A card component for displaying user profile information with avatar,
 * name, title, bio, and social media links.
 */
export function ProfileCard({
  name,
  title,
  bio,
  avatar_url,
  company,
  location,
  social_links,
}: ProfileCardProps): React.ReactElement {
  // Limit social links to maximum 5
  const displayedLinks = social_links?.slice(0, 5) || [];

  return (
    <Card className="group cursor-default bg-gradient-to-br from-card to-secondary/30 border-blue-500/20">
      <CardHeader>
        <div className="flex items-start gap-4">
          {avatar_url ? (
            <div className="overflow-hidden rounded-full border-2 border-blue-500/40 transition-all duration-300 group-hover:border-blue-400/60 group-hover:shadow-lg group-hover:shadow-blue-500/20">
              <img
                src={avatar_url}
                alt={name}
                className="w-16 h-16 object-cover transition-transform duration-300 group-hover:scale-110"
              />
            </div>
          ) : (
            <div className="w-16 h-16 rounded-full border-2 border-blue-500/40 bg-blue-950/50 flex items-center justify-center transition-all duration-300 group-hover:border-blue-400/60 group-hover:shadow-lg group-hover:shadow-blue-500/20">
              <span className="text-2xl font-bold text-blue-200">
                {name.charAt(0).toUpperCase()}
              </span>
            </div>
          )}
          <div className="flex-1">
            <CardTitle className="text-base text-white">{name}</CardTitle>
            <CardDescription className="text-blue-300">
              {title}
              {company && ` at ${company}`}
              {location && ` • ${location}`}
            </CardDescription>
          </div>
        </div>
      </CardHeader>
      {bio && (
        <CardContent>
          <p className="text-sm text-slate-200">{bio}</p>
        </CardContent>
      )}
      {displayedLinks.length > 0 && (
        <CardFooter className="flex gap-2 flex-wrap">
          {displayedLinks.map((link, idx) => (
            <Button
              key={idx}
              asChild
              variant="outline"
              size="sm"
              className="border-blue-500/30 text-blue-300 hover:bg-blue-500/10 hover:text-blue-200 hover:border-blue-400/50"
            >
              <a href={link.url} target="_blank" rel="noopener noreferrer">
                {link.platform}
              </a>
            </Button>
          ))}
        </CardFooter>
      )}
    </Card>
  );
}

export default ProfileCard;
