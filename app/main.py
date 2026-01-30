from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session, engine
from app.models import Base
from app.crud import PriceCRUD
from app.schemas import PriceResponse, LatestPriceResponse

app = FastAPI(title="Deribit Price API")

crud = PriceCRUD()

async def get_db():
    async with async_session() as session:
        yield session

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/prices", response_model=list[PriceResponse])
async def get_all_prices(ticker: str = Query(..., min_length=3), db: AsyncSession = Depends(get_db)):
    """Все сохранённые данные по тикеру."""
    data = await crud.get_all(db, ticker)
    if not data:
        raise HTTPException(404, "No data found")
    return data

@app.get("/latest-price", response_model=LatestPriceResponse)
async def get_latest_price(ticker: str = Query(..., min_length=3), db: AsyncSession = Depends(get_db)):
    """Последняя цена."""
    data = await crud.get_latest(db, ticker)
    if not data:
        raise HTTPException(404, "No data found")
    return data

@app.get("/prices/filter", response_model=list[PriceResponse])
async def get_prices_by_date(
    ticker: str = Query(..., min_length=3),
    start_ts: int = Query(..., description="UNIX timestamp start"),
    end_ts: int = Query(..., description="UNIX timestamp end"),
    db: AsyncSession = Depends(get_db)
):
    """Цены за период."""
    if start_ts >= end_ts:
        raise HTTPException(400, "start_ts must be < end_ts")
    data = await crud.get_by_date(db, ticker, start_ts, end_ts)
    if not data:
        raise HTTPException(404, "No data in range")
    return data