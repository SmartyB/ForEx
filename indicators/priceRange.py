from indicators.indicator import *
from indicators.fractal import *

class PriceRange(Indicator):
    def __init__(self, chart, **kwargs):
        Indicator.__init__(self, chart)

        self.rangeSet = False
        self.fractals = self.chart.indicator(Fractals, {'range':2})

        self.loadRange()
        self.chart.on("Candle-Close", self.candleClose, 30)

    def candleClose(self, candle, data=None, **kwargs):
        if self.rangeSet:
            if candle.openBid < self.rangeHigh and candle.closeBid > self.rangeHigh:
                self.event("Range-Break", self, data={'range':'high'})
            elif candle.openBid > self.rangeLow and candle.closeBid < self.rangeLow:
                self.event("Range-Break", self, data={'range':'down'})

            if candle.highBid > self.rangeHigh and candle.closeBid < self.rangeHigh:
                self.event("Range-Reject", self, data={'range':'high'})
            elif candle.lowBid < self.rangeLow and candle.closeBid:
                self.event("Range-Reject", self, data={'range':'low'})

        self.loadRange()

    def loadRange(self):
        try:
            upFractal = self.fractals.upfractals().onlyUnbroken().get().last()
            downFractal = self.fractals.downfractals().onlyUnbroken().get().last()

            self.rangeLow = downFractal.candle.lowBid
            self.rangeHigh = upFractal.candle.highBid

            self.rangeSet = True
        except:
            pass
