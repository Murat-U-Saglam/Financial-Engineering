from sqlalchemy import create_engine, Column, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Type, TypedDict

Base = declarative_base()


# Define a TypedDict for type hints
class StockDataFields(TypedDict):
    id: int
    open: float
    high: float
    low: float
    close: float
    volume: int
    dividends: float
    stock_splits: float


def create_stock_data_class(table_name: str) -> Type[Base]:
    return type(
        "DynamicStockData",
        (Base,),
        {
            "__tablename__": table_name,
            "id": Column(Integer, primary_key=True),
            "open": Column(Float),
            "high": Column(Float),
            "low": Column(Float),
            "close": Column(Float),
            "volume": Column(Integer),
            "dividends": Column(Float),
            "stock_splits": Column(Float),
            "__annotations__": StockDataFields.__annotations__,  # Add type hints
        },
    )


if __name__ == "__main__":
    # Example usage
    engine = create_engine("sqlite:///stock_data.db", echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a dynamic class for 'AAPL' table
    AAPLStockData = create_stock_data_class("AAPL")

    # Use the class with type hints
    new_record = AAPLStockData(
        open=150.0,
        high=155.0,
        low=149.0,
        close=154.0,
        volume=1000,
        dividends=0.5,
        stock_splits=0.0,
    )
    session.add(new_record)
    session.commit()
