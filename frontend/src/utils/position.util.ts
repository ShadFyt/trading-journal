export type RoundingMode = 'nearest' | 'floor' | 'ceil' | 'bankers'

export interface SharesFromPercentOptions {
  /** If your broker supports fractional shares, set true */
  allowFractional?: boolean
  /** Decimal places for fractional shares (e.g. 4 = 0.0001) */
  decimals?: number
  /** Rounding to apply when whole shares are required */
  rounding?: RoundingMode
}

const normalizePercent = (p: number | string): number => {
  let v: number
  if (typeof p === 'string') {
    const s = p.trim().replace('%', '')
    v = Number(s)
    if (!Number.isFinite(v)) throw new Error('Invalid percent string')
  } else {
    v = p
  }
  // If it's 0..1 treat as ratio; if >1 treat as whole percent
  if (v > 1) v = v / 100
  // Clamp 0..1
  return Math.min(1, Math.max(0, v))
}

const applyRounding = (x: number, mode: RoundingMode): number => {
  switch (mode) {
    case 'floor':
      return Math.floor(x)
    case 'ceil':
      return Math.ceil(x)
    case 'bankers': {
      const f = Math.floor(x)
      const frac = x - f
      if (frac > 0.5) return f + 1
      if (frac < 0.5) return f
      return f % 2 === 0 ? f : f + 1 // half-to-even
    }
    case 'nearest':
    default:
      return Math.round(x)
  }
}

export const sharesFromPercent = (
  totalShares: number,
  percent: number,
  options: SharesFromPercentOptions = {},
) => {
  const { allowFractional = false, decimals = 4, rounding = 'nearest' } = options
  const pct = normalizePercent(percent) // 0..1
  const raw = totalShares * pct

  let shares: number
  if (allowFractional) {
    const factor = 10 ** decimals
    shares = Math.round(raw * factor) / factor
  } else {
    shares = applyRounding(raw, rounding)
  }

  // Clamp to valid range
  shares = Math.max(0, Math.min(totalShares, shares))

  const remaining = allowFractional
    ? +(totalShares - shares).toFixed(decimals)
    : totalShares - shares

  const pctRequested = pct * 100
  const pctActual = (shares / totalShares) * 100

  return { shares, remaining, pctRequested, pctActual }
}
