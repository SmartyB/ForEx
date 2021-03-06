import position, lib, selector
import threading, time, datetime, pytz

class Strategy(lib.Event, lib.Scheduler):
    def __init__(self, instrument, kwargs):
        self.__dict__.update(kwargs)
        self.account    = instrument.account
        self.instrument = instrument

        lib.Scheduler.__init__(self)

        self.con         = self.account.connections[self.thread]
        self.displayName = self.parseDisplayName(self.__class__, self.__dict__)

        self._orders   = []
        self._trades   = []

        self.news_close_schedule()

    def begin(self):
        pass

    def createOrder(self, side, units, entry=None, stopLoss=None, takeProfit=None, trailingStop=None, expiry=10800, type='stop', riskClosePips=None):
        if not self.active:
            return False
        if not self.order_news_allowed():
            return False

        if units < 1:
            return

        if entry:
            entry = round(entry, self.instrument.precision)
        if stopLoss:
            stopLoss = round(stopLoss, self.instrument.precision)
        if takeProfit:
            takeProfit = round(takeProfit, self.instrument.precision)
        if trailingStop:
            trailingStop = round(trailingStop, self.instrument.precision)

        dOrder = {
            'instrument'    : self.instrument.pair,
            'side'          : side,
            'type'          : type,
            'units'         : int(round(units)),
            'price'         : entry,
            'stopLoss'      : stopLoss,
            'takeProfit'    : takeProfit,
            'trailingStop'  : trailingStop,
            'expiry'        : lib.helpers.epochToRfc3339(time.time() + expiry),
        }
        try:
            order = self.con.create_order(lib.oanda.Order(**dOrder))
            self._orders.append(position.Order(self, order['orderOpened']['id'], riskClosePips=riskClosePips))
            return order
        except:
            print('error creating order')


    def createTrade(self, side, units, stopLoss=None, takeProfit=None, trailingStop=None):
        if not self.active:
            return False
        if not self.order_news_allowed():
            return False

        if stopLoss:
            stopLoss = round(stopLoss, self.instrument.precision)
        if takeProfit:
            takeProfit = round(takeProfit, self.instrument.precision)
        if trailingStop:
            trailingStop = round(trailingStop, self.instrument.precision)

        dTrade = {
            'instrument'    : self.instrument.pair,
            'side'          : side,
            'type'          : 'market',
            'units'         : int(round(units)),
            'stopLoss'      : stopLoss,
            'takeProfit'    : takeProfit,
            'trailingStop'  : trailingStop,
        }
        try:
            dtrade       = self.con.create_order(lib.oanda.Order(**dTrade))
        except:
            print('error creating trade')
            
        if len(dtrade['tradeOpened']) > 0:
            self._trades.append(position.Trade(self, dtrade['tradeOpened']['id']))
        if len(dtrade['tradeReduced']) > 0:
            trade = self.trades().withID(dtrade['tradeReduced']['id']).get()
            if trade.hasNext():
                trade.next().pullDetails()
        for closedTrade in dtrade['tradesClosed']:
            trade = self.trades().withID(reducedTrade['id']).get()
            if trade.hasNext():
                trade.next().closeEvent()

    def order_news_allowed(self):
        for newsBlock in self.newsBlock:
            if newsBlock['type'] == "before":
                nTime = self.account.news.next(self.instrument.pair, newsBlock['minImportance'])
            elif newsBlock['type'] == "after":
                nTime = self.account.news.previous(self.instrument.pair, newsBlock['minImportance'])
            if not nTime == None and abs(nTime - int(time.time())) < newsBlock['time']:
                return False
        return True

    def news_close_schedule(self):
        nextClose = None
        for newsClose in self.newsClose:
            nextnewstime = self.account.news.next(self.instrument.pair, newsClose['minImportance'])
            if nextClose == None or nextnewstime < nextClose:
                nextClose = nextnewstime

        if not nextClose == None:
            interval = nextClose - time.time()
            self.newsCloseTimer = threading.Timer(interval, self.newsCloseCalled)
            self.newsCloseTimer.start()

    def newsCloseCalled(self):
        # print('news close all')
        self.closeAll()
        self.news_close_schedule()

    def appendTrade(self, trade):
        self._trades.append(trade)

    def appendOrder(self, order):
        self._orders.append(order)

    def orders(self, onlyOpen=True):
        return selector.OrderSelector(self._orders, onlyOpen)

    def trades(self, onlyOpen=True):
        return selector.TradeSelector(self._trades, onlyOpen)

    def closeAll(self):
        trades = self.trades().get()
        orders = self.orders().get()
        while trades.hasNext():
            trades.next().close()
        while orders.hasNext():
            orders.next().close()

    def start(self):
        self.active = True
        self.event("Strategy-Start", self)
        self.instrument.event("Strategy-Start", self)

    def stop(self):
        self.active = False
        self.event("Strategy-Stop", self)
        self.instrument.event("Strategy-Stop", self)

        if self.closeTradesOnStop:
            self.closeAll()

    @staticmethod
    def parseDisplayName(strategy, params):
        required = {
            'DirPredict'      : ['risk', 'tpPips', 'slPips'],
            'DirPredictRev'   : ['risk','tpPips','slPips'],
            'EmptyStrat'      : [],
            'Rejects'         : [],
            'RejectsRev'      : [],
            'Tradimo'         : [],
            'TradimoTS'         : [],
            'TradimoRR'         : [],
            'TradimoRev'         : [],
            'SmartyStrat'         : [],
        }

        dispName = strategy.__name__
        required = required[dispName]

        for req in required:
            dispName += "-" + str(req) + ':' + str(params[req])
        return dispName

    @property
    def ins(self):
        return self.instrument
    @property
    def pair(self):
        return self.ins.pair
