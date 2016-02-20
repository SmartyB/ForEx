import time, datetime, pytz, calendar, threading

class Scheduler:
    def __init__(self):
        self.active = False
        self.activeSchedule = None
        self.schedule()

    def start(self):
        self.active = True
    def stop(self):
        self.active = False

    def next(self, timeString):
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

        wntdDay = timeString.split(' ')[0].lower()
        wntdTime = timeString.split(' ')[1].split(':')
        wntdHour = int(wntdTime[0])
        wntdMin  = int(wntdTime[1])
        wntdSec  = int(wntdTime[2])

        time = datetime.datetime.now(tz=pytz.utc)

        if wntdDay == 'daily':
            acceptedDays = days
        elif wntdDay == 'dailywork':
            acceptedDays = days[:5]
        else:
            acceptedDays = [wntdDay]

        time = time.replace(hour=wntdHour, minute=wntdMin, second=wntdSec)
        if time < datetime.datetime.now(tz=pytz.utc):
            time += datetime.timedelta(days=1)

        while not days[time.weekday()] in acceptedDays:
            time += datetime.timedelta(days=1)
        return time

    def in_schedule(self, scheduleStart, scheduleEnd):
        start = self.next(scheduleStart)
        end = self.next(scheduleEnd)

        return start > end

    def schedule(self):
        if len(self._schedule) == 0:
            self.start()
        for sched in self._schedule:
            if self.in_schedule(sched['start'], sched['end']):
                if not self.active:
                    self.activeSchedule = sched
                    self.start()
                    endTime = self.next(sched['end'])
                    endTime = calendar.timegm(endTime.timetuple()) + 1
                    threading.Timer(endTime - time.time(), self.schedule).start()
                    return

        if self.activeSchedule:
            self.stop()

        nextSched = None
        for sched in self._schedule:
            if nextSched == None or self.next(sched['start']) < nextSched:
                nextSched = self.next(sched['start'])
        startTime = calendar.timegm(nextSched.timetuple()) + 1
        threading.Timer(startTime - time.time(), self.schedule).start()
