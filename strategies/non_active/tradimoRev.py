import indicators, lib
from strategies.strategy import Strategy
from lib.definitions import *

import time, datetime, pytz

class TradimoRev(Strategy, lib.Event):
    def __init__(self, instrument, kwargs):
        Strategy.__init__(self, instrument, kwargs)

        self.dir        = None
        self.dirtime    = None

        self.dirchart = self.instrument.chart(self.dirchart)
        self.tradechart = self.instrument.chart(self.tradechart)

        self.dirFractals = self.dirchart.indicator(indicators.Fractals, {'range':2})
        self.tradeFractals = self.tradechart.indicator(indicators.Fractals, {'range':2})

        self.pivots  = self.dirchart.indicator(indicators.Pivots, {})

        self.findDir()

    def begin(self):
        self.processing = False

        self.dirchart.on("Candle-Close", self.findDir)
        self.dirFractals.on('Fractal-Forms', self.findDir)
        self.dirFractals.on('Fractal-Breaks', self.findDir)

        self.tradeFractals.on('Fractal-Breaks', self.tradeFractalBreaks)
        self.tradeFractals.on('Fractal-Forms', self.manageTrade)
        self.tradeFractals.on('Fractal-Forms', self.manageOrder)

        self.manageTrade()
        self.manageOrder()

    def findDir(self, callee=None, data=None):
        up = self.dirFractals.upfractals().onlyBroken().getWithLastBreakPoint()
        down = self.dirFractals.downfractals().onlyBroken().getWithLastBreakPoint()

        #determine direction
        dir = self.dir
        if up.breakpoint.time > down.breakpoint.time:
            dir = "up"
            dirtime = up.breakpoint.time
        elif up.breakpoint.time < down.breakpoint.time:
            dir = "down"
            dirtime = down.breakpoint.time
        else:
            return


        # see if determined direction is different from our prev. dir.
        if self.dir == None:
            self.dir = dir
            self.dirtime = dirtime
        elif not self.dir == dir:
            self.dir = dir
            self.dirtime = dirtime
            self.dirChange()

    def dirChange(self, callee=None, data=None):
        self.closeAll()

    def tradeFractalBreaks(self, fractal, data=None):
        # fractal needs to break after the time our dir was set
        if fractal.candle.time < self.dirtime:
            return
        # fractal needs to break in opposite direction
        if data['type'] == self.dir:
            return

        # we only want one open trade per instrument
        if self.trades().get().length() > 0:
            return
        if self.orders().get().length() > 0:
            return

        if not self.processing:
            self.processing = True
            self.makeOrder()
            self.processing = False

    def makeOrder(self):
        side = None

        if self.dir == "up":
            side = SELL
            entry   = self.tradeFractals.upfractals().get().last().candle.highBid
            sl      = entry + 8 * self.instrument.pip
            tp      = entry - 5 * self.instrument.pip
        elif self.dir == "down":
            side = BUY
            entry   = self.tradeFractals.downfractals().get().last().candle.lowBid
            sl      = entry - 8 * self.instrument.pip
            tp      = entry + 5 * self.instrument.pip

        if tp == None:
            return

        if side:
            amount = self.account.get_balance(self.thread) * self.instrument.eurToQuote() * self.risk
            self.createOrder(side, amount, entry=entry, stopLoss=sl, takeProfit=tp, expiry=3600, type="marketIfTouched")


    def manageTrade(self, fractal=None, data=None):
        trades = self.trades().get()
        while trades.hasNext():
            trade = trades.next()
            if not trade.entry_price:
                continue

            # self.setSL(trade)
            # self.setTP(trade)

    def manageOrder(self, fractal=None, data=None):
        orders = self.orders().get()
        while orders.hasNext():
            order = orders.next()

            if not order.entry_price:
                continue

            self.setEntry(order)
            self.setSL(order, onlyLessRisk=True)
            self.setTP(order)

    def setTP(self, trade):
        entry = trade.entry_price
        if trade.side == BUY:
            tp = trade.entry_price + 5 * self.instrument.pip
        elif trade.side == SELL:
            tp = trade.entry_price - 5 * self.instrument.pip
        if tp == None:
            trade.close()
        else:
            trade.update(takeProfit=tp)

    def setSL(self, trade, onlyLessRisk=False):
        if trade.side == BUY:
            sl = trade.entry_price - 8 * self.instrument.pip
            if onlyLessRisk and not sl > trade.stopLoss:
                return
        if trade.side == SELL:
            sl = trade.entry_price + 8 * self.instrument.pip
            if onlyLessRisk and not sl < trade.stopLoss:
                return
        trade.update(stopLoss=sl)

    def setEntry(self, order):
        if order.side == BUY:
            entry = self.tradeFractals.downfractals().get().last().candle.lowBid
        elif order.side == SELL:
            entry = self.tradeFractals.downfractals().get().last().candle.lowBid
        order.update(entry=entry)
