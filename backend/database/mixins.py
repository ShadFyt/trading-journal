from typing import List, Optional

class RrRatioMixin:
    def calculate_rr_ratio(self, entry_price: float, stop: float, target_prices: Optional[List[float]]) -> float:
        if entry_price is None or stop is None or not target_prices:
            return 0.0
        risk = abs(entry_price - stop)
        if risk == 0:
            return 0.0
        
        total_rr = 0.0
        
        for target in target_prices:
            reward = abs(target - entry_price)
            rr = reward / risk
            total_rr += rr
        
        return round(total_rr / len(target_prices), 2)