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
    <Card className="dark:bg-slate-900/50 dark:border-slate-700">
      <CardContent className="pt-6 space-y-3">
        {description && (
          <p className="text-sm text-muted-foreground dark:text-slate-400">{description}</p>
        )}
        <div className="flex items-center gap-2 bg-muted dark:bg-slate-950/50 p-4 rounded-lg border dark:border-slate-700">
          <div className="flex items-center gap-2 flex-1 overflow-x-auto">
            {language && (
              <Badge variant="outline" className="text-xs shrink-0 dark:border-slate-600 dark:text-slate-400">
                {language}
              </Badge>
            )}
            <code className="font-mono text-sm flex-1 dark:text-slate-300">
              <span className="text-muted-foreground dark:text-slate-500 select-none">{getCommandPrefix()}</span>{' '}
              {command}
            </code>
          </div>
          {copyable && (
            <Button
              size="sm"
              variant="ghost"
              onClick={handleCopy}
              className="shrink-0 dark:hover:bg-slate-800"
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
