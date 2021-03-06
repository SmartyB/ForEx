import sqlite3
import threading

class Stream:
    def tickStream(self):
        self.unprocessed_ticks = 0
        self.tickDB = sqlite3.connect('database/db.db')
        for tick in self.connections['t1'].stream_ticks(instruments=",".join(self.active_instruments())):
            if 'tick' in tick:
                self.unprocessed_ticks += 1
                instruments = self.instruments().withPair(tick['tick']['instrument']).get()
                while(instruments.hasNext()):
                    # use threading for when a lot of ticks come at once
                    threading.Thread(target=instruments.next().tick, kwargs={'tick':tick['tick']}).start()
                self.unprocessed_ticks -= 1
                # self.writeTick2DB(tick['tick'])

                if self.unprocessed_ticks > 10:
                    print('ticks backlog alert')

    def writeTick2DB(self, tick):
        try:
            tick = (tick['instrument'], tick['time'], tick['bid'], tick['ask'])
            c = self.tickDB.cursor()
            c.execute("INSERT INTO `ticks`(instrument, time, bid, ask) VALUES \
                (?,?,?,?)", tick)
            self.tickDB.commit()
        except:
            pass

    def eventStream(self, con):
        for event in con.stream_events():
            if 'transaction' in event:
                ev = event['transaction']
                if ev['type'] == 'ORDER_FILLED':
                    # print("Order id {0} filled".format(ev['orderId']))
                    order = self.orders().withID(ev['orderId']).get()
                    if not order.hasNext():
                        print('No order for order id {0}'.format(ev['orderId']))
                    if order.hasNext():
                        order.next().fill(ev)
                elif ev['type'] == 'ORDER_UPDATE':
                    pass
                elif ev['type'] == 'ORDER_CANCEL':
                    order = self.orders().withID(ev['orderId']).get()
                    if order.hasNext():
                        order.next().closeEvent()
                elif ev['type'] == 'TRADE_CLOSE':
                    trade = self.trades().withID(ev['id']).get()
                    if trade.hasNext():
                        trade.next().closeEvent()
                elif ev['type'] == 'STOP_LOSS_FILLED':
                    trade = self.trades().withID(ev['tradeId']).get()
                    if trade.hasNext():
                        trade.next().stopLossFilled(ev)
                elif ev['type'] == 'MARKET_ORDER_CREATE':
                    pass
                elif ev['type'] == 'MARKET_IF_TOUCHED_ORDER_CREATE':
                    pass
                elif ev['type'] == "TAKE_PROFIT_FILLED":
                    trade = self.trades().withID(ev['tradeId']).get()
                    if trade.hasNext():
                        trade.next().takeProfitFilled(ev)
                elif ev['type'] == "TRANSFER_FUNDS":
                    pass
                elif ev['type'] == "DAILY_INTEREST":
                    pass
                elif ev['type'] == 'LIMIT_ORDER_CREATE':
                    pass
                elif ev['type'] == 'STOP_ORDER_CREATE':
                    pass
                elif ev['type'] == "TRAILING_STOP_FILLED":
                    trade = self.trades().withID(ev['tradeId']).get()
                    if trade.hasNext():
                        trade.next().trailingStopFilled(ev)
                elif ev['type'] == "TRADE_UPDATE":
                    # trade = self.trades().withID(ev['tradeId']).get()
                    pass
                    # print(ev)
                    # if trade.hasNext():
                        # trade.next().tradeUpdate(ev)
                else:
                    print(ev)
