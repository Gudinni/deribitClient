import asyncio
import time
from celery import Celery
from app.config import settings
from app.client import DeribitClient
from app.database import async_session
from app.crud import PriceCRUD

celery_app = Celery(
    "tasks",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.tasks"]
)

celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "app.tasks.periodic_fetch_prices",
        "schedule": 60.0,  
    },
}

@celery_app.task
def periodic_fetch_prices():
    """Синхронная обёртка для async задачи."""
    asyncio.run(_async_fetch_and_save())

async def _async_fetch_and_save():
    client = DeribitClient(settings.deribit_url)
    crud = PriceCRUD()
    async with async_session() as session: 
        for index_name, ticker in [("btc_usd", "BTC"), ("eth_usd", "ETH")]:
            try:
                price = await client.get_index_price(index_name)
                ts = int(time.time())
                async with session.begin():  
                    await crud.create(session, ticker, price, ts)
                print(f"Saved {ticker}: {price} at {ts}")  
            except Exception as e:
                print(f"Error for {ticker} ({index_name}): {e}")