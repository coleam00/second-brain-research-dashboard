import { Card } from '@/components/ui/card'

export function LoadingSkeleton() {
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header Skeleton */}
      <div className="space-y-3">
        <div className="h-8 bg-gradient-to-r from-secondary via-blue-500/20 to-secondary rounded-lg animate-shimmer bg-[length:200%_100%]" />
        <div className="h-4 bg-gradient-to-r from-secondary via-blue-500/20 to-secondary rounded-lg animate-shimmer bg-[length:200%_100%] w-3/4" />
      </div>

      {/* Card Skeletons */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {[1, 2, 3, 4].map((i) => (
          <Card key={i} className="p-4 space-y-3 border-blue-500/10">
            <div className="h-6 bg-gradient-to-r from-secondary via-blue-500/20 to-secondary rounded-lg animate-shimmer bg-[length:200%_100%] w-1/2" />
            <div className="space-y-2">
              <div className="h-4 bg-gradient-to-r from-secondary via-blue-500/15 to-secondary rounded animate-shimmer bg-[length:200%_100%]" />
              <div className="h-4 bg-gradient-to-r from-secondary via-blue-500/15 to-secondary rounded animate-shimmer bg-[length:200%_100%] w-5/6" />
              <div className="h-4 bg-gradient-to-r from-secondary via-blue-500/15 to-secondary rounded animate-shimmer bg-[length:200%_100%] w-4/6" />
            </div>
          </Card>
        ))}
      </div>

      {/* List Skeleton */}
      <Card className="p-4 space-y-3 border-blue-500/10">
        <div className="h-6 bg-gradient-to-r from-secondary via-blue-500/20 to-secondary rounded-lg animate-shimmer bg-[length:200%_100%] w-1/3" />
        <div className="space-y-2">
          {[1, 2, 3, 4, 5].map((i) => (
            <div
              key={i}
              className="flex items-center gap-3"
            >
              <div className="h-4 w-4 bg-gradient-to-r from-blue-500/30 via-blue-400/40 to-blue-500/30 rounded-full animate-shimmer bg-[length:200%_100%]" />
              <div className="h-4 bg-gradient-to-r from-secondary via-blue-500/15 to-secondary rounded animate-shimmer bg-[length:200%_100%] flex-1" />
            </div>
          ))}
        </div>
      </Card>

      {/* Chart Skeleton */}
      <Card className="p-4 space-y-3 border-blue-500/10">
        <div className="h-6 bg-gradient-to-r from-secondary via-blue-500/20 to-secondary rounded-lg animate-shimmer bg-[length:200%_100%] w-1/4" />
        <div className="flex items-end gap-2 h-32">
          {[40, 60, 80, 50, 70, 90, 65].map((height, i) => (
            <div
              key={i}
              className="flex-1 bg-gradient-to-t from-blue-600/40 to-blue-400/20 rounded-t animate-shimmer bg-[length:100%_200%]"
              style={{ height: `${height}%` }}
            />
          ))}
        </div>
      </Card>

      {/* Stats Skeleton */}
      <div className="grid grid-cols-3 gap-4">
        {[1, 2, 3].map((i) => (
          <Card key={i} className="p-4 space-y-2 border-blue-500/10">
            <div className="h-4 bg-gradient-to-r from-secondary via-blue-500/20 to-secondary rounded animate-shimmer bg-[length:200%_100%] w-2/3" />
            <div className="h-8 bg-gradient-to-r from-blue-500/30 via-blue-400/40 to-blue-500/30 rounded-lg animate-shimmer bg-[length:200%_100%] w-1/2" />
          </Card>
        ))}
      </div>
    </div>
  )
}
