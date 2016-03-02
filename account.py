# dependancies
import lib, instrument, news, selector
import environment.env         as env

import time, threading, sqlite3, os

class Account(lib.Event, lib.Stream):
    '''
    Account contains connection to Oanda. Also contains methods for getting
    the account balance, orders and instruments.
    '''
    def __init__(self):
        env.set_environment(0)
        self.start_time    = lib.helpers.epochToRfc3339(time.time())
        self.connections   = env.get_connections()
        self.__instruments = []

        self.start_trading()

    def start_trading(self):
        '''
        Start trading
        Usefull for when connection breaks and we want to restart
        '''
        self.news = news.News()
        for instrument_plan in env.get_trading_plan():
            ins = instrument.Instrument(self, instrument_plan)
            self.__instruments.append(ins)

        threading.Thread(target=self.stream_ticks).start()
        for con in self.connections:
            kwargs = {'con':self.connections[con]}
            threading.Thread(target=self.eventStream, kwargs=kwargs).start()

    def stop_trading(self):
        del self.news

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
        order_selector = selector.OrderSelector([])
        for instrument in self.__instruments:
            order_selector += instrument.orders()
        return order_selector

    def trades(self):
        '''
        Returns a TradeSelector instance containing all trades in account
        '''
        trade_selector = selector.TradeSelector([])
        for instrument in self.__instruments:
            trade_selector += instrument.trades()
        return trade_selector

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
            balance = self.connections[thread].get_credentials()['balance']
            if balance < 980:
                return 0.
            return float(balance)
        except:
            return 0.

    def exit(self):
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
