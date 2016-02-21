import httplib2
import datetime as dt
import threading
from dateutil import parser
import time, pytz
from bs4 import *
from lib.event import Event
import sqlite3
import calendar
from lib.helpers import *

def downloadFile(URL=None):
    h = httplib2.Http(".cache")
    resp, content = h.request(URL, "GET")
    return content

importanceKey = ['Not significant', 'Low', 'Medium', 'High']
class News(Event):
    def __init__(self):
        self.getNewsItems()

    def getNewsItems(self):
        feed = downloadFile("http://www.roboforex.com/analytics/economic-calendar/rss/")
        feed = BeautifulSoup(feed, "html.parser")

        db = sqlite3.connect('../database/testing.db')
        c = db.cursor()
        for item in feed.findAll("item"):
            time = parser.parse(item.pubdate.string)
            time = calendar.timegm(time.timetuple())
            title = item.title.string.strip()

            importance = 0

            for row in item.description.contents:
                if row.startswith(" Importance:"):
                    importance = row.replace(" Importance: ", "")
                    importance = importanceKey.index(importance.strip())
                elif row.startswith(" Currency:"):
                    currency = row.replace(" Currency: ", "").replace("<br/>", "").strip().lower()

            c.execute("SELECT * FROM `news` WHERE `time`={0} AND `currency`='{1}' AND `importance` = {2}".format(time, currency, importance))
            if c.fetchone() == None:
                c.execute("INSERT INTO `news`(time, currency, importance) VALUES({0},'{1}',{2})".format(time, currency, importance))

        db.commit()

        # self.__timer = threading.Timer(3600, self.getNewsItems)
        # self.__timer.start()

    def next(self, pair, minImportance):
        currencies = pair.lower().split("_")
        db = sqlite3.connect('../database/testing.db')
        c = db.cursor()
        q = "SELECT `time` FROM `news` WHERE `time` >= {0} AND `currency` IN ('{1}','{2}') AND `importance` >= {3} ORDER BY `time` ASC".format(int(time.time()), currencies[0], currencies[1], minImportance)
        c.execute("SELECT `time` FROM `news` WHERE `time` >= {0} AND `currency` IN ('{1}','{2}') AND `importance` >= {3} ORDER BY `time` ASC".format(int(time.time()), currencies[0], currencies[1], minImportance))
        try:
            return c.fetchone()[0]
        except:
            return None

    def previous(self, pair, minImportance):
        currencies = pair.lower().split("_")
        db = sqlite3.connect('../database/testing.db')
        c = db.cursor()
        c.execute("SELECT `time` FROM `news` WHERE `time` <= {0} AND `currency` IN ('{1}','{2}') AND `importance` >= {3} ORDER BY `time` DESC".format(int(time.time()), currencies[0], currencies[1], minImportance))
        try:
            return c.fetchone()[0]
        except:
            return None
