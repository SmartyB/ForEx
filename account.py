from strategy import *
from selector import *

import lib, instrument, news
import time, threading, sqlite3
import os

from timer import *
from lib.connections import *


class Account(lib.Event, lib.Stream):
    '''
    Account contains connection to Oanda. Also contains methods for getting
    the account balance, orders and instruments.
    '''
    def __init__(self):
        self.start = lib.helpers.epochToRfc3339(time.time())
        self.__instruments     = []
        self.connections = connections

        self.load()

    def load(self):
        self.news = news.News()
        for dIns in lStrategy:
            self.__instruments.append(instrument.Instrument(self, dIns))

        threading.Thread(target=self.tickStream).start()
        for con in self.connections:
            threading.Thread(target=self.eventStream, kwargs={'con':self.connections[con]}).start()

    def unload(self):
        self.news = None
        self.__instruments[:] = []

    def strategies(self):
        strat_selector = selector.StrategySelector([])
        for instrument in self.__instruments:
            strat_selector += instrument.strategies()
        return strat_selector

    def orders(self):
        orderSelector = selector.OrderSelector([])
        for instrument in self.__instruments:
            orderSelector += instrument.orders()
        return orderSelector

    def trades(self):
        tradeSelector = selector.TradeSelector([])
        for instrument in self.__instruments:
            tradeSelector += instrument.trades()
        return tradeSelector

    def active_instruments(self):
        '''
        returns a list of unique instruments
        '''
        instruments = []
        for instrument in self.__instruments:
            if instrument.pair not in instruments:
                instruments.append(instrument.pair)
        return instruments

    def get_balance(self, thread):
        '''
        returns available balance in our (sub)account. Returns 0 if error
        '''
        try:
            return float(self.connections[thread].get_credentials()['balance'])
        except:
            return 0.

    def stop(self):
        '''
        Controlled stopping
        '''
        orders = self.orders().get()
        trades = self.trades().get()
        while orders.hasNext():
            orders.next().store_to_db()
        while trades.hasNext():
            trades.next().store_to_db()
        os._exit(0)

    def instruments(self):  return InstrumentSelector(self.__instruments)
    def ins(self, pair):    return self.instruments().withPair(pair).get().next()
    def num_orders(self):   return self.orders().get().length()
    def num_trades(self):   return self.trades().get().length()

    #shorthand
    def nt(self): return self.num_trades()
    def no(self): return self.num_orders()


def to():
    s.createOrder('buy',1,i.ask+0.00001)
    s.createOrder('sell',1,i.bid-0.00001)


a = Account()
i = a.ins('eur_usd')
s = a.strategies().get().next()
# s = a.instruments().withPair('gbp_usd').get().next().strategies().get().next()
