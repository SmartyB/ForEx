SELECT `strategy`, `instrument`, COUNT(`profitTotal`) as NumTrades, SUM(`profitTotal`) AS Profit
FROM `trades`
GROUP BY `strategy` , `instrument`
Order By  `strategy` ASC