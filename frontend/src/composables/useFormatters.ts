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

  return {
    formatTradeDate,
    formatEntryPrice,
  }
}
