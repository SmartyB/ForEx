import lib
import datetime, pytz
from position.trade import Trade
from lib.database import DataBase

class Order(lib.Event, DataBase):
    def __init__(self, strategy, id, riskClosePips=None):
        self.id             = id
        self.strategy       = strategy
        self.strategy_name  = strategy.displayName
        self.con            = self.strategy.con

        self.instrument = self.strategy.instrument
        self.pair       = self.instrument.pair

        # print("Order - {0}, {1}, {2}".format(id, self.pair, self.strategy_name))

        self.time       = datetime.datetime.now(tz=pytz.utc)
        self.year       = self.time.year
        self.month      = self.time.month
        self.day        = self.time.day
        self.weekday    = lib.definitions.days[self.time.weekday()]
        self.hour       = self.time.hour
        self.minute     = self.time.minute
        self.second     = self.time.second

        # self.type = 'stop'
        self.risk_remove_pips   = riskClosePips

        self.entry_price = self.stopLoss = self.takeProfit = self.trailingStop = None

        self.pull_details()

        self.open = True
        self.trade = None

        self.load_from_db()
        self.store_to_db()

    def pull_details(self):
        try:
            details = self.con.get_order(self.id)
        except:
            return
        if details['takeProfit'] == 0:
            details['takeProfit'] = None
        if details['stopLoss'] == 0:
            details['stopLoss'] = None
        if details['trailingStop'] == 0:
            details['trailingStop'] = None

        self.side = details['side']
        self.entry_price = details['price']
        self.units = details['units']
        self.takeProfit = details['takeProfit']
        self.stopLoss = details['stopLoss']
        self.trailingStop = details['trailingStop']
        self.expiry = lib.helpers.timeToEpoch(details['expiry'])

    def close(self):
        try:
            self.open = False
            self.con.close_order(self.id)
            self.store_to_db()
        except:
            pass

    def closeEvent(self):
        self.open = False
        self.store_to_db()

    def update(self, entry=None, stopLoss=None, takeProfit=None, trailingStop=None):
        update = False
        if entry and not entry == self.entry_price:
            update = True
            self.entry_price = round(entry, self.instrument.precision)
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
            elif self.side == 'sell' and takeProfit > self.instrument.ask:
                self.close()
                return
        if trailingStop and not trailingStop == self.trailingStop:
            update = True
            self.trailingStop = trailingStop

        if update:
            order = lib.oanda.Order(**{
                'instrument'    : self.instrument.pair,
                'side'          : self.side,
                # 'type'          : self.type,
                'units'         : self.units,
                'price'         : self.entry_price,
                'stopLoss'      : self.stopLoss,
                'takeProfit'    : self.takeProfit,
                'trailingStop'  : self.trailingStop,
                'expiry'        : lib.helpers.epochToRfc3339(self.expiry)
            })
            try:
                self.con.update_order(self.id, order)
            except:
                self.closeEvent()


    def fill(self, dOrder):
        self.open = False
        id = dOrder['tradeOpened']['id']
        trade = Trade(self.strategy, id, riskClosePips=self.risk_remove_pips, order=self)
        self.strategy.appendTrade(trade)

        self.trade = trade
        self.trade_id = trade.id

        self.store_to_db()
