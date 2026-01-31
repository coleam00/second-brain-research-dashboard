/**
 * Media Components Test Page (DYN-210)
 *
 * Standalone page to test all 4 media components:
 * - VideoCard
 * - ImageCard
 * - PlaylistCard
 * - PodcastCard
 */

import { VideoCard, ImageCard, PlaylistCard, PodcastCard } from '@/components/A2UI/Media';

export function MediaComponentsTest() {
  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-7xl mx-auto">
        <header className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Media Components Test - DYN-210</h1>
          <p className="text-muted-foreground">
            Testing VideoCard, ImageCard, PlaylistCard, and PodcastCard components
          </p>
        </header>

        <div className="space-y-12">
          {/* VideoCard Section */}
          <section>
            <h2 className="text-2xl font-semibold mb-4">VideoCard Component</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <VideoCard
                title="Introduction to React"
                description="Learn the basics of React in this comprehensive tutorial covering components, hooks, and state management"
                thumbnail_url="https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=400"
                duration="15:30"
                platform="YouTube"
                url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
              />
              <VideoCard
                title="Advanced TypeScript Patterns"
                description="Deep dive into TypeScript generics, utility types, and advanced patterns"
                thumbnail_url="https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=400"
                duration="45:20"
                platform="YouTube"
                youtube_id="dQw4w9WgXcQ"
                embed={false}
              />
            </div>
          </section>

          {/* ImageCard Section */}
          <section>
            <h2 className="text-2xl font-semibold mb-4">ImageCard Component</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <ImageCard
                title="Beautiful Sunset"
                description="A stunning sunset over the mountains"
                image_url="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600"
                alt_text="Mountain sunset"
                source="Unsplash"
                url="https://unsplash.com/photos/mountain-sunset"
              />
              <ImageCard
                title="Ocean Waves"
                description="Peaceful ocean waves at dawn"
                image_url="https://images.unsplash.com/photo-1505142468610-359e7d316be0?w=600"
                alt_text="Ocean waves"
                source="Unsplash"
              />
              <ImageCard
                image_url="https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=600"
                alt_text="Forest path"
              />
            </div>
          </section>

          {/* PlaylistCard Section */}
          <section>
            <h2 className="text-2xl font-semibold mb-4">PlaylistCard Component</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <PlaylistCard
                title="Web Development Tutorials"
                description="Complete playlist for learning web development from scratch"
                item_count={25}
                thumbnail_url="https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=400"
                platform="YouTube"
                creator="Tech Academy"
                total_duration="12h 30m"
                url="https://www.youtube.com/playlist?list=example"
              />
              <PlaylistCard
                title="JavaScript Best Practices"
                description="Learn modern JavaScript patterns and best practices"
                item_count={18}
                thumbnail_url="https://images.unsplash.com/photo-1579468118864-1b9ea3c0db4a?w=400"
                platform="YouTube"
                creator="Code Masters"
                total_duration="8h 45m"
              />
            </div>
          </section>

          {/* PodcastCard Section */}
          <section>
            <h2 className="text-2xl font-semibold mb-4">PodcastCard Component</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <PodcastCard
                title="The Future of AI"
                description="Exploring the latest developments in artificial intelligence and machine learning"
                host="Tech Talks"
                episode_number={42}
                duration="1h 15m"
                thumbnail_url="https://images.unsplash.com/photo-1590602847861-f357a9332bbc?w=400"
                published_at="2024-01-15"
                categories={['Technology', 'AI', 'Future']}
                url="https://example.com/podcast/episode-42"
              />
              <PodcastCard
                title="Building Scalable Systems"
                description="Discussions on architecture patterns for building scalable distributed systems"
                host="Software Engineering Daily"
                episode_number="Special"
                duration="52:30"
                thumbnail_url="https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400"
                published_at="2024-01-20"
                categories={['Engineering', 'Architecture']}
                url="https://example.com/podcast/special"
              />
            </div>
          </section>

          {/* Edge Cases Section */}
          <section>
            <h2 className="text-2xl font-semibold mb-4">Edge Cases</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <VideoCard
                title="Minimal Video Card"
                url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
              />
              <ImageCard
                image_url="https://invalid-url-to-test-fallback.jpg"
                title="Broken Image Test"
                description="This should show a fallback state"
              />
              <PodcastCard
                title="Minimal Podcast"
                host="Unknown Host"
                url="https://example.com/minimal"
              />
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}

export default MediaComponentsTest;
