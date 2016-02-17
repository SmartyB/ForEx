import strategies

lStrategy = [
        {
            'pair'        : "EUR_USD",
            'strategy'    : [
                {
                    'name'              : strategies.Tradimo,
                    'thread'            : 't1',
                    'store'             : True,
                    'risk'              : 1,
                    'dirchart'          : 'M30',
                    'tradechart'        : 'M5',
                    '_schedule'      : [
                        {'start':'Mon 04:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop': True,
                    'newsBlock'     :[
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose':[
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },
                {
                    'name'              : strategies.TradimoRR,
                    'thread'            : 't2',
                    'store'             : True,
                    'risk'              : 1,
                    'dirchart'          : 'M30',
                    'tradechart'        : 'M5',
                    '_schedule'      : [
                        {'start':'Mon 04:00:00', 'end':'Fri 16:00:00'},
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
        {
            'pair'        : "GBP_USD",
            'strategy'    : [
                {
                    'name'              : strategies.Tradimo,
                    'thread'            : 't1',
                    'store'             : True,
                    'risk'              : 1,
                    'dirchart'          : 'M30',
                    'tradechart'        : 'M5',
                    '_schedule'      : [
                        {'start':'Mon 04:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop': True,
                    'newsBlock'     :[
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose':[
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },
                {
                    'name'              : strategies.TradimoRR,
                    'thread'            : 't2',
                    'store'             : True,
                    'risk'              : 1,
                    'dirchart'          : 'M30',
                    'tradechart'        : 'M5',
                    '_schedule'      : [
                        {'start':'Mon 04:00:00', 'end':'Fri 16:00:00'},
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
        {
            'pair'        : "USD_CHF",
            'strategy'    : [
                    {
                        'name'              : strategies.Tradimo,
                        'thread'            : 't1',
                        'store'             : True,
                        'risk'              : 1,
                        'dirchart'          : 'M30',
                        'tradechart'        : 'M5',
                        '_schedule'      : [
                            {'start':'Mon 04:00:00', 'end':'Fri 16:00:00'},
                        ],
                        'closeTradesOnStop': True,
                        'newsBlock'     :[
                            {'type':'before', 'time':400, 'minImportance':1}
                        ],
                        'newsClose':[
                            {'type':'before', 'time':300, 'minImportance':1}
                        ],
                    },
                    {
                        'name'              : strategies.TradimoRR,
                        'thread'            : 't2',
                        'store'             : True,
                        'risk'              : 1,
                        'dirchart'          : 'M30',
                        'tradechart'        : 'M5',
                        '_schedule'      : [
                            {'start':'Mon 04:00:00', 'end':'Fri 16:00:00'},
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
        {
            'pair'        : "USD_CAD",
            'strategy'    : [
                {
                    'name'              : strategies.Tradimo,
                    'thread'            : 't1',
                    'store'             : True,
                    'risk'              : 1,
                    'dirchart'          : 'M30',
                    'tradechart'        : 'M5',
                    '_schedule'      : [
                        {'start':'Mon 04:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop': True,
                    'newsBlock'     :[
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose':[
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },
                {
                    'name'              : strategies.TradimoRR,
                    'thread'            : 't2',
                    'store'             : True,
                    'risk'              : 1,
                    'dirchart'          : 'M30',
                    'tradechart'        : 'M5',
                    '_schedule'      : [
                        {'start':'Mon 04:00:00', 'end':'Fri 16:00:00'},
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
        {
            'pair'        : "AUD_USD",
            'strategy'    : [
                {
                    'name'              : strategies.Tradimo,
                    'thread'            : 't1',
                    'store'             : True,
                    'risk'              : 1,
                    'dirchart'          : 'M30',
                    'tradechart'        : 'M5',
                    '_schedule'      : [
                        {'start':'Mon 04:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop': True,
                    'newsBlock'     :[
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose':[
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },
                {
                    'name'              : strategies.TradimoRR,
                    'thread'            : 't2',
                    'store'             : True,
                    'risk'              : 1,
                    'dirchart'          : 'M30',
                    'tradechart'        : 'M5',
                    '_schedule'      : [
                        {'start':'Mon 04:00:00', 'end':'Fri 16:00:00'},
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
        {
            'pair'        : "EUR_CHF",
            'strategy'    : [

                {
                    'name'              : strategies.Tradimo,
                    'thread'            : 't1',
                    'store'             : True,
                    'risk'              : 1,
                    'dirchart'          : 'M30',
                    'tradechart'        : 'M5',
                    '_schedule'      : [
                        {'start':'Mon 04:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop': True,
                    'newsBlock'     :[
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose':[
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },
                {
                    'name'              : strategies.TradimoRR,
                    'thread'            : 't2',
                    'store'             : True,
                    'risk'              : 1,
                    'dirchart'          : 'M30',
                    'tradechart'        : 'M5',
                    '_schedule'      : [
                        {'start':'Mon 04:00:00', 'end':'Fri 16:00:00'},
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
        {
            'pair'        : "EUR_GBP",
            'strategy'    : [
                {
                    'name'              : strategies.Tradimo,
                    'thread'            : 't1',
                    'store'             : True,
                    'risk'              : 1,
                    'dirchart'          : 'M30',
                    'tradechart'        : 'M5',
                    '_schedule'      : [
                        {'start':'Mon 04:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop': True,
                    'newsBlock'     :[
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose':[
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },
                {
                    'name'              : strategies.TradimoRR,
                    'thread'            : 't2',
                    'store'             : True,
                    'risk'              : 1,
                    'dirchart'          : 'M30',
                    'tradechart'        : 'M5',
                    '_schedule'      : [
                        {'start':'Mon 04:00:00', 'end':'Fri 16:00:00'},
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
        {
            'pair'        : "AUD_CAD",
            'strategy'    : [
                {
                    'name'              : strategies.Tradimo,
                    'thread'            : 't1',
                    'store'             : True,
                    'risk'              : 1,
                    'dirchart'          : 'M30',
                    'tradechart'        : 'M5',
                    '_schedule'      : [
                        {'start':'Mon 04:00:00', 'end':'Fri 16:00:00'},
                    ],
                    'closeTradesOnStop': True,
                    'newsBlock'     :[
                        {'type':'before', 'time':400, 'minImportance':1}
                    ],
                    'newsClose':[
                        {'type':'before', 'time':300, 'minImportance':1}
                    ],
                },
                {
                    'name'              : strategies.TradimoRR,
                    'thread'            : 't2',
                    'store'             : True,
                    'risk'              : 1,
                    'dirchart'          : 'M30',
                    'tradechart'        : 'M5',
                    '_schedule'      : [
                        {'start':'Mon 04:00:00', 'end':'Fri 16:00:00'},
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
