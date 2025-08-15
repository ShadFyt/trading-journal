export const useFormatters = () => {
  const formatTradeDate = (dateInput: string | Date) => {
    const date = convertStringToDate(dateInput)
    const now = new Date()

    const toStartOfDay = (d: Date) => {
      const sd = new Date(d)
      sd.setHours(0, 0, 0, 0)
      return sd
    }

    const isSameDay = (a: Date, b: Date) =>
      a.getFullYear() === b.getFullYear() &&
      a.getMonth() === b.getMonth() &&
      a.getDate() === b.getDate()

    if (isSameDay(date, now)) return 'Today'

    const yesterday = new Date(now)
    yesterday.setDate(now.getDate() - 1)
    if (isSameDay(date, yesterday)) return 'Yesterday'

    const diffInDays = Math.floor(
      (toStartOfDay(now).getTime() - toStartOfDay(date).getTime()) / (1000 * 60 * 60 * 24),
    )

    if (diffInDays >= 0 && diffInDays < 7) return `${diffInDays} days ago`

    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  }

  const convertStringToDate = (dateString: string | Date) => {
    if (dateString instanceof Date) return dateString
    if (!dateString || dateString.trim() === '') {
      throw new TypeError('Invalid date string: empty or whitespace')
    }

    const date = new Date(dateString)

    // Check if the date is valid by checking if it returns NaN
    if (isNaN(date.getTime())) {
      throw new TypeError(`Invalid date string: ${dateString}`)
    }

    return date
  }

  const formatEntryPrice = (entryMin: number, entryMax?: number) => {
    if (!entryMax || entryMin === entryMax) return `$${entryMin}`
    return `$${entryMin} - $${entryMax}`
  }

  const formatTradeDuration = (entryDate: Date | string) => {
    const entryDateObj = convertStringToDate(entryDate)
    const now = new Date()
    const diffTime = Math.abs(now.getTime() - entryDateObj.getTime())
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))

    if (diffDays === 0) return 'Today'
    if (diffDays === 1) return '1 day'
    return `${diffDays} days`
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
    formatTradeDuration,
    convertStringToDate,
  }
}
