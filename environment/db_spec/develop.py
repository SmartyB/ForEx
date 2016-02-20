db_path = '../database/develop.db'
spec = {
  'Order':{
    'table'         : 'orders',
    'primary_key'   : 'id',
    'fields'        : ['id', 'year', 'month', 'day', 'weekday', 'hour', 'minute',
                        'second', 'pair', 'strategy_name', 'trade_id',
                        'risk_remove_pips']
  },
  'Trade':{
    'table'         : 'trades',
    'primary_key'   : 'id',
    'fields'        : ['id', 'year', 'entry_time', 'exit_time', 'month', 'day',
                        'weekday', 'hour', 'minute', 'second', 'pair',
                        'strategy_name', 'side', 'units', 'entry_price', 'exit_price',
                        'profit_pips', 'profit_total', 'max_profit_pips',
                        'min_profit_pips', 'time_since_order', 'risk_remove_pips']
  }
}
