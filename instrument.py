# dependancies
import math, sqlite3, pyoanda

import lib, position, selector, chart

class Instrument(lib.Event):
    def __init__(self, account, instrument):
        self.account      = account

        # we can use any connection for getting candle values
        self.con          = account.connections["t1"]

        self.pair         = instrument['pair']
        self.base         = self.pair.split('_')[0]
        self.quote        = self.pair.split('_')[1]
        self.get_instrument_data()

        self.__charts       = {}
        self.__strategies   = []

        self.initiate_strategies(instrument['strategy'])

        # load open orders and trades
        self.load_trades()
        self.load_orders()

        for strategy in self.__strategies:
            strategy.begin()

    def initiate_strategies(self, strategies):
        '''
        Create the desired Strategy instances
        '''
        for strategy in strategies:
            strat = strategy['name'](self, strategy)
            self.__strategies.append(strat)

    def tick(self, tick):
        '''
        Send ticks to the active charts
        '''
        self.bid = tick['bid']
        self.ask = tick['ask']
        for gran in self.__charts:
            self.__charts[gran].tick(tick)

    def chart(self, gran):
        '''
        Returns the Chart instance defined by the granularity gran
        Creates the instance if it does not yet exist.
        '''
        gran = gran.upper()
        try:
            # asking for forgiveness is better than asking for permission
            return self.__charts[gran]
        except KeyError:
            self.__charts[gran] = chart.Chart(self, gran)
            return self.__charts[gran]

    def orders(self):
        '''
        Returns an OrderSelector instance containing all orders in the instrument
        '''
        order_selector = selector.OrderSelector([])
        for strategy in self.__strategies:
            order_selector += strategy.orders()
        return order_selector

    def trades(self):
        '''
        Returns a TradeSelector instance containing all trades in the intrument
        '''
        trade_selector = selector.TradeSelector([])
        for strategy in self.__strategies:
            trade_selector += strategy.trades()
        return trade_selector

    def strategies(self):
        '''
        Returns a StrategySelector insance containing all strategies in intrument
        '''
        return selector.StrategySelector(self.__strategies)

    def load_trades(self):
        '''
        UGLY
        Methods that tries to reload trades that are open according to Oanda.
        Usefull in production when the connection interupts.
        Usefull in development for obvious reasons
        '''
        db = lib.database.DataBase()

        # get all open trades for this instrument
        open_trades = []
        for con in self.account.connections.values():
            open_trades += con.get_trades(instrument=self.pair)['trades']

        for open_trade in open_trades:
            trade_id = open_trade['id']

            # see if we have this trade in our db
            db_trade = db.get_from_db('trades', 'id', trade_id)
            if not db_trade:
                continue

            # see if this strategy is still active
            strat_name = db_trade['strategy_name']
            strat_itterator = self.strategies().withDisplayName(strat_name).get()
            if not strat_itterator.hasNext():
                continue
            strat = strat_itterator.next()

            # load the trade
            trade = position.Trade(strat, trade_id)
            strat.appendTrade(trade)

    def load_orders(self):
        '''
        UGLY
        Methods that tries to reload orders that are open according to Oanda.
        Usefull in production when the connection interupts.
        Usefull in development for obvious reasons
        '''
        db = lib.database.DataBase()

        # get all open orders
        open_orders = []
        for con in self.account.connections.values():
            open_orders += con.get_orders(instrument=self.pair)['orders']
        for open_order in open_orders:
            order_id = open_order['id']

            # see if we can find the order in our db
            db_order = db.get_from_db('orders', 'id', order_id)
            if not db_order:
                continue

            # see if we can find the strategy in self.
            strat_name = db_order['strategy_name']
            strat_itterator = self.strategies().withDisplayName(strat_name).get()
            if not strat_itterator.hasNext():
                continue

            # load the orders
            strat = strat_itterator.next()
            order = position.Order(strat, order_id)
            strat.appendOrder(order)

    def get_instrument_data(self):
        '''
        Loads some random data about the instrument from Oanda.
        Pipsize is quite important
        '''
        instrumentData = self.con.get_instrument(instruments=self.pair)['instruments'][0]

        self.precision    = round(math.log(1/float(instrumentData['precision']),10))
        self.pip          = float(instrumentData['pip'])
        self.displayName  = instrumentData['displayName']
        self.interest     = instrumentData['interestRate']
        self.marginRate   = instrumentData['marginRate']
        self.maxTradeUnits    = instrumentData['maxTradeUnits']
        self.maxTrailingStop  = instrumentData['maxTrailingStop']
        self.minTrailingStop  = instrumentData['minTrailingStop']

    def eurToQuote(self):
        '''
        Method that calculates our account balance in terms of the quote currency
        '''
        try:
            rate = self.con.get_prices(instruments="EUR_"+self.quote, stream=False)
        except pyoanda.exceptions.BadRequest:
            rate = self.con.get_prices(instruments=self.quote+"_EUR", stream=False)
        return float(rate['prices'][0]['bid'])

    @property
    def spread(self): return self.ask - self.bid

    def num_trades(self): return self.trades().get().length()
    def num_orders(self): return self.orders().geT().length()

    #shorthand
    def nt(self): return self.num_trades()
    def no(self): return self.num_orders()
