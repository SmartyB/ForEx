# from trading_plan import trading_plan

import lib.connections          as connections
import lib.helpers              as helpers

import lib, instrument, news
import trading_plan, selector
import time, threading, sqlite3
import os

from lib.connections import *

class Account(lib.Event, lib.Stream):
    '''
    Account contains connection to Oanda. Also contains methods for getting
    the account balance, orders and instruments.
    '''
    def __init__(self):
        self.start_time    = helpers.epochToRfc3339(time.time())
        self.connections   = connections
        self.__instruments = []

        self.start_trading()

    def start_trading(self):
        '''
        Start trading
        Usefull for when connection breaks and we want to restart
        '''
        self.news = news.News()
        for instrument_plan in trading_plan.plan:
            ins = instrument.Instrument(self, instrument_plan)
            self.__instruments.append(ins)

        threading.Thread(target=self.stream_ticks).start()
        for con in self.connections:
            kwargs = {'con':self.connections[con]}
            threading.Thread(target=self.eventStream, kwargs=kwargs).start()

    def stop_trading(self):
        self.news = None

        # the next line does not seem to free memory, we still need to really
        # delete the instances
        self.__instruments[:] = []

    def strategies(self):
        '''
        Returns a StrategySelector instance containing all strategies in account
        '''
        strat_selector = selector.StrategySelector([])
        for instrument in self.__instruments:
            strat_selector += instrument.strategies()
        return strat_selector

    def orders(self):
        '''
        Returns an OrderSelector instance containing all orders in account
        '''
        orderSelector = selector.OrderSelector([])
        for instrument in self.__instruments:
            orderSelector += instrument.orders()
        return orderSelector

    def trades(self):
        '''
        Returns a TradeSelector instance containing all trades in account
        '''
        tradeSelector = selector.TradeSelector([])
        for instrument in self.__instruments:
            tradeSelector += instrument.trades()
        return tradeSelector

    def active_instruments(self):
        '''
        Returns an array of unique instruments we are trading
        '''
        instruments = []
        for instrument in self.__instruments:
            if instrument.pair not in instruments:
                instruments.append(instrument.pair)
        return instruments

    def get_balance(self, thread):
        '''
        Returns available balance in our (sub)account. Returns 0 if it excepts
        '''
        try:
            return float(self.connections[thread].get_credentials()['balance'])
        except:
            return 0.

    def stop(self):
        '''
        Controlled stopping. Saves all Trade and Order instances to db, then
        forces exit. This has to be forced because of threading.Timer instances
        '''
        orders = self.orders().get()
        trades = self.trades().get()
        while orders.hasNext():
            orders.next().store_to_db()
        while trades.hasNext():
            trades.next().store_to_db()
        os._exit(0)


    def instruments(self):  return selector.InstrumentSelector(self.__instruments)
    def ins(self, pair):    return self.instruments().withPair(pair).get().next()
    def num_orders(self):   return self.orders().get().length()
    def num_trades(self):   return self.trades().get().length()

    #shorthand
    def nt(self): return self.num_trades()
    def no(self): return self.num_orders()

# initiate
a = Account()

# set some variables for easy access
i = a.ins('eur_usd')
s = i.strategies().get().next()
