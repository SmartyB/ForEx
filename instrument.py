import math, sqlite3

import lib, position, selector
from chart.chart import Chart

import database.database

class Instrument(lib.Event):
    def __init__(self, account, instrument):
        self.account      = account
        self.con          = account.connections['t1']

        self.pair         = instrument['pair']
        self.base         = self.pair.split('_')[0]
        self.quote        = self.pair.split('_')[1]
        self.get_instrument_data()

        self.__charts       = {}

        self.__strategies   = []
        self.initStrategies(instrument['strategy'])

        self.load_trades()
        self.loadOrders()

        for strategy in self.__strategies:
            strategy.begin()

    def initStrategies(self, strategies):
        for strategy in strategies:
            self.__strategies.append(strategy['name'](self, strategy))

    def tick(self, tick):
        self.bid = tick['bid']
        self.ask = tick['ask']
        for gran in self.__charts:
            self.__charts[gran].tick(tick)

    def chart(self, gran):
        try:
            return self.__charts[gran.upper()]
        except KeyError:
            self.__charts[gran] = Chart(self, gran)
            return self.__charts[gran]

    def orders(self):
        orderSelector = selector.OrderSelector([])
        for strategy in self.__strategies:
            orderSelector += strategy.orders()
        return orderSelector

    def trades(self):
        tradeSelector = selector.TradeSelector([])
        for strategy in self.__strategies:
            tradeSelector += strategy.trades()
        return tradeSelector

    def strategies(self):
        return selector.StrategySelector(self.__strategies)

    def load_trades(self):
        db = database.database.DataBase()

        open_trades = []
        for con in self.account.connections.values():
            open_trades += con.get_trades(instrument=self.pair)['trades']
        for open_trade in open_trades:
            trade_id = open_trade['id']
            db_trade = db.get_from_db('trades', 'id', trade_id)
            if not db_trade:
                # print('no trade')
                continue
            strat_name = db_trade['strategy_name']
            strat_itterator = self.strategies().withDisplayName(strat_name).get()
            if not strat_itterator.hasNext():
                # print('strategy no longer active')
                continue
            strat = strat_itterator.next()
            trade = position.Trade(strat, trade_id)
            strat.appendTrade(trade)

    def loadOrders(self):
        db = database.database.DataBase()

        open_orders = []
        for con in self.account.connections.values():
            open_orders += con.get_orders(instrument=self.pair)['orders']
        for open_order in open_orders:
            order_id = open_order['id']
            db_order = db.get_from_db('orders', 'id', order_id)
            if not db_order:
                continue
            strat_name = db_order['strategy_name']
            strat_itterator = self.strategies().withDisplayName(strat_name).get()
            if not strat_itterator.hasNext():
                continue
            strat = strat_itterator.next()
            order = position.Order(strat, order_id)
            strat.appendOrder(order)

    def get_instrument_data(self):
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
        # need this to calculate our account balance in quote currency
        try:
            rate = self.con.get_prices(instruments="EUR_"+self.quote, stream=False)
        except BadRequest:
            rate = self.con.get_prices(instruments=self.quote+"_EUR", stream=False)
        return float(rate['prices'][0]['bid'])

    @property
    def spread(self):
        return self.ask - self.bid
