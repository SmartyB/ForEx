from lib.helpers import *
from indicators.indicator import *

class EMA(Indicator):
    def __init__(self, chart, period, **kwargs):
        self.period = period
        self.weight = 2. / (self.period +  1)
        Indicator.__init__(self, chart)

        self.__points   = []

        self.initEMA()

        self.chart.on("Candle-Tick", target=self.tick)

    def initEMA(self):
        values = {'openAsk':0.,'openBid':0.,'highAsk':0.,'highBid':0.,'closeAsk':0.,'closeBid':0.,'lowAsk':0.,'lowBid':0.}
        candles = self.chart.candles().notFirst(self.period).get()
        firstcandle = candles.next()

        ema = self.loadEMAPoint(firstcandle)
        maCandles = self.chart.candles().before(firstcandle.time).get()

        # first ema is the ma point
        while maCandles.hasNext():
            candle = maCandles.next()
            for key in values:
                    values[key] += getattr(candle, key) / self.period

        ema.__dict__.update(values)

        while candles.hasNext():
            candle = candles.next()
            ema = self.loadEMAPoint(candle)
            ema.calculateEMA()

    def tick(self, candle, data=None):
        ema = self.loadEMAPoint(candle)
        ema.calculateEMA()
        self.event("EMA-Update", self, data={'candle':candle})

    def loadEMAPoint(self, candle):
        try:
            ema = candle.indicators[self.displayName]
        except KeyError:
            ema = EMAPoint(self, candle)
            candle.addIndicator(self.displayName, ema)
            self.__points.append(ema)

        return ema

    def __str__(self):
        string = "["
        for point in self.__points[-10:]:
            string += str(point) + ", "
        return string[:-2] + "]"

class EMAPoint:
    def __init__(self, ema, candle):
        self.ema = ema
        self.candle = candle
    def calculateEMA(self):
        self.period = self.ema.period
        weight = 2. / (self.period + 1)
        lastCandle = self.ema.chart.candles().before(self.candle.time).get().last()
        lastEma = lastCandle.indicators[self.ema.displayName]

        values = {'openAsk':0.,'openBid':0.,'highAsk':0.,'highBid':0.,'closeAsk':0.,'closeBid':0.,'lowAsk':0.,'lowBid':0.}
        for key in values:
            values[key] = weight * getattr(self.candle, key) + (1. - weight) * getattr(lastEma, key)
        self.__dict__.update(values)


    def __str__(self):
        return "<ema C:{:7.5f}>".format(self.closeBid)
