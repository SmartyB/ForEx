from lib.event import Event

class Indicator(Event):
    def __init__(self, chart):
        self.chart = chart
        self.instrument = self.chart.instrument

        self.displayName    = self.parseDisplayName(self.__class__, self.__dict__)

    @staticmethod
    def parseDisplayName(indicator, params):
        required = {
            'Fractals'      : ['range'],
            'PriceRange'    : [],
            'Activity'      : ['range'],
            'EMA'           : ['period'],
            'Pivots'        : [],
            'EmaGradient'       : ['period'],
        }
        optional = {
            'Fractals'      : [],
            'PriceRange'    : [],
            'Activity'      : [],
            'EMA'           : [],
            'Pivots'        : [],
            'EmaGradient'       : [],

        }

        dispName = indicator.__name__
        required = required[dispName]
        optional = optional[dispName]

        for req in required:
            dispName += "-" + str(params[req])
        for opt in optional:
            if opt in params:
                dispName += "-" + str(params[opt])
        return dispName
