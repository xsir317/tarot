export interface QuotaIndicatorProps {
  remaining: number
  total: number
}

export function QuotaIndicator({ remaining, total }: QuotaIndicatorProps) {
  const percentage = (remaining / total) * 100

  return (
    <div className="quota-indicator w-full max-w-xs space-y-2">
      <div className="flex justify-between items-center text-sm">
        <span className="text-purple-700 dark:text-purple-300">
          免费次数: {remaining}/{total}
        </span>
      </div>
      <div className="h-2 bg-purple-200 dark:bg-purple-800 rounded-full overflow-hidden">
        <div
          className="progress-fill h-full bg-gradient-to-r from-purple-500 to-indigo-500 transition-all duration-300"
          style={{ width: `${percentage.toFixed(2)}%` }}
        />
      </div>
    </div>
  )
}
