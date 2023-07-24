declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1, '19000101');
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-0 , '19000101');
select @dtb,@dte

---split---

SELECT t.CountryCode, g.name_PL, g.name
	,[podział NBP] as podzial_NBP
	,SUM(ilosc) as ilosc_transakcji
	,SUM(ilosc_internet) as ilosc_internet
	,SUM([ilość transakcji CashBack]) as ilosc_transakcji_CashBack
	,SUM([wartość transakcji]) as wartosc_transakcji
	,SUM(wartosc_internet) as wartosc_internet
	,SUM([Wartość wypłat CashBack]) as wartosc_wyplat_CashBack
FROM #transakcje t
LEFT JOIN #geo6 g on g.code = t.CountryCode 
GROUP BY t.CountryCode, g.name_PL, g.name, [podział NBP]
ORDER BY [podział NBP] desc, g.name

