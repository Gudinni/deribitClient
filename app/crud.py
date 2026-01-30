from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Price
from decimal import Decimal
from typing import List, Optional

class PriceCRUD:
    async def create(self, db: AsyncSession, ticker: str, price: float, ts: int):
        obj = Price(ticker=ticker.upper(), price=Decimal(str(price)), timestamp=ts)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def get_all(self, db: AsyncSession, ticker: str) -> List[dict]:
        result = await db.execute(
            select(Price).where(Price.ticker == ticker.upper()).order_by(Price.timestamp.desc())
        )
        return [{"ticker": p.ticker, "price": float(p.price), "timestamp": p.timestamp} for p in result.scalars().all()]

    async def get_latest(self, db: AsyncSession, ticker: str) -> Optional[dict]:
        result = await db.execute(
            select(Price).where(Price.ticker == ticker.upper()).order_by(Price.timestamp.desc()).limit(1)
        )
        p = result.scalar_one_or_none()
        if p:
            return {"ticker": p.ticker, "price": float(p.price), "timestamp": p.timestamp}
        return None

    async def get_by_date(self, db: AsyncSession, ticker: str, start_ts: int, end_ts: int) -> List[dict]:
        result = await db.execute(
            select(Price).where(
                Price.ticker == ticker.upper(),
                Price.timestamp >= start_ts,
                Price.timestamp <= end_ts
            ).order_by(Price.timestamp)
        )
        return [{"ticker": p.ticker, "price": float(p.price), "timestamp": p.timestamp} for p in result.scalars().all()]