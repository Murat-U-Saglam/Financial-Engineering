from sqlalchemy import (
    create_engine,
    Column,
    String,
    Date,
    Integer,
    ForeignKey,
    MetaData,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Create the base class for declarative models
Base = declarative_base()


# Define the tickers table
class Tickers(Base):
    __tablename__ = "tickers"
    ticker = Column(String(10), primary_key=True)
    date_from = Column(Date)
    date_to = Column(Date)


# Define the ticker_data table
class TickerData(Base):
    __tablename__ = "ticker_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), ForeignKey("tickers.ticker"))
    date = Column(Date)
    open_price = Column(Integer)
    close_price = Column(Integer)
    volume = Column(Integer)
