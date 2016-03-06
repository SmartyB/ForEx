from lib.helpers import *
from indicators.indicator import *

class Cleanliness(Indicator):
    def __init__(self, chart, **kwargs):
        Indicator.__init__(self, chart)

        self.__points = []
        self.num_candles = 3
        self.init_cleanliness()

        self.chart.on("Candle-Tick", target=self.tick)

    def init_cleanliness(self):
        candles = self.chart.candles().notFirst(self.num_candles).get()

        while candles.hasNext():
            candle = candles.next()
            cleanliness_point = self.init_cleanliness_point(candle)
            # cleanliness_point.calculate_gradient()

    def init_cleanliness_point(self, candle):
        try:
            cleanliness_point = candle.indicators[self.displayName]
        except KeyError:
            cleanliness_point = CleanlinessPoint(self, candle)
            candle.addIndicator(self.displayName, cleanliness_point)
            self.__points.append(cleanliness_point)

        return cleanliness_point

    def tick(self, candle, data=None):
        cleanliness_point = self.init_cleanliness_point(candle)
        cleanliness_point.determine_cleanliness()

class CleanlinessPoint:
    def __init__(self, indicator, candle):
        self.candle = candle
        self.indicator = indicator

        self.min = self.max = None
        self.cleanliness_abs = self.cleanlinesss_rel = None

        self.determine_min_max()
        self.determine_cleanliness()

    def determine_min_max(self):
        min_bid = max_bid = None

        candles = self.indicator.chart.candles().before(self.candle.time).last(self.indicator.num_candles).get()
        while candles.hasNext():
            prev_candle = candles.next()
            candle_min = min(prev_candle.closeBid, prev_candle.openBid)
            candle_max = max(prev_candle.closeBid, prev_candle.openBid)
            if not min_bid or candle_min < min_bid:
                min_bid = candle_min
            if not max_bid or candle_max > max_bid:
                max_bid = candle_max
        self.min = min_bid
        self.max = max_bid

    def determine_cleanliness(self):
         candle_max = max(self.candle.closeBid, self.candle.openBid)
         candle_min = min(self.candle.closeBid, self.candle.openBid)

         self.cleanliness_abs = max(0, min(self.max, candle_max) - max(self.min, candle_min))
        #  self.cleanlinesss_rel = self.cleanliness_abs / self.candle.strength

    def __str__(self):
        return "<cleanliness C:{:7.5f}>".format(self.cleanliness_abs)
