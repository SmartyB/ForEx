import sqlite3
import threading
import time

class Stream:
    def stream_ticks(self):
        self.unprocessed_ticks = 0
        for tick in self.connections['t1'].stream_ticks(instruments=",".join(self.active_instruments())):
            if 'tick' in tick:
                self.unprocessed_ticks += 1
                instruments = self.instruments().withPair(tick['tick']['instrument']).get()
                while(instruments.hasNext()):
                    # use threading for when a lot of ticks come at once
                    threading.Thread(target=instruments.next().tick, kwargs={'tick':tick['tick']}).start()
                self.unprocessed_ticks -= 1

                if self.unprocessed_ticks > 10:
                    print('ticks backlog alert')

    def eventStream(self, con):
        for event in con.stream_events():
            if 'transaction' in event:
                ev = event['transaction']
                if ev['type'] == 'ORDER_FILLED':
                    time.sleep(1)
                    order = self.orders().withID(ev['orderId']).get()
                    if order.hasNext():
                        order.next().fill(ev)
                elif ev['type'] == 'ORDER_UPDATE':
                    print({1:ev})
                    # pass
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
                    print({5:ev})
                    # pass
                elif ev['type'] == 'MARKET_IF_TOUCHED_ORDER_CREATE':
                    print({6:ev})
                    # pass
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
                    print({8:ev})
                    # pass
                elif ev['type'] == "TRAILING_STOP_FILLED":
                    print({9:ev})
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
