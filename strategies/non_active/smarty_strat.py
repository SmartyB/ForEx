import indicators, lib
from strategies.strategy import Strategy
from lib.definitions import *

import time, datetime, pytz

class SmartyStrat(Strategy, lib.Event):
    def __init__(self, instrument, kwargs):
        Strategy.__init__(self, instrument, kwargs)

        self.chart =     self.instrument.chart(self.chart)
        self.ema_grad =  self.chart.indicator(indicators.EmaGrad, {'period': self.ema_period})
