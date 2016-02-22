import json
import datetime as dt
import calendar
import pytz
import pyoanda as oanda
import threading, time
import os
import lib
import sqlite3

import lib.scheduler as scheduler

def min(a,b):
    if a == None and b == None:
        return None

    if a == None: return b
    if b == None: return a
    if b < a: return b
    if a < b: return a
    return a

def max(a,b):
    if a == None and b == None:
        return None

    if a == None: return b
    if b == None: return a
    if b > a: return b
    if a > b: return a
    return a

def unixRepr(unix):
    string = ''
    time = dt.datetime.fromtimestamp(unix, tz=pytz.utc)
    string += lib.definitions.days[time.weekday()]
    string += ' ' + str(time.hour) + ':' + str(time.minute)


def rfc3339toEpoch(rfc3339):
    date = dt.datetime.strptime(rfc3339, '%Y-%m-%dT%H:%M:%S.%fZ')
    return calendar.timegm(date.timetuple())

def epochToRfc3339(epoch):
    rfc = dt.datetime.fromtimestamp(epoch, tz=pytz.utc)
    return rfc.isoformat("T") + "Z"

def epochToRfc3339_2(epoch):
    rfc = dt.datetime.fromtimestamp(epoch, tz=pytz.utc)
    return rfc.isoformat("T") + "Z"

def datetimeToRfc3339(date):
    return date.isoformat("T") + "Z"

def inTimeRange(range):
    start = scheduler.getDateTime(range['start'])
    end = scheduler.getDateTime(range['end'])
    return end < start

def timeToEpoch(time):
    if time.__class__.__name__ == 'int':
        return time
    if time.__class__.__name__ == "str":
        return rfc3339toEpoch(time)
    if time.__class__.__name__ == 'datetime':
        return calendar.timegm(time.timetuple())


def prevWorkDayStart():
    today = dt.datetime.combine(dt.date.today(), dt.datetime.min.time())
    yesterday = today - dt.timedelta(days=1)
    if yesterday.weekday() == 6:
        yesterday = yesterday - dt.timedelta(days=2)
    elif yesterday.weekday() == 5:
        yesterday = yesterday - dt.timedelta(days=1)

    return calendar.timegm(yesterday.timetuple())

def beep():
    import sys
    sys.stdout.write('\a')

def printDirs(account):
    inss = account.instruments().get()
    while inss.hasNext():
        ins = inss.next()
        strat = ins.strategies().get().next()
        print(ins.pair + ' ' + str(strat.dir))

def tick(a):
    ins = a.instruments().get().next()
    chart = ins.chart('m5')
    t = time.time()
    t = lib.helpers.epochToRfc3339_2(t).replace('+00','').replace(':00Z', '.00Z')
    ins.tick({'bid':1, 'ask':2, 'time': t})

clear = lambda: os.system('cls')
