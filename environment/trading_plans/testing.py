import strategies

plan = [
        {
            'pair'        : "EUR_USD",
            'strategy'    : [
                {
                    'name'                  : strategies.SmartyStrat,
                    'thread'                : 't1',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period'            : 8,
                    'set_direction_limit'   : 4,
                    'remove_direction_limit': 2,
                    'entry_distance'        : 1,
                    'tp_pips'               : 20,
                    'sl_pips'               : 30,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },
                {
                    'name'                  : strategies.SmartyStratRR,
                    'thread'                : 't2',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period'            : 8,
                    'set_direction_limit'   : 4,
                    'remove_direction_limit': 2,
                    'entry_distance'        : 1,
                    'tp_pips'               : 30,
                    'sl_pips'               : 20,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },

            ],
        },
        {
            'pair'        : "GBP_USD",
            'strategy'    : [
                {
                    'name'                  : strategies.SmartyStrat,
                    'thread'                : 't1',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period'            : 8,
                    'set_direction_limit'   : 4,
                    'remove_direction_limit': 2,
                    'entry_distance'        : 1,
                    'tp_pips'               : 20,
                    'sl_pips'               : 30,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },
                {
                    'name'                  : strategies.SmartyStratRR,
                    'thread'                : 't2',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period'            : 8,
                    'set_direction_limit'   : 4,
                    'remove_direction_limit': 2,
                    'entry_distance'        : 1,
                    'tp_pips'               : 20,
                    'sl_pips'               : 30,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },

            ],
        },
        {
            'pair'        : "USD_CHF",
            'strategy'    : [
                {
                    'name'                  : strategies.SmartyStrat,
                    'thread'                : 't1',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period'            : 8,
                    'set_direction_limit'   : 4,
                    'remove_direction_limit': 2,
                    'entry_distance'        : 1,
                    'tp_pips'               : 20,
                    'sl_pips'               : 30,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },
                {
                    'name'                  : strategies.SmartyStratRR,
                    'thread'                : 't2',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period'            : 8,
                    'set_direction_limit'   : 4,
                    'remove_direction_limit': 2,
                    'entry_distance'        : 1,
                    'tp_pips'               : 20,
                    'sl_pips'               : 30,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },

            ],
        },
        {
            'pair'        : "USD_CAD",
            'strategy'    : [
                {
                    'name'                  : strategies.SmartyStrat,
                    'thread'                : 't1',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period'            : 8,
                    'set_direction_limit'   : 4,
                    'remove_direction_limit': 2,
                    'entry_distance'        : 1,
                    'tp_pips'               : 20,
                    'sl_pips'               : 30,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },
                {
                    'name'                  : strategies.SmartyStratRR,
                    'thread'                : 't2',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period'            : 8,
                    'set_direction_limit'   : 4,
                    'remove_direction_limit': 2,
                    'entry_distance'        : 1,
                    'tp_pips'               : 20,
                    'sl_pips'               : 30,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },

            ],
        },
        {
            'pair'        : "AUD_USD",
            'strategy'    : [
                {
                    'name'                  : strategies.SmartyStrat,
                    'thread'                : 't1',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period'            : 8,
                    'set_direction_limit'   : 4,
                    'remove_direction_limit': 2,
                    'entry_distance'        : 1,
                    'tp_pips'               : 20,
                    'sl_pips'               : 30,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },
                {
                    'name'                  : strategies.SmartyStratRR,
                    'thread'                : 't2',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period'            : 8,
                    'set_direction_limit'   : 4,
                    'remove_direction_limit': 2,
                    'entry_distance'        : 1,
                    'tp_pips'               : 20,
                    'sl_pips'               : 30,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },

            ],
        },
        {
            'pair'        : "EUR_CHF",
            'strategy'    : [
                {
                    'name'                  : strategies.SmartyStrat,
                    'thread'                : 't1',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period'            : 8,
                    'set_direction_limit'   : 4,
                    'remove_direction_limit': 2,
                    'entry_distance'        : 1,
                    'tp_pips'               : 20,
                    'sl_pips'               : 30,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },
                {
                    'name'                  : strategies.SmartyStratRR,
                    'thread'                : 't2',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period'            : 8,
                    'set_direction_limit'   : 4,
                    'remove_direction_limit': 2,
                    'entry_distance'        : 1,
                    'tp_pips'               : 20,
                    'sl_pips'               : 30,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },

            ],
        },
        {
            'pair'        : "EUR_GBP",
            'strategy'    : [
                {
                    'name'                  : strategies.SmartyStrat,
                    'thread'                : 't1',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period'            : 8,
                    'set_direction_limit'   : 4,
                    'remove_direction_limit': 2,
                    'entry_distance'        : 1,
                    'tp_pips'               : 20,
                    'sl_pips'               : 30,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },
                {
                    'name'                  : strategies.SmartyStratRR,
                    'thread'                : 't2',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period'            : 8,
                    'set_direction_limit'   : 4,
                    'remove_direction_limit': 2,
                    'entry_distance'        : 1,
                    'tp_pips'               : 20,
                    'sl_pips'               : 30,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },

            ],
        },
        {
            'pair'        : "AUD_CAD",
            'strategy'    : [
                {
                    'name'                  : strategies.SmartyStrat,
                    'thread'                : 't1',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period'            : 8,
                    'set_direction_limit'   : 4,
                    'remove_direction_limit': 2,
                    'entry_distance'        : 1,
                    'tp_pips'               : 20,
                    'sl_pips'               : 30,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },
                {
                    'name'                  : strategies.SmartyStratRR,
                    'thread'                : 't2',
                    'store'                 : True,
                    'risk'                  : 1,
                    'chart'                 : 'M30',
                    'ema_period'            : 8,
                    'set_direction_limit'   : 4,
                    'remove_direction_limit': 2,
                    'entry_distance'        : 1,
                    'tp_pips'               : 20,
                    'sl_pips'               : 30,
                    '_schedule'             : [
                        {'start':'Mon 01:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop' : True,
                    'newsBlock'         : [
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose' : [
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },

            ],
        },
    ]
