from ORM.ticker import StockData, Tickers
from models.db_models import StockDataModel, TickersModel
from data.database import get_session


def write_meta_data_to_db(meta_data_model: TickersModel) -> None:
    """
    write_meta_data_to_db writes the meta data to the database, checks if the data range is already in the database and updates it if necessary.
    """
    with get_session() as session:
        in_db = get_ticker_data(meta_data_model)
        if not in_db:
            ticker = Tickers(
                ticker=meta_data_model.ticker,
                date_from=meta_data_model.date_from,
                date_to=meta_data_model.date_to,
            )
            session.add(ticker)
            session.commit()
        else:
            update_ticker_data(ticker_data_model=meta_data_model, in_db=in_db)


def update_ticker_data(ticker_data_model: TickerDataModel, in_db: TickerData) -> None:
    with get_session() as session:
        if in_db.date_from < ticker_data_model.date_from:
            in_db.date_from = ticker_data_model.date_from
            session.commit()
        elif in_db.date_to > ticker_data_model.date_to:
            in_db.date_to = ticker_data_model.date_to
            session.commit()


def get_ticker_data(get_ticker_data: TickersModel) -> bool | Tickers:
    """
    get_meta_data: returns the meta data if it is already in the database. If it is not in the database it returns False.
    """
    with get_session() as session:
        query = session.query(Tickers).filter_by(ticker=get_ticker_data.ticker)
        if query.first():
            return query.first()
        else:
            return False


def delete_ticker_data(ticker_data: TickersModel) -> None:
    """
    delete_ticker_data deletes the meta data from the database.
    """
    with get_session() as session:
        query = session.query(Tickers).filter_by(ticker=ticker_data.ticker)
        if query.first():
            query.delete()
            session.commit()
        else:
            return False


def get_stock_data(stock_data: StockDataModel) -> bool | StockData:
    """
    get_stock_data returns the stock data from the database.
    """
    with get_session() as session:
        query = session.query(StockData).filter_by(ticker=stock_data.ticker)
        if query.first():
            return query.first()
        else:
            return False


def create_stock_data(stock_data: StockDataModel) -> None:
    """
    create_stock_data writes the stock data to the database.
    Always check data bounds with TickerData before writing stock data.
    """
    with get_session() as session:
        in_db = get_stock_data(stock_data)
        if not in_db:
            stock_data = StockData(
                ticker=stock_data.ticker,
                date=stock_data.date,
                open_price=stock_data.open_price,
                close_price=stock_data.close_price,
                volume=stock_data.volume,
            )
            session.add(stock_data)
            session.commit()


def delete_all_stock_data(stock_data: StockDataModel) -> None:
    """
    delete_stock_data deletes the stock data from the database.
    """
    with get_session() as session:
        query = session.query(StockData).filter_by(ticker=stock_data.ticker)
        if query.first():
            query.delete()
            session.commit()
        else:
            return None
