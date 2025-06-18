// Shared trade status definitions and style mapping
// Readability > cleverness, explicit types, and clear error handling

import type { Status } from '@/interfaces/watchlist.type'

export interface StatusOption {
  value: Status | 'all'
  label: string
}

/**
 * List of all trade status options for dropdowns and filters.
 * @example
 * statusOptions.map(opt => <SelectItem value={opt.value}>{opt.label}</SelectItem>)
 */
export const statusOptions: StatusOption[] = [
  { value: 'all', label: 'All' },
  { value: 'inProgress', label: 'Executing Trade' },
  { value: 'invalidated', label: 'Trade invalidated' },
  { value: 'waiting', label: 'Watchlist' },
  { value: 'live', label: 'Live' },
]

/**
 * Mapping of trade status to Tailwind classes for badges.
 * @example
 * statusBadgeClass[trade.status]
 */
export const statusBadgeClass: Record<string, string> = {
  all: 'bg-gray-100 text-gray-700 border-gray-300',
  inProgress: 'bg-blue-100 text-blue-700 border-blue-300',
  invalidated: 'bg-red-100 text-red-700 border-red-300',
  waiting: 'bg-yellow-100 text-yellow-700 border-yellow-300',
  live: 'bg-green-100 text-green-700 border-green-300',
}
