from typing import List, Optional, Literal

Side = Literal["long", "short"]

class RrRatioMixin:
    @staticmethod
    def _risk_per_share(entry: float, stop: float, side: Side) -> float:
        risk = (entry - stop) if side == "long" else (stop - entry)
        return risk if risk > 0 else 0.0

    @staticmethod
    def _rr(entry: float, stop: float, target: float, side: Side) -> float:
        risk = (entry - stop) if side == "long" else (stop - entry)
        reward = (target - entry) if side == "long" else (entry - target)
        if risk <= 0 or reward <= 0:
            return 0.0
        return reward / risk

    def calculate_rr_ratio(
        self,
        entry_price: float,
        stop: float,
        target_prices: Optional[List[float]],
        side: Optional[Side] = None,
        weights: Optional[List[float]] = None,
    ) -> Optional[float]:
        if entry_price is None or stop is None or not target_prices:
            return None

        # Infer side if not provided: stop below entry => long, else short
        side = side or ("long" if stop < entry_price else "short")

        rrs = [self._rr(entry_price, stop, t, side) for t in target_prices]
        # If all targets are non-profitable, bail
        if not any(rrs):
            return None

        if weights:
            if len(weights) != len(target_prices):
                raise ValueError("weights length must match target_prices length")
            total_w = sum(weights)
            if total_w <= 0:
                return None
            rr = sum(rr * w for rr, w in zip(rrs, weights)) / total_w
        else:
            rr = sum(rrs) / len(rrs)

        return rr  # format with round(...) or f"{rr:.2f}" in your UI
