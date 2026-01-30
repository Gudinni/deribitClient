from sqlalchemy import Column, Integer, String, Numeric, BigInteger, Index
from sqlalchemy.orm import DeclarativeBase
from decimal import Decimal

class Base(DeclarativeBase):
    pass

class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), nullable=False, index=True)
    price = Column(Numeric(precision=18, scale=8), nullable=False)
    timestamp = Column(BigInteger, nullable=False)  # UNIX timestamp

    __table_args__ = (Index("ix_ticker_timestamp", "ticker", "timestamp"),)