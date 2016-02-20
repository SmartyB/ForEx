from lib.helpers import *
import indicators
from indicators.indicator import *
import lib

class EmaGradient(Indicator, lib.Event):
    def __init__(self, chart, period, **kwargs):
        self.period = period
        Indicator.__init__(self, chart)

        self.__points = []
        self.ema = self.chart.indicator(indicators.EMA, {'period':self.period})
        self.init_ema_gradient()

        self.chart.on("Candle-Close", target=self.calc_ema_grad)

    def init_ema_gradient(self):
        candles = self.chart.candles().notFirst(self.period+1).onlyClosed().get()

        while candles.hasNext():
            candle = candles.next()
            ema_gradient_point = self.init_ema_gradient_point(candle)
            ema_gradient_point.calculate_gradient()

    def init_ema_gradient_point(self, candle):
        try:
            ema_gradient_point = candle.indicators[self.displayName]
        except KeyError:
            ema_gradient_point = EmaGradientPoint(self, candle)
            candle.addIndicator(self.displayName, ema_gradient_point)
            self.__points.append(ema_gradient_point)

        return ema_gradient_point

    def calc_ema_grad(self, candle ):
        ema_gradient_point = self.init_ema_gradient_point(candle)
        ema_gradient_point.calculate_gradient()

class EmaGradientPoint:
    def __init__(self, ema_gradient, candle):
        self.ema_gradient = ema_gradient
        self.candle = candle

    def calculate_gradient(self):
        this_candle = self.candle
        prev_candle = self.ema_gradient.chart.candles().before(this_candle.time).get().last()

        this_ema = this_candle.indicators[self.ema_gradient.ema.displayName]
        prev_ema = prev_candle.indicators[self.ema_gradient.ema.displayName]

        values = {'openAsk':0.,'openBid':0.,'highAsk':0.,'highBid':0.,'closeAsk':0.,'closeBid':0.,'lowAsk':0.,'lowBid':0.}
        for field in values.keys():
            values[field] = this_ema.__dict__[field] - prev_ema.__dict__[field]
        self.__dict__.update(values)

        self.ema_gradient.event("Ema_Gradient-Set", self.candle)

    def __str__(self):
        return "<ema_gradient C:{:7.5f}>".format(self.closeBid)
