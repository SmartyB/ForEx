SELECT `strategy`, `hour`, COUNT(`profitTotal`) as NumTrades, SUM(`profitTotal`) AS Profit
FROM `trades`
GROUP BY `strategy` , `hour`
Order By `Strategy`, `hour` ASC