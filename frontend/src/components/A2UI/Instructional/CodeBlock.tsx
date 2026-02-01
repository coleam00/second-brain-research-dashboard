/**
 * CodeBlock Component
 *
 * Displays code with syntax highlighting, optional title, copy button, and language badge.
 * Uses CSS-based syntax highlighting with language-specific classes.
 */

import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export interface CodeBlockProps {
  /** Code content to display */
  code: string;

  /** Programming language (e.g., 'javascript', 'python', 'typescript') */
  language: string;

  /** Optional title/filename for the code block */
  title?: string;

  /** Whether to show copy button (defaults to true) */
  copyable?: boolean;
}

/**
 * CodeBlock Component
 *
 * A card component for displaying code snippets with syntax highlighting,
 * language indicator, and copy-to-clipboard functionality.
 */
export function CodeBlock({
  code,
  language,
  title,
  copyable = true,
}: CodeBlockProps): React.ReactElement {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  return (
    <Card className="bg-gradient-to-br from-card to-secondary/30 dark:border-blue-500/20">
      {(title || copyable) && (
        <CardHeader className="pb-2 flex flex-row items-center justify-between space-y-0">
          <div className="flex items-center gap-2">
            {title && (
              <CardDescription className="font-mono text-xs text-blue-300">
                {title}
              </CardDescription>
            )}
            <Badge variant="outline" className="text-xs bg-blue-500/20 border-blue-500/30 text-blue-300">
              {language}
            </Badge>
          </div>
          {copyable && (
            <Button
              size="sm"
              variant="ghost"
              onClick={handleCopy}
              className="h-8 px-2 text-xs text-blue-300 hover:text-blue-200 hover:bg-blue-500/20"
            >
              {copied ? '✓ Copied' : 'Copy'}
            </Button>
          )}
        </CardHeader>
      )}
      <CardContent className="p-0">
        <pre className="p-4 overflow-x-auto bg-slate-950/90 dark:bg-[#1e1e2e] rounded-b-lg m-0">
          <code className={`text-sm font-mono language-${language} text-slate-100`}>
            {code}
          </code>
        </pre>
      </CardContent>
    </Card>
  );
}

export default CodeBlock;
