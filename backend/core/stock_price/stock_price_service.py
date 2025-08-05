from dotenv import load_dotenv
import os
import requests
from typing import List
from .stock_price_schema import StockQuote

load_dotenv()


class StockPriceService:
    def __init__(self):
        self.api_key = os.getenv('FINHUB_API_KEY')
        self.base_url = os.getenv('FINHUB_BASE_URL')

    def get_stock_price(self, symbol: str) -> StockQuote:
        """Fetch current stock price for a given symbol."""
        if not self.api_key:
            raise ValueError("FINHUB_API_KEY not found in environment variables")
        if not self.base_url:
            raise ValueError("FINHUB_BASE_URL not found in environment variables")
    
        url = f"{self.base_url}/quote?symbol={symbol.upper()}"
        headers = {
            'Content-Type': 'application/json',
            'X-Finnhub-Token': self.api_key
        }
    
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return StockQuote(**data, symbol=symbol)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching stock price: {e}")
            raise

    def get_stock_price_batch(self, symbols: List[str]) -> List[StockQuote]:
        """Fetch current stock prices for a list of symbols using individual API calls."""
        if not self.api_key:
            raise ValueError("FINHUB_API_KEY not found in environment variables")
        if not self.base_url:
            raise ValueError("FINHUB_BASE_URL not found in environment variables")
        
        quotes = []
        for symbol in symbols:
            try:
                quote = self.get_stock_price(symbol)
                quotes.append(quote)
            except Exception as e:
                print(f"Error fetching price for {symbol}: {e}")
                # Optionally skip failed symbols or re-raise
                continue
        
        return quotes


# Usage example
if __name__ == "__main__":  
    try:
        stock_price_service = StockPriceService()
        quotes = stock_price_service.get_stock_price_batch(['AMSC', 'AAPL', 'MSFT'])
        for quote in quotes:
            print(f"Stock: {quote.symbol}")
            print(f"Current price: ${quote.current_price}")
            print(f"Change: ${quote.change}")
            print(f"Percent change: {quote.percent_change}%")
            print(f"Day range: ${quote.low} - ${quote.high}")
        print(f"Previous close: ${quote.previous_close}")
    except Exception as e:
        print(f"Failed to get price: {e}")

