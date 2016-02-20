from lib.helpers import *
from lib.event import Event

import threading
import time as t

class Candle(Event):
    def __init__(self, chart, time, sendEvents=True):
        self.chart        = chart
        self.instrument   = chart.instrument
        self.account      = self.instrument.account

        self.lowAsk     = None
        self.lowBid     = None
        self.highAsk    = None
        self.highBid    = None
        self.openAsk    = None
        self.openBid    = None
        self.closeAsk   = None
        self.closeBid   = None
        self.strength   = None

        self.indicators = {}

        self.complete   = False
        self.lastTick = None
        self.time       = time

        if sendEvents:
            self.chart.event("Candle-Open", self)
            self.instrument.event("Candle-Open", self)

        closeTime = self.time + self.chart.period - t.time()
        if closeTime > 0:
            threading.Timer(closeTime, self.close).start()

    def close(self):
        self.complete = True
        self.chart.event("Candle-Close", self)
        self.instrument.event("Candle-Close", self)

    def tick(self, tick):
        self.lastTick = tick
        ask = tick['ask']
        bid = tick['bid']

        if self.openBid == None:
            self.openAsk = ask
            self.openBid = bid

        if self.lowAsk == None or ask < self.lowAsk:
            self.lowAsk = ask
        if self.lowBid == None or bid < self.lowBid:
            self.lowBid = bid
        if self.highAsk == None or ask > self.highAsk:
            self.highAsk = ask
        if self.highBid == None or bid > self.highBid:
            self.highBid = bid

        self.closeBid = bid
        self.closeAsk = ask
        self.strength = self.closeBid - self.openBid

        self.chart.event("Candle-Tick", self)
        self.instrument.event("Candle-Tick", self)

        return self

    def addIndicator(self, key, indicator):
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
