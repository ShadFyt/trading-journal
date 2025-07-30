export const useFormatters = () => {
  const formatTradeDate = (dateString: string) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffInDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24))

    if (diffInDays === 0) return 'Today'
    if (diffInDays === 1) return 'Yesterday'
    if (diffInDays < 7) return `${diffInDays} days ago`

    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  }

  const formatEntryPrice = (entryMin: number, entryMax?: number) => {
    if (!entryMax || entryMin === entryMax) return `$${entryMin}`
    return `$${entryMin} - $${entryMax}`
  }

  /**
   * Format currency values
   */
  const formatCurrency = (value: number): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(value)
  }

  /**
   * Format percentage values
   */
  const formatPercentage = (value: number): string => {
    const sign = value >= 0 ? '+' : ''
    return `${sign}${value.toFixed(2)}%`
  }

  return {
    formatTradeDate,
    formatEntryPrice,
    formatCurrency,
    formatPercentage,
  }
}
