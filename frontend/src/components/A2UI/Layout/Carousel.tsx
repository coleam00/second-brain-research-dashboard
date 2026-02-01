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
            className="absolute left-2 top-1/2 -translate-y-1/2 rounded-full bg-slate-900/90 backdrop-blur-sm border-blue-500/30 text-blue-300 hover:bg-blue-600 hover:text-white hover:border-blue-400 transition-all shadow-lg shadow-blue-500/20"
            onClick={handlePrev}
          >
            <ChevronLeft className="h-4 w-4" />
          </Button>
          <Button
            variant="outline"
            size="icon"
            className="absolute right-2 top-1/2 -translate-y-1/2 rounded-full bg-slate-900/90 backdrop-blur-sm border-blue-500/30 text-blue-300 hover:bg-blue-600 hover:text-white hover:border-blue-400 transition-all shadow-lg shadow-blue-500/20"
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
                'h-2 rounded-full transition-all',
                index === currentIndex
                  ? 'bg-gradient-to-r from-blue-500 to-blue-400 w-8 shadow-lg shadow-blue-500/50'
                  : 'bg-blue-500/20 w-2 hover:bg-blue-500/40'
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
