/**
 * CommandCard Component
 *
 * Displays terminal/shell commands with copy functionality and optional command prefix.
 * Ideal for displaying CLI commands, shell scripts, and terminal operations.
 */

import React, { useState } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export interface CommandCardProps {
  /** Command to display */
  command: string;

  /** Optional language/platform (e.g., 'bash', 'powershell', 'cmd') */
  language?: string;

  /** Optional description of what the command does */
  description?: string;

  /** Whether to show copy button (defaults to true) */
  copyable?: boolean;
}

/**
 * CommandCard Component
 *
 * A card component for displaying terminal commands with copy-to-clipboard
 * functionality and platform/language indicators.
 */
export function CommandCard({
  command,
  language,
  description,
  copyable = true,
}: CommandCardProps): React.ReactElement {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(command);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy command:', err);
    }
  };

  const getCommandPrefix = () => {
    if (!language) return '$';
    if (language.toLowerCase() === 'powershell') return '>';
    if (language.toLowerCase() === 'cmd') return '>';
    if (language.toLowerCase() === 'bash' || language.toLowerCase() === 'sh') return '$';
    return '$';
  };

  return (
    <Card className="bg-gradient-to-br from-card to-secondary/30 dark:border-blue-500/20">
      <CardContent className="pt-6 space-y-3">
        {description && (
          <p className="text-sm text-blue-300">{description}</p>
        )}
        <div className="flex items-center gap-2 bg-slate-950/90 dark:bg-[#1e1e2e] p-4 rounded-lg border border-blue-500/20">
          <div className="flex items-center gap-2 flex-1 overflow-x-auto">
            {language && (
              <Badge variant="outline" className="text-xs shrink-0 bg-blue-500/20 border-blue-500/30 text-blue-300">
                {language}
              </Badge>
            )}
            <code className="font-mono text-sm flex-1 text-slate-100">
              <span className="text-blue-400 select-none">{getCommandPrefix()}</span>{' '}
              {command}
            </code>
          </div>
          {copyable && (
            <Button
              size="sm"
              variant="ghost"
              onClick={handleCopy}
              className="shrink-0 text-blue-300 hover:text-blue-200 hover:bg-blue-500/20"
            >
              {copied ? '✓ Copied' : 'Copy'}
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

export default CommandCard;
