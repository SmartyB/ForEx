import lib
import threading, time, pytz
import datetime as dt
import calendar

class Pivots(lib.Event):
    def __init__(self, instrument):
        self.instrument = instrument
        self.con        = self.instrument.con

        self.m1pivot = M1Pivot(self)
        self.r1pivot = R1Pivot(self)
        self.r2pivot = R2Pivot(self)
        self.r3pivot = R3Pivot(self)
        self.s1pivot = S1Pivot(self)
        self.s2pivot = S2Pivot(self)
        self.s3pivot = S3Pivot(self)

        self.determinePivots()

    def determinePivots(self):
        try:
            yesterday = self.con.get_instrument_history(
                instrument      = self.instrument.pair,
                count           = 2,
                candle_format   = 'bidask',
                granularity     = 'D',
                daily_alignment  = 23,
                alignment_timezone = 'Europe/Amsterdam',
            )['candles'][0]
        except:
            return
        self.high   = yesterday['highBid']
        self.low    = yesterday['lowBid']
        self.close  = yesterday['closeBid']

        self.m1pivot.update()
        self.r1pivot.update()
        self.r2pivot.update()
        self.r3pivot.update()
        self.s1pivot.update()
        self.s2pivot.update()
        self.s3pivot.update()

        updateTime = dt.datetime.now(tz=pytz.utc).replace(hour=0, minute=0, second=0)
        while updateTime < dt.datetime.now(tz=pytz.utc):
            updateTime += dt.timedelta(days=1)

        updateTimer = calendar.timegm(updateTime.timetuple()) - time.time()
        threading.Timer(round(updateTimer,0), self.determinePivots).start()
        self.event('Pivots-Update', self)

    def nextAbove(self, value, offSet):
        if self.s3pivot.value > value + offSet:
            return self.s3pivot
        if self.s2pivot.value > value + offSet:
            return self.s1pivot
        if self.s1pivot.value > value + offSet:
            return self.s1pivot
        if self.m1pivot.value > value + offSet:
            return self.m1pivot
        if self.r1pivot.value > value + offSet:
            return self.r1pivot
        if self.r2pivot.value > value + offSet:
            return self.r2pivot
        if self.r3pivot.value > value + offSet:
            return self.r3pivot

    def nextBelow(self, value, offSet):
        if self.r3pivot.value < value - offSet:
            return self.r3pivot
        if self.r2pivot.value < value - offSet:
            return self.r2pivot
        if self.r1pivot.value < value - offSet:
            return self.r1pivot
        if self.m1pivot.value < value - offSet:
            return self.m1pivot
        if self.s1pivot.value < value - offSet:
            return self.s1pivot
        if self.s2pivot.value < value - offSet:
            return self.s2pivot
        if self.s3pivot.value < value - offSet:
            return self.s3pivot

class Pivot:
    def __init__(self, pivots):
        self.pivots = pivots

class M1Pivot(Pivot):
    def update(self):
        self.value = ( self.pivots.high + self.pivots.low + self.pivots.close ) / 3

class R1Pivot(Pivot):
    def update(self):
        self.value = 2 * self.pivots.m1pivot.value - self.pivots.low

class R2Pivot(Pivot):
    def update(self):
        self.value = self.pivots.m1pivot.value - self.pivots.low + self.pivots.high

class R3Pivot(Pivot):
    def update(self):
        self.value = self.pivots.high + 2*(self.pivots.m1pivot.value - self.pivots.low)

class S1Pivot(Pivot):
    def update(self):
        self.value = 2 * self.pivots.m1pivot.value - self.pivots.high

class S2Pivot(Pivot):
    def update(self):
        self.value = self.pivots.m1pivot.value + self.pivots.low - self.pivots.high

class S3Pivot(Pivot):
    def update(self):
        self.value = self.pivots.low - 2*(self.pivots.high - self.pivots.m1pivot.value)
