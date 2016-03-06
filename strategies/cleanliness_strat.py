import indicators, lib
from strategies.strategy import Strategy
from lib.definitions import *

import time, datetime, pytz

class CleanlinessStrat(Strategy, lib.Event):
    def __init__(self, instrument, kwargs):
        Strategy.__init__(self, instrument, kwargs)

        self.chart          = self.instrument.chart(self.chart)
        self.cleanliness    = self.chart.indicator(indicators.Cleanliness)
