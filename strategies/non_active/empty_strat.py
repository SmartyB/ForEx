import indicators, lib
from strategies.strategy import Strategy
from lib.definitions import *

import time, datetime, pytz

class EmptyStrat(Strategy, lib.Event):
    def __init__(self, instrument, kwargs):
        Strategy.__init__(self, instrument, kwargs)
