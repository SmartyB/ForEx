import strategies

plan = [
        {
            'pair'        : "EUR_USD",
            'strategy'    : [
                {
                    'name'              : strategies.SmartyStrat,
                    'thread'            : 't1',
                    'store'             : True,
                    'risk'              : 1,
                    'chart'             : 'M5',
                    'ema_period'        : 8,
                    '_schedule'      : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop': True,
                    'newsBlock'     :[
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose':[
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },
            ],
        },
    ]
