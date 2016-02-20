import time, datetime, pytz, calendar, threading

class Time:
    def __init__(self):
        self.timeOverride = None

        self.addedSeconds   = 0
        self.addedMinutes   = 0
        self.addedHours     = 0
        self.addedDays      = 0

    def addTime(self, days=0,hours=0,mins=0,secs=0):
        self.addedDays = days
        self.addedHours = hours
        self.addedMinutes = mins
        self.addedSeconds = secs

    def setTime(self, year=None, month=None, day=None, hour=None, minute=None, second=None):
        time = self.nowDatetime
        if year:
            time = time.replace(year=year)
        if month:
            time = time.replace(month=month)
        if day:
            time = time.replace(day=day)
        if hour:
            time = time.replace(hour=hour)
        if minute:
            time = time.replace(minute=minute)
        if second:
            time = time.replace(second=second)

        self.setTimeOverride(time)

    def stop(self):
        self.setTimeOverride(self.now)

    def setTimeOverride(self, time):
        self.timeOverride = self.timeToEpoch(time)

    def timeToEpoch(self, time):
        if time.__class__.__name__ == 'int' or time.__class__.__name__ == 'float':
            return time
        if time.__class__.__name__ == "str":
            return rfc3339toEpoch(time)
        if time.__class__.__name__ == 'datetime':
            return calendar.timegm(time.timetuple())

    @property
    def now(self):
        return self.nowEpoch

    @property
    def nowEpoch(self):
        if self.timeOverride:
            epoch = self.timeOverride
        else:
            epoch = time.time()
        epoch += self.addedSeconds
        epoch += self.addedMinutes * 60
        epoch += self.addedHours * 3600
        epoch += self.addedDays * 86400
        return epoch

    @property
    def nowRfc(self):
        timeEpoch = self.nowEpoch
        rfc = datetime.datetime.fromtimestamp(timeEpoch, tz=pytz.utc)
        return rfc.isoformat("T") + "Z"

    @property
    def nowDatetime(self):
        timeEpoch = self.nowEpoch
        return datetime.datetime.fromtimestamp(timeEpoch, tz=pytz.utc)

t = Time()
