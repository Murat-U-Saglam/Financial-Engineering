from backtesting import Backtest, Strategy
from backtesting.lib import crossover

from backtesting.test import SMA, RSI


class RSISMAStrategy(Strategy):
    rsi_period = 14
    sma_period = 50
    rsi_overbought = 70
    rsi_oversold = 30
    stop_loss = 0.05
    take_profit = 0.10

    def init(self):
        self.rsi = self.I(RSI, self.data.Close, self.rsi_period)
        self.sma = self.I(SMA, self.data.Close, self.sma_period)
        self.buy_price = None

    def next(self):
        if not self.position:
            if self.rsi[-1] < self.rsi_oversold and crossover(self.data.Close, self.sma):
                self.buy_price = self.data.Close[-1]
                self.buy(sl=self.buy_price * (1 - self.stop_loss), tp=self.buy_price * (1 + self.take_profit))
        else:
            if self.rsi[-1] > self.rsi_overbought or crossover(self.sma, self.data.Close):
                self.position.close()