from dotenv import load_dotenv
import logging
import os
import asyncio
import httpx
from typing import List
from .finnhub_schema import StockQuote

load_dotenv()
logger = logging.getLogger(__name__)


class FinnhubService:
    def __init__(self):
        self.api_key = os.getenv("FINHUB_API_KEY")
        self.base_url = os.getenv("FINHUB_BASE_URL")
        self.client = httpx.AsyncClient()

    async def close(self):
        await self.client.aclose()

    async def get_stock_price(self, symbol: str) -> StockQuote:
        """Fetch current stock price for a given symbol."""
        if not self.api_key:
            raise ValueError("FINHUB_API_KEY not found in environment variables")
        if not self.base_url:
            raise ValueError("FINHUB_BASE_URL not found in environment variables")

        url = f"{self.base_url}/quote?symbol={symbol.upper()}"
        headers = {"Content-Type": "application/json", "X-Finnhub-Token": self.api_key}

        try:
            response = await self.client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            data["symbol"] = symbol
            return StockQuote(**data)
        except httpx.HTTPError as e:
            logger.error(f"Error fetching stock price: {e}")
            raise

    async def get_stock_price_batch(self, symbols: List[str]) -> List[StockQuote]:
        """Fetch current stock prices for a list of symbols using individual API calls."""
        if not self.api_key:
            raise ValueError("FINHUB_API_KEY not found in environment variables")
        if not self.base_url:
            raise ValueError("FINHUB_BASE_URL not found in environment variables")

        tasks = [self.get_stock_price(symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        quotes: List[StockQuote] = []
        for symbol, result in zip(symbols, results):
            if isinstance(result, Exception):
                print(f"Error fetching price for {symbol}: {result}")
                continue

            quotes.append(result)
        return quotes


# Usage example
async def main():
    try:
        stock_price_service = FinnhubService()
        quotes = await stock_price_service.get_stock_price_batch(
            ["AMSC", "AAPL", "MSFT"]
        )
        for quote in quotes:
            print(f"Stock: {quote.symbol}")
            print(f"Current price: ${quote.current_price}")
            print(f"Change: ${quote.change}")
            print(f"Percent change: {quote.percent_change}%")
            print(f"Day range: ${quote.low} - ${quote.high}")
        print(f"Previous close: ${quote.previous_close}")
        await stock_price_service.close()
    except Exception as e:
        print(f"Failed to get price: {e}")


if __name__ == "__main__":
    asyncio.run(main())
