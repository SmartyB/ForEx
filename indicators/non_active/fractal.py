from lib.helpers import *
from indicators.indicator import *
import selector
import time

class Fractals(Indicator):
    def __init__(self, chart, range, **kwargs):
        self.range  = range
        Indicator.__init__(self, chart)

        self.__upFractals     = []
        self.__downFractals   = []
        self.__unbrokenDownFractals   = []
        self.__unbrokenUpFractals     = []

        self.loadHistoric()
        self.breakHistoric()

        self.chart.on("Candle-Close", target=self.candleClose)
        self.chart.on("Candle-Tick", target=self.candleTick)

    def loadHistoric(self):
        candles = self.chart.candles().notFirst(self.range).notLast(self.range).get()
        while candles.hasNext():
            candle = candles.next()
            self.candleHasFractal(candle)

    def candleClose(self, candle):
        # -1 because before method also removes one
        testCandle = self.chart.candles().before(candle.time).notLast(self.range -1).get().last()
        self.candleHasFractal(testCandle)

    def breakHistoric(self):
        fractals = self.__upFractals + self.__downFractals
        for fractal in fractals:
            candles = self.chart.candles().after(fractal.candle.time).get()
            while candles.hasNext():
                candle = candles.next()
                if fractal.__class__.__name__ == "UpFractal" and \
                        candle.highBid > fractal.candle.highBid:
                    self.__unbrokenUpFractals.remove(fractal)
                    fractal.frBreak(candle)
                    break
                if fractal.__class__.__name__ == "DownFractal" and \
                        candle.lowBid < fractal.candle.lowBid:
                    self.__unbrokenDownFractals.remove(fractal)
                    fractal.frBreak(candle)
                    break


    def breakTick(self, candle):
        broken = False
        if len(self.__unbrokenDownFractals) > 0:
            fractal = self.__unbrokenDownFractals[-1]
            if candle.lowBid < fractal.candle.lowBid:
                self.__unbrokenDownFractals.remove(fractal)
                fractal.frBreak(candle)
                broken = True
        if len(self.__unbrokenUpFractals) > 0:
            fractal = self.__unbrokenUpFractals[-1]
            if candle.highBid > fractal.candle.highBid:
                self.__unbrokenUpFractals.remove(fractal)
                fractal.frBreak(candle)
                broken = True
        if broken:
            self.breakTick(candle)

    def candleTick(self, candle):
        self.breakTick(candle)

    def candleHasFractal(self, candle):
        before = self.chart.candles().before(candle.time).last(self.range).get()
        after  = self.chart.candles().after(candle.time).first(self.range).get()

        upFrac = True
        downFrac = True

        while before.hasNext():
            testCandle = before.next()
            if testCandle.lowBid < candle.lowBid:
                downFrac = False
            if testCandle.highBid > candle.highBid:
                upFrac = False

        while after.hasNext():
            testCandle = after.next()
            if testCandle.lowBid <= candle.lowBid:
                downFrac = False
            if testCandle.highBid >= candle.highBid:
                upFrac = False

        if downFrac:
            fractal = DownFractal(self, candle)
            self.__downFractals.append(fractal)
            self.__unbrokenDownFractals.append(fractal)
            self.event("Fractal-Forms", fractal, data={'type':'down'})

        if upFrac:
            fractal = UpFractal(self, candle)
            self.__upFractals.append(fractal)
            self.__unbrokenUpFractals.append(fractal)
            self.event("Fractal-Forms", fractal, data={'type':'up'})

    def fractals(self):
        return selector.FractalSelector(self.__upFractals + self.__downFractals)

    def upfractals(self):
        return selector.FractalSelector(self.__upFractals)

    def downfractals(self):
        return selector.FractalSelector(self.__downFractals)

class Fractal:
    def __init__(self, fractals, candle):
        self.displayName = self.__class__.__name__+"-"+str(fractals.range)

        self.fractals = fractals
        self.candle = candle

        self.candle.addIndicator(self.displayName, self)

        self.broken = False
        self.breakpoint = None


    def __str__(self):
        if self.broken:
            return "<" + str(self.displayName) + " broken @" + str(self.breakpoint.time) + ">"
        else:
            return "<unbroken " + self.displayName + ">"


class UpFractal(Fractal):
    def __init__(self, fractals, candle):
        Fractal.__init__(self, fractals, candle)

    def frBreak(self, breakpoint):
        self.broken = True
        self.breakpoint = breakpoint
        self.fractals.event("Fractal-Breaks", self, data={'type':'up'})

class DownFractal(Fractal):
    def __init__(self, fractals, candle):
        Fractal.__init__(self, fractals, candle)

    def frBreak(self, breakpoint):
        self.broken = True
        self.breakpoint = breakpoint
        self.fractals.event("Fractal-Breaks", self, data={'type':'down'})
