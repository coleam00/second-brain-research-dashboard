/**
 * Carousel Component
 *
 * Scrollable carousel with scroll snap, optional auto-scroll, and navigation indicators.
 * Touch-friendly on mobile with smooth scroll behavior.
 */

import React, { useState, useEffect, useRef } from 'react';
import { cn } from "@/lib/utils";
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from "@/components/ui/button";

export interface CarouselProps {
  /** Carousel items to display */
  items: React.ReactNode[];

  /** Enable automatic scrolling */
  autoScroll?: boolean;

  /** Auto-scroll interval in milliseconds */
  autoScrollInterval?: number;

  /** Show navigation indicators (dots) */
  showIndicators?: boolean;

  /** Show navigation arrows */
  showArrows?: boolean;

  /** Gap spacing between items */
  gap?: string;

  /** Additional CSS classes */
  className?: string;
}

/**
 * Carousel Component
 *
 * Scrollable carousel with scroll snap container.
 * Supports auto-scroll, indicators, and touch-friendly navigation.
 */
export function Carousel({
  items,
  autoScroll = false,
  autoScrollInterval = 3000,
  showIndicators = true,
  showArrows = true,
  gap = '1rem',
  className,
}: CarouselProps): React.ReactElement {
  const [currentIndex, setCurrentIndex] = useState(0);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  const scrollToIndex = (index: number) => {
    if (scrollContainerRef.current) {
      const container = scrollContainerRef.current;
      const itemWidth = container.scrollWidth / items.length;
      container.scrollTo({
        left: itemWidth * index,
        behavior: 'smooth',
      });
      setCurrentIndex(index);
    }
  };

  const handleNext = () => {
    const nextIndex = (currentIndex + 1) % items.length;
    scrollToIndex(nextIndex);
  };

  const handlePrev = () => {
    const prevIndex = (currentIndex - 1 + items.length) % items.length;
    scrollToIndex(prevIndex);
  };

  // Auto-scroll effect
  useEffect(() => {
    if (autoScroll) {
      const interval = setInterval(handleNext, autoScrollInterval);
      return () => clearInterval(interval);
    }
  }, [autoScroll, autoScrollInterval, currentIndex]);

  return (
    <div className={cn('relative', className)}>
      {/* Carousel container with scroll snap */}
      <div
        ref={scrollContainerRef}
        className="flex overflow-x-auto snap-x snap-mandatory scrollbar-hide"
        style={{ gap, scrollbarWidth: 'none', msOverflowStyle: 'none' }}
      >
        {items.map((item, index) => (
          <div
            key={index}
            className="flex-shrink-0 w-full snap-center"
          >
            {item}
          </div>
        ))}
      </div>

      {/* Navigation Arrows */}
      {showArrows && items.length > 1 && (
        <>
          <Button
            variant="outline"
            size="icon"
            className="absolute left-2 top-1/2 -translate-y-1/2 rounded-full bg-background/80 backdrop-blur-sm"
            onClick={handlePrev}
          >
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            size="icon"
            className="absolute right-2 top-1/2 -translate-y-1/2 rounded-full bg-background/80 backdrop-blur-sm"
            onClick={handleNext}
          >
            <ChevronRight className="h-4 w-4" />
          </Button>
        </>
      )}

      {/* Indicators */}
      {showIndicators && items.length > 1 && (
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
          {items.map((_, index) => (
            <button
              key={index}
              onClick={() => scrollToIndex(index)}
              className={cn(
                'w-2 h-2 rounded-full transition-all',
                index === currentIndex
                  ? 'bg-primary w-4'
                  : 'bg-muted-foreground/30 hover:bg-muted-foreground/50'
              )}
              aria-label={`Go to slide ${index + 1}`}
            />
          ))}
        </div>
      )}

      {/* CSS to hide scrollbar */}
      <style>{`
        .scrollbar-hide::-webkit-scrollbar {
          display: none;
        }
      `}</style>
    </div>
  );
}

export default Carousel;
