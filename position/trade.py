import lib
import sqlite3, datetime, pytz, time
from lib.database import DataBase

class Trade(lib.Event, DataBase):
    def __init__(self, strategy,  id, store=True, riskClosePips=None, order=None):
        self.order = order
        self.strategy = strategy
        self.strategy_name = strategy.displayName

        self.instrument = strategy.instrument
        self.pair = self.instrument.pair
        self.con = self.strategy.con

        # print("Trade - {0}, {1}, {2}".format(id, self.pair, self.strategy_name))

        self.id = id

        self.time       = datetime.datetime.now(tz=pytz.utc)
        self.entry_time = lib.helpers.datetimeToRfc3339(self.time)
        self.exit_time  = None

        self.year       = self.time.year
        self.month      = self.time.month
        self.day        = self.time.day
        self.weekday    = lib.definitions.days[self.time.weekday()]
        self.hour       = self.time.hour
        self.minute     = self.time.minute
        self.second     = self.time.second

        self.side = self.entry_price = self.exit_price = self.takeProfit = None
        self.stopLoss = self.trailingStop = self.max_profit_pips         = None
        self.min_profit_pips = self.time_since_order                     = None

        self.units = 0
        self.risk_remove_pips = riskClosePips

        if order:
            self.time_since_order = int((self.time - self.order.time).total_seconds())

        self.pullDetails()
        self.open = True

        self.load_from_db()
        self.store_to_db()

        self.tickListener = self.instrument.on('Candle-Tick', self.tick)

    def tick(self, candle=None, data=None):
        if self.risk_remove_pips:
            self.remove_risk()

        profit = self.profitPips
        if self.max_profit_pips == None or profit > self.max_profit_pips:
            self.max_profit_pips = profit

        if self.min_profit_pips == None or profit < self.min_profit_pips:
            self.min_profit_pips = profit

    def remove_risk(self):
        profit_pips = self.profitPips
        if profit_pips > self.risk_remove_pips:
            if not self.stopLoss:
                self.update(stopLoss=self.entry_price)
            elif self.side == "buy" and self.entry_price > self.stopLoss:
                self.update(stopLoss=self.entry_price)
            elif self.side == "sell" and self.entry_price < self.stopLoss:
                self.update(stopLoss=self.entry_price)

    def pullDetails(self):
        try:
            details = self.con.get_trade(self.id)
        except:
            return
        self.side = details['side']
        self.entry_price = details['price']
        self.units = details['units']
        if not details['takeProfit'] == 0:
            self.takeProfit = details['takeProfit']
        if not details['stopLoss'] == 0:
            self.stopLoss = details['stopLoss']
        if not details['trailingAmount'] == 0:
            self.trailingStop = details['trailingAmount']

    def close(self):
        dEvent = self.con.close_trade(self.id)

        self.profit_total = dEvent['profit']
        self.exit_price = dEvent['price']

        self.exit()

    def exit(self):
        self.open = False
        self.profit_pips = self.profitPips

        time = datetime.datetime.now(tz=pytz.utc)
        self.exit_time = lib.helpers.datetimeToRfc3339(time)

        self.store_to_db()
        self.instrument.removeListener(self.tickListener)

    def closeEvent(self):
        self.open = False
        self.instrument.removeListener(self.tickListener)

    def update(self, stopLoss=None, takeProfit=None, trailingStop=None):
        update = False
        if stopLoss and not stopLoss == self.stopLoss:
            update = True
            self.stopLoss = round(stopLoss, self.instrument.precision)

            if self.side == 'buy' and stopLoss > self.instrument.bid:
                self.close()
                return
            elif self.side == 'sell' and stopLoss < self.instrument.ask:
                self.close()
                return
        if takeProfit and not takeProfit == self.takeProfit:
            update = True
            self.takeProfit = round(takeProfit, self.instrument.precision)

            if self.side == 'buy' and takeProfit < self.instrument.bid:
                self.close()
                return
            if self.side == 'sell' and takeProfit > self.instrument.ask:
                self.close()
                return

        if trailingStop and not trailingStop == self.trailingStop:
            update = True
            self.trailingStop = trailingStop

        if update:
            try:
                self.con.update_trade(
                    trade_id = self.id,
                    stop_loss = self.stopLoss,
                    take_profit = self.takeProfit,
                    )
            except:
                self.closeEvent()

    def stopLossFilled(self, dTrade):
        self.exit_price = dTrade['price']
        self.profit_total = dTrade['pl']
        self.profit_pips = self.profitPips

        self.exit()

    def takeProfitFilled(self, dTrade):
        self.exit_price = dTrade['price']
        self.profit_total = dTrade['pl']
        self.profit_pips = self.profitPips

        self.exit()

    def trailingStopFilled(self, dTrade):
        self.exit_price = dTrade['price']
        self.profit_total = dTrade['pl']
        self.profit_pips = self.profitPips

        self.exit()

    @property
    def profitPips(self):
        try:
            if not self.open:
                if self.side == "buy":
                    return (self.exit_price - self.entry_price) / self.instrument.pip
                elif self.side == "sell":
                    return (self.entry_price - self.exit_price) / self.instrument.pip
            else:
                if self.side == "buy":
                    return (self.instrument.bid - self.entry_price) / self.instrument.pip
                elif self.side == "sell":
                    return (self.entry_price - self.instrument.ask) / self.instrument.pip
        except TypeError as e:
            print('Error getting trade profit: <{0}>'.format(e))
            return -99999999999999999
