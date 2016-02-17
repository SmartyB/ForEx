SELECT `strategy_name`, COUNT(`profit_total`) as NumTrades, SUM(`profit_pips`) AS Profit
FROM `trades`
GROUP BY `strategy_name`
Order By  `strategy_name` ASC