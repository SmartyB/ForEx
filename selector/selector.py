from selector.itterator import Itterator
import lib, time

class Selector:
    def __init__(self, arr):
        # copy the array
        self.array = []
        for i in arr:
            self.array.append(i)

    def withCondition(self, param, value=None):
        arr = []
        for i in self.array:
            if getattr(i, param) == value or (value == None and not getattr(i, param) == None):
                arr.append(i)
        self.array = arr
        return self

    def ofType(self, sType):
        arr = []
        for indicator in self.array:
            if indicator.__class__.__name__ == sType:
                arr.append(indicator)
        self.array = arr
        return self

    def notFirst(self, n):
        self.array = self.array[n:]
        return self

    def notLast(self, n):
        self.array = self.array[:-n]
        return self

    def last(self, n):
        self.array = self.array[-n:]
        return self

    def first(self, n):
        self.array = self.array[:n]
        return self

    def get(self):
        return Itterator(self.array)

    def __add__(self, other):
        assert self.__class__.__name__ == other.__class__.__name__
        self.array += other.array
        return self

class FractalSelector(Selector):
    def onlyBroken(self):
        temp = []
        for fractal in self.array:
            if fractal.broken:
                temp.append(fractal)
        self.array = temp
        return self
    def onlyUnbroken(self):
        temp = []
        for fractal in self.array:
            if not fractal.broken:
                temp.append(fractal)
        self.array = temp
        return self
    def after(self, time):
        time = lib.helpers.timeToEpoch(time)
        temp = []
        for fractal in self.array:
            if fractal.candle.time > time:
                temp.append(fractal)
        self.array = temp
        return self
    def onlyInLast(self, seconds):
        now = time.time()
        after = now - seconds
        temp = []
        for fractal in self.array:
            if lib.helpers.timeToEpoch(fractal.candle.time) > after:
                temp.append(fractal)
        self.array = temp
        return self
    def getWithLastBreakPoint(self):
        last = self.array[0]
        for fractal in self.array[1:]:
            if fractal.breakpoint.time >= last.breakpoint.time:
                last = fractal
        return last

class CandleSelector(Selector):
    def containsTime(self,time):
        time = lib.helpers.timeToEpoch(time)
        temp = []
        candleTime = self.array[-1].chart.period
        for candle in self.array:
            if candle.time <= time and time < candle.time + candleTime:
                temp.append(candle)
        self.array = temp
        return self

    def withTime(self,time):
        time = lib.helpers.timeToEpoch(time)
        temp = []
        for candle in self.array:
            if candle.time == time:
                temp.append(candle)
        self.array = temp
        return self

    def before(self, time):
        time = lib.helpers.timeToEpoch(time)
        temp = []
        for candle in self.array:
            if candle.time < time:
                temp.append(candle)
        self.array = temp
        return self

    def after(self, time):
        time = lib.helpers.timeToEpoch(time)
        temp = []
        for candle in self.array:
            if candle.time > time:
                temp.append(candle)
        self.array = temp
        return self

    def onlyClosed(self):
        return self.withCondition('complete', value=True)

    def withIndicator(self, indicator):
        temp = []
        for candle in self.array:
            try:
                getattr(candle, indicator)
                temp.append(candle)
            except AttributeError:
                pass
        self.array = temp
        return self

class ChartSelector(Selector):
    def withGran(self, gran):
        temp = []
        for chart in self.array:
            if chart.getGran() == gran:
                temp.append(chart)
        self.array = temp
        return self

    def withCur(self, cur):
        temp = []
        for chart in self.array:
            if cur in chart.getPair():
                temp.append(chart)
        self.array = temp
        return self

class InstrumentSelector(Selector):
    def withPair(self, pair):
        tempList = []
        for instrument in self.array:
            if instrument.pair.lower() == pair.lower():
                tempList.append(instrument)
        self.array = tempList
        return self

    def withCur(self, cur):
        tempList = []
        for instrument in self.array:
            if cur.lower() in instrument.pair.lower():
                tempList.append(instrument)
        self.array = tempList
        return self

    def onlyActive(self):
        tempList = []
        for instrument in self.array:
            if instrument.getActive():
                tempList.append(instrument)
        self.array = tempList
        return self

    def onlyPaused(self):
        tempList = []
        for instrument in self.array:
            if not instrument.getActive():
                tempList.append(instrument)
        self.array = tempList
        return self

class IndicatorSelector(Selector):
    pass


class IndicatorPointSelector(Selector):
    pass

class StrategySelector(Selector):
    def withDisplayName(self, displayName):
        arr = []
        for strat in self.array:
            if strat.displayName == displayName:
                arr.append(strat)
        self.array = arr
        return self

class OrderSelector(Selector):
    def __init__(self, arr, onlyOpen=True):
        self.array = []
        for i in arr:
            self.array.append(i)
        if onlyOpen:
            self.onlyOpen()

    def withID(self, id):
        arr = []
        for order in self.array:
            if order.id == id:
                arr.append(order)
        self.array = arr
        return self
    def onlyOpen(self):
        arr = []
        for order in self.array:
            if order.open:
                arr.append(order)
        self.array = arr
        return self

class TradeSelector(Selector):
    def __init__(self, arr, onlyOpen=True):
        self.array = []
        for i in arr:
            self.array.append(i)
        if onlyOpen:
            self.onlyOpen()

    def onlyLong(self):
        arr = []
        for trade in self.array:
            if trade.side == "buy":
                arr.append(trade)
        self.array = arr
        return self

    def onlyShort(self):
        arr = []
        for trade in self.array:
            if trade.side == "sell":
                arr.append(trade)
        self.array = arr
        return self

    def withID(self, id):
        arr = []
        for trade in self.array:
            if trade.id == id:
                arr.append(trade)
        self.array = arr
        return self
    def onlyOpen(self):
        arr = []
        for trade in self.array:
            if trade.open:
                arr.append(trade)
        self.array = arr
        return self
    def onlyClosed(self):
        arr = []
        for trade in self.array:
            if not trade.open:
                arr.append(trade)
        self.array = arr
        return self
