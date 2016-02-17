from pyoanda import *
import json

class Client(Client):
    def event_stream(self):
        url = "{0}/{1}/events".format(
            self.domain_stream,
            self.API_VERSION
        )
        params = {}

        call = {"uri": url, "params": params, "method": "get"}

        try:
            return self._Client__call_stream(**call)
        except RequestException:
            return False
        except AssertionError:
            return False

    def stream_events(self):
        resp = self.event_stream()
        for line in resp.iter_lines():
            yield json.loads(line.decode("utf-8"))

    def stream_ticks(self, instruments):
        resp = self.get_prices(instruments=instruments)
        for line in resp.iter_lines():
            yield json.loads(line.decode("utf-8"))

    def get_instrument(self, instruments, fields=None):
        url = "{0}/{1}/instruments".format(self.domain, self.API_VERSION)
        if fields == None:
            fields = "displayName,pip,maxTradeUnits,precision,maxTrailingStop,minTrailingStop,marginRate,halted,interestRate"
        params = {
            "accountId"     : self.account_id,
            "instruments"   : instruments,
            "fields"        : fields
        }
        try:
            response = self._Client__call(uri=url, params=params)
            assert len(response) > 0
            return response
        except AssertionError:
            return False
