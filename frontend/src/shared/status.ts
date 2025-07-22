// Shared trade status definitions and style mapping
// Readability > cleverness, explicit types, and clear error handling

import type { TradeIdeaStatus } from '@/interfaces/trade-idea.type'

export interface StatusOption {
  value: TradeIdeaStatus | 'all'
  label: string
}

/**
 * List of all trade status options for dropdowns and filters.
 * @example
 * statusOptions.map(opt => <SelectItem value={opt.value}>{opt.label}</SelectItem>)
 */
export const statusOptions: StatusOption[] = [
  { value: 'all', label: 'All' },
  { value: 'InProgress', label: 'Executing Trade' },
  { value: 'Invalidated', label: 'Trade invalidated' },
  { value: 'Watching', label: 'Watchlist' },
  { value: 'Live', label: 'Live' },
]

/**
 * Mapping of trade status to Tailwind classes for badges.
 * @example
 * statusBadgeClass[trade.status]
 */
export const statusBadgeClass: Record<string, string> = {
  all: 'bg-gray-100 text-gray-700 border-gray-300',
  InProgress: 'bg-blue-100 text-blue-700 border-blue-300',
  Invalidated: 'bg-red-100 text-red-700 border-red-300',
  Watching: 'bg-yellow-100 text-yellow-700 border-yellow-300',
  Live: 'bg-green-100 text-green-700 border-green-300',
}
