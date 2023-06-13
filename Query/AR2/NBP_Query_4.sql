use paytel_olap

set transaction isolation level read uncommitted

declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1, '19000101');
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-0 , '19000101');
select @dtb,@dte
---- DO WKLEJANIA:

---split---

--Transakcje płatnicze realizowane w oparciu o kartę [otrzymane]
	SELECT code, name, isnull(SUM(ilosc), 0) as ilosc, isnull(SUM(wartosc_transakcji), 0) wartosc_transakcji
	FROM #start s
	LEFT JOIN #dane_2 d on s.mcc = d.merchant_category_code and s.code = d.country_code_NBP
	group by code, name
	order by 1

---split---

--Inicjowane w formie elektronicznej
	SELECT code, name, isnull(SUM(ilosc), 0) as ilosc, isnull(SUM(wartosc_transakcji), 0) wartosc_transakcji
	FROM #start s
	LEFT JOIN #dane_2 d on s.mcc = d.merchant_category_code and s.code = d.country_code_NBP and czy_moto = 'inne'
	group by code, name
	order by 1

---split---

--Niezdalne
	SELECT code, name, isnull(SUM(ilosc), 0) as ilosc, isnull(SUM(wartosc_transakcji), 0) wartosc_transakcji
	FROM #start s
	LEFT JOIN #dane_2 d on s.mcc = d.merchant_category_code and s.code = d.country_code_NBP and czy_moto = 'inne'
	group by code, name
	order by 1

---split---

--w tym w podziale na kody MCC:

SELECT code, name, mcc, opis, isnull(ilosc, 0) as ilosc, isnull(wartosc_transakcji, 0) wartosc_transakcji
FROM #start s
LEFT JOIN #dane_2 d on s.mcc = d.merchant_category_code and s.code = d.country_code_NBP and czy_moto = 'inne'
ORDER BY 1,3








