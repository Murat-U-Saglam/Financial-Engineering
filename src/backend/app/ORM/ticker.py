from sqlalchemy import (
    Column,
    String,
    Date,
    Integer,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base

# Create the base class for declarative models
Base = declarative_base()


# Define the tickers table
class Tickers(Base):
    __tablename__ = "tickers"
    ticker = Column(String(length=5), primary_key=True)
    date_from = Column(Date)
    date_to = Column(Date)


# Define the ticker_data table
class StockData(Base):
    __tablename__ = "ticker_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(length=5), ForeignKey("tickers.ticker"))
    date = Column(Date)
    open_price = Column(Integer)
    close_price = Column(Integer)
    volume = Column(Integer)
