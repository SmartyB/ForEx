import selector
from lib.event import Event
from lib.helpers import *
from lib.definitions import *

from chart.candle import *
from indicators.indicator import Indicator

import threading
import time
import copy
import time

class Chart(Event):
    def __init__(self, instrument, granularity):
        self.instrument   = instrument
        self.account      = instrument.account
        self.con          = self.account.connections['t1']

        self.gran         = granularity
        self.period       = periods[self.gran]
        self.pair         = self.instrument.pair

        self.__indicators = {}
        self.__candles = []

        self._fully_loaded      = False
        self._unprocessed_ticks = []
        self.getHistory()

    def getHistory(self, numCandles=500):
        candlesTemp = self.con.get_instrument_history(
            instrument      = self.pair,
            count           = numCandles,
            granularity     = self.gran
        )['candles']
        for dCandle in candlesTemp:
            dCandle['time'] = rfc3339toEpoch(dCandle['time'])
            candle = Candle(self, dCandle['time'], sendEvents=False)
            candle.__dict__.update(dCandle)
            candle.strength = candle.closeBid - candle.openBid
            self.__candles.append(candle)
        self.instrument.bid = dCandle['closeBid']
        self.instrument.ask = dCandle['closeAsk']

        for tick in self._unprocessed_ticks:
            self.tick(tick)
        self._fully_loaded = True

    def tick(self, tick):
        if not self._fully_loaded:
            self._unprocessed_ticks.append(tick)
            return

        candles = self.candles() \
                    .containsTime(tick['time']) \
                    .get()
        if candles.hasNext():
            candles.next().tick(tick)
        else:
            #build the candle
            tickTime = rfc3339toEpoch(tick['time'])
            lastTime = self.__candles[-1].time
            while lastTime + self.period <= tickTime:
                lastTime += self.period
            candle = Candle(self, lastTime).tick(tick)
            self.__candles.append(candle)

    def candles(self):
        return selector.CandleSelector(self.__candles)

    def indicator(self, indicator, params={}):
        dispName = Indicator.parseDisplayName(indicator, params)

        if dispName in self.__indicators:
            return self.__indicators[dispName]
        else:
            self.__indicators[dispName] = indicator(self, **params)
            return self.__indicators[dispName]

    def __str__(self):
        num = 20
        for candle in reversed(self.__candles[-num:]):
            print(candle)
        return ""
