from dotenv import load_dotenv
from fastapi import HTTPException
from fastapi_cache.decorator import cache
from fastapi_cache import FastAPICache
import logging
import os
import asyncio
import httpx
import time
from typing import List

from pydantic import ValidationError

from .finnhub_schema import StockQuote, CompanyProfile


load_dotenv()
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

ONE_DAY = 86400


@cache(expire=ONE_DAY)
async def _fetch_company_profile(url: str) -> dict | None:
    """Cached function to fetch company profile data."""
    api_key = os.getenv("FINHUB_API_KEY")
    headers = {"Content-Type": "application/json", "X-Finnhub-Token": api_key}

    logger.info(f"🔥 CACHE MISS: Fetching {url} from Finnhub API")
    start_time = time.time()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            end_time = time.time()
            logger.info(f"✅ API call took {end_time - start_time:.2f} seconds")

            # Check if the response is empty or invalid (Finnhub returns {} for invalid tickers)
            if not data or not isinstance(data, dict) or not data.get("name"):
                logger.warning(f"Invalid or empty response from Finnhub API: {data}")
                return None

            return data
        except httpx.HTTPError as e:
            logger.error(f"Error fetching company profile: {e}")
            return None


class FinnhubService:
    def __init__(self):
        self.api_key = os.getenv("FINHUB_API_KEY")
        self.base_url = os.getenv("FINHUB_BASE_URL")
        self._validate_config()

        headers = {"Content-Type": "application/json", "X-Finnhub-Token": self.api_key}
        self.client = httpx.AsyncClient(headers=headers)

    def _validate_config(self):
        """Validate API configuration on initialization."""
        if not self.api_key:
            raise ValueError("FINHUB_API_KEY not found in environment variables")
        if not self.base_url:
            raise ValueError("FINHUB_BASE_URL not found in environment variables")

    async def close(self):
        await self.client.aclose()

    async def get_stock_price(self, symbol: str) -> StockQuote:
        """Fetch current stock price for a given symbol."""

        url = f"{self.base_url}/quote?symbol={symbol.upper()}"

        try:
            response = await self.client.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            data["symbol"] = symbol
            return StockQuote(**data)
        except httpx.HTTPError as e:
            logger.error(f"Error fetching stock price: {e}")
            raise

    async def get_stock_price_batch(self, symbols: List[str]) -> List[StockQuote]:
        """Fetch current stock prices for a list of symbols using individual API calls."""

        tasks = [self.get_stock_price(symbol) for symbol in symbols]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        quotes: List[StockQuote] = []
        for symbol, result in zip(symbols, results):
            if isinstance(result, Exception):
                print(f"Error fetching price for {symbol}: {result}")
                continue

            quotes.append(result)
        return quotes

    async def get_company_profile(self, symbol: str) -> CompanyProfile | None:
        """Fetch company profile for a given symbol."""
        url = f"{self.base_url}/stock/profile2?symbol={symbol.upper()}"

        try:
            data = await _fetch_company_profile(url)
            if data is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Company profile not found for symbol {symbol}",
                )

            return CompanyProfile(**data)

        except HTTPException:
            raise
        except ValidationError as e:

            raise HTTPException(
                status_code=422,
                detail=f"Invalid data format for symbol {symbol}: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Internal error processing symbol {symbol}"
            )


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
