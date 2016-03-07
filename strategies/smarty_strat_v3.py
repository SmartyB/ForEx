import indicators, lib
from strategies.strategy import Strategy
from lib.definitions import *

import time, datetime, pytz

class SmartyStratV3(Strategy, lib.Event):
    def __init__(self, instrument, kwargs):
        Strategy.__init__(self, instrument, kwargs)

        self.market_direction = None
        self.__processing = False

        self.chart          = self.instrument.chart(self.chart)
        self.ema_gradient   = self.chart.indicator(indicators.EmaGradient,
                            {'period': self.ema_period})

        self.ema_gradient.on('Ema_Gradient-Set', self.execute_strategy)

    def execute_strategy(self, candle):
        self.processing = True
        self.find_market_direction(candle)

        if self.orders().get().length() > 0:
            self.processing = False
            return
        if self.trades().get().length() > 0:
            self.processing = False
            return

        if self.market_direction:
            self.create_order()

        self.processing = False

    def create_order(self):
        # we wan't only one open trade per unit time
        if self.trades().get().length() > 0 or self.orders().get().length() > 0:
            return

        # we don't want to trade if a recent trade was losing
        trades = self.trades(onlyOpen=False).get()
        if trades.hasNext():
            last_trade = trades.last()
            time_since_trade = (datetime.datetime.now(tz=pytz.utc) - last_trade.exit_time).total_seconds()
            if last_trade.profitPips < 0 and time_since_trade < 7200:
                return

        side = None
        pip  = self.instrument.pip
        if self.market_direction == "up":
            side = BUY
            entry = self.instrument.ask - self.entry_distance * pip
            tp = entry + self.tp_pips * pip
            sl = entry - self.sl_pips * pip
        elif self.market_direction == "down":
            side = SELL
            entry = self.instrument.bid + self.entry_distance * pip
            tp = entry - self.tp_pips * pip
            sl = entry + self.sl_pips * pip

        if side:
            amount = self.account.get_balance(self.thread) * self.instrument.eurToQuote() * self.risk
            self.createOrder(side, amount, entry=entry, stopLoss=sl, takeProfit=tp, expiry=180, type="limit")

    def find_market_direction(self, candle):
        pip = self.instrument.pip
        new_dir = None

        ema_gradient = candle.indicators[self.ema_gradient.displayName].closeBid
        if abs(ema_gradient) > self.set_direction_limit * pip:
            if ema_gradient > 0: new_dir = 'up'
            elif ema_gradient < 0: new_dir = 'down'
        if abs(ema_gradient) < self.remove_direction_limit * pip:
            new_dir = None
            if self.market_direction:
                self.closeAll()

        if not self.market_direction == new_dir:
            # print("{0} - {1} - {2}".format(self.pair, new_dir, lib.helpers.epochToRfc3339_2(candle.time)))
            self.market_direction = new_dir
            self.event('smartystrat-new_direction', self)
