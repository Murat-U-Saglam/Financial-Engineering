from sqlalchemy import (
    Column,
    String,
    Date,
    Integer,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Float

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
    __tablename__ = "stock_data"
    id = Column(Integer, primary_key=True)
    ticker = Column(String(5), nullable=False)
    date = Column(Date, nullable=False)
    open = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    dividend = Column(Float, nullable=False)
    stock_splits = Column(Float, nullable=False)
