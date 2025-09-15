import { inject, provide, type InjectionKey } from 'vue'

export interface TradeActions {
  openExecutionForm: () => void
  openTradeForm: () => void
  clearSelectedTrade: () => void
}

export type TradeActionsType = TradeActions
export const TRADE_ACTIONS_KEY: InjectionKey<TradeActionsType> = Symbol('tradeActions')

export const useProvideTradeActions = (actions: TradeActions): void => {
  provide(TRADE_ACTIONS_KEY, actions)
}

export const useInjectTradeActions = (): TradeActionsType => {
  const tradeActions = inject(TRADE_ACTIONS_KEY)

  if (!tradeActions) {
    throw new Error(
      'Trade actions not provided. Make sure to wrap component with trade actions provider.',
    )
  }

  return tradeActions
}
