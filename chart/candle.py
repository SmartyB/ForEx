from lib.helpers import *
from lib.event import Event

import threading
import time as t

class Candle(Event):
    def __init__(self, chart, time, sendEvents=True):
        self.chart        = chart
        self.instrument   = chart.instrument
        self.account      = self.instrument.account

        self.lowAsk  = self.lowBid  = self.highAsk  = self.highBid  = None
        self.openAsk = self.openBid = self.closeAsk = self.closeBid = None
        self.strength = self.lastTick = None

        self.time       = time
        self.complete   = False
        self.indicators = {}

        if sendEvents:
            self.chart.event("Candle-Open", self)
            self.instrument.event("Candle-Open", self)

        closeTime = self.time + self.chart.period - t.time()
        if closeTime > 0:
            threading.Timer(closeTime, self.close).start()

    def close(self):
        '''
        Close the candle and send events
        '''
        self.complete = True
        self.chart.event("Candle-Close", self)
        self.instrument.event("Candle-Close", self)

    def tick(self, tick):
        '''
        Tick on the candle. Set new low and high values.
        '''
        ask = tick['ask']
        bid = tick['bid']
        self.lastTick = tick

        if self.openBid == None:
            self.openAsk = ask
            self.openBid = bid
        self.closeBid = bid
        self.closeAsk = ask
        self.strength = self.closeBid - self.openBid

        self.lowAsk  = min(self.lowAsk, ask)
        self.lowBid  = min(self.lowBid, bid)
        self.highAsk = max(self.highAsk, ask)
        self.highBid = max(self.highBid, bid)

        self.chart.event("Candle-Tick", self)
        self.instrument.event("Candle-Tick", self)

        return self

    def addIndicator(self, key, indicator):
        '''
        Add a new indicator
        '''
        self.indicators[key] = indicator

    def __str__(self):
        string =  "<Candle "
        if self.strength > 0:
            string += "  up>"
        elif self.strength < 0:
            string += "down>"

        string += " T:{} H:{:7.5f}, L:{:7.5f}, O:{:7.5f}, C:{:7.5f}, ".format(epochToRfc3339(self.time), self.highBid, self.lowBid, self.openBid, self.closeBid)

        string += " Indicators: ["
        for indicator in self.indicators:
            string += str(self.indicators[indicator]) + ", "
        return string[:-2] + "]"
