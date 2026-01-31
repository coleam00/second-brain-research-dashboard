/**
 * DYN-213 Resource Components Test Page
 * Tests all 4 resource components: LinkCard, ToolCard, BookCard, RepoCard
 */

import { LinkCard } from '@/components/A2UI/Resources/LinkCard';
import { ToolCard } from '@/components/A2UI/Resources/ToolCard';
import { BookCard } from '@/components/A2UI/Resources/BookCard';
import { RepoCard } from '@/components/A2UI/Resources/RepoCard';

export function ResourceTest() {
  return (
    <div className="min-h-screen bg-background p-8">
      <h1 className="text-4xl font-bold mb-8">DYN-213: Resource Components Test</h1>

      {/* LinkCard Tests */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-4">LinkCard Component</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <LinkCard
            title="OpenAI Documentation"
            url="https://platform.openai.com/docs"
            description="Official OpenAI API documentation and guides"
            domain="platform.openai.com"
          />
          <LinkCard
            title="React Official Tutorial"
            url="https://react.dev/learn"
            description="Learn React from the official documentation"
            domain="react.dev"
          />
          <LinkCard
            title="MDN Web Docs"
            url="https://developer.mozilla.org"
            description="Resources for developers, by developers"
            domain="developer.mozilla.org"
          />
        </div>
      </section>

      {/* ToolCard Tests */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-4">ToolCard Component</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <ToolCard
            name="VS Code"
            description="Free, open-source code editor from Microsoft with excellent extension support"
            rating={5}
            category="Code Editor"
            pricing="Free"
            url="https://code.visualstudio.com"
          />
          <ToolCard
            name="Figma"
            description="Collaborative interface design tool used by design teams worldwide"
            rating={4}
            category="Design Tool"
            pricing="Freemium"
            url="https://figma.com"
          />
          <ToolCard
            name="Notion"
            description="All-in-one workspace for notes, databases, and project management"
            rating={5}
            category="Productivity"
            pricing="Freemium"
            url="https://notion.so"
          />
        </div>
      </section>

      {/* BookCard Tests */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-4">BookCard Component</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <BookCard
            title="The Pragmatic Programmer"
            author="David Thomas, Andrew Hunt"
            coverImage="https://m.media-amazon.com/images/I/71VvgaXvHoL._SY466_.jpg"
            rating={5}
            year={2019}
            description="Your journey to mastery in software development and programming best practices"
            url="https://pragprog.com"
          />
          <BookCard
            title="Clean Code"
            author="Robert C. Martin"
            coverImage="https://m.media-amazon.com/images/I/51E2055ZGUL._SY466_.jpg"
            rating={5}
            year={2008}
            description="A handbook of agile software craftsmanship with principles and practices"
            url="https://www.amazon.com"
          />
          <BookCard
            title="Designing Data-Intensive Applications"
            author="Martin Kleppmann"
            coverImage="https://m.media-amazon.com/images/I/71u2EcdLvIL._SY466_.jpg"
            rating={5}
            year={2017}
            description="The big ideas behind reliable, scalable, and maintainable systems"
            url="https://dataintensive.net"
          />
        </div>
      </section>

      {/* RepoCard Tests */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold mb-4">RepoCard Component</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <RepoCard
            name="react"
            owner="facebook"
            url="https://github.com/facebook/react"
            description="The library for web and native user interfaces"
            language="JavaScript"
            stars={231000}
            forks={47200}
          />
          <RepoCard
            name="typescript"
            owner="microsoft"
            url="https://github.com/microsoft/typescript"
            description="TypeScript is a superset of JavaScript that compiles to clean JavaScript output"
            language="TypeScript"
            stars={102000}
            forks={12300}
          />
          <RepoCard
            name="vite"
            owner="vitejs"
            url="https://github.com/vitejs/vite"
            description="Next generation frontend tooling. It's fast!"
            language="TypeScript"
            stars={69500}
            forks={6250}
          />
        </div>
      </section>
    </div>
  );
}

export default ResourceTest;
