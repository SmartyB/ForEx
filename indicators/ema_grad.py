from lib.helpers import *
import indicators
from indicators.indicator import *

class EmaGrad(Indicator):
    def __init__(self, chart, period, **kwargs):
        print('emagrad')
        self.period = period
        Indicator.__init__(self, chart)

        self._ema = self.chart.indicator(indicators.EMA, {'period':self.period})

        self.chart.on("Candle-Close", target=self.calc_ema_grad)

    def calc_ema_grad(self, candle ):
        print('x')
