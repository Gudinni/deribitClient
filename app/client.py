import aiohttp
from typing import Dict

class DeribitClient:
    """Клиент для Deribit API (index price)."""
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_index_price(self, index_name: str) -> float:
        url = f"{self.base_url}/public/get_index_price"
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "public/get_index_price",
            "params": {"index_name": index_name}
        }
        async with aiohttp.ClientSession() as session:
            resp = await session.post(url, json=payload)
            resp.raise_for_status()
            data: Dict = await resp.json()
            return float(data["result"]["index_price"])