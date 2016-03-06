import strategies

plan = [
        {
            'pair'        : "EUR_USD",
            'strategy'    : [
                {
                    'name'                  : strategies.SmartyStratV3,
                    'thread'                : 't1',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period':           8,
                    'set_direction_limit': 4,
                    'remove_direction_limit': 2,
                    'tp_pips': 20,
                    'sl_pips': 20,
                    'entry_distance': 2,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [],
                },


            ],
        },

    ]
