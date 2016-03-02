from indicators.indicator import *

class Activity(Indicator):
    def __init__(self, chart, range, **kwargs):
        Indicator.__init__(self, chart)
        self.range = range
        self.displayName = "Activity-"+str(self.range)

        self.loadHistoric()

        self.chart.on("Candle-Open", self.calcActivity, 20)

    def loadHistoric(self):
        candles = self.chart.candles().notFirst(self.range).get()
        while candles.hasNext():
            self.calcActivity(candles.next())

    def calcActivity(self, candle):
        before = self.chart.candles().before(candle.time).last(self.range).get()

        lowest = None
        highest = None

        while before.hasNext():
            beforeCandle = before.next()

            if lowest == None or lowest > beforeCandle.lowBid:
                lowest = beforeCandle.lowBid
            if highest == None or highest < beforeCandle.highBid:
                highest = beforeCandle.highBid
        diff = highest - lowest

        candle.addIndicator(self.displayName, ActivityPoint(diff))


class ActivityPoint:
    def __init__(self, activity):
        self.value = activity
    def __str__(self):
        return "<activity: "+str(self.value)+">"
