--select * from #geo3
--SELECt * from #dane

-- Transakcje płatnicze realizowane w oparciu o kartę [otrzymane]
select 
g.code
,num
,COUNT(ARN) as ilosc
,isnull(SUM(tr_amout), 0) as wartosc
FROM #dane d
right join #geo3 g on d.code = g.code
group by g.code, num
order by num

---split---

-- Inicjowane w formie innej niż elektroniczna (imprinter, zlecenie pocztowe i MOTO)
select
g.code
,num
,COUNT(ARN) as ilosc
,isnull(SUM(tr_amout), 0) as wartosc
FROM #dane d
right join #geo3 g on d.code = g.code and czy_moto = 'MOTO'
group by g.code, num
order by num

---split---

--  Niezdalne
-- 0

--  Zdalne
select
g.code
,num
,COUNT(ARN) as ilosc
,isnull(SUM(tr_amout), 0) as wartosc
FROM #dane d
right join #geo3 g on d.code = g.code and czy_moto = 'MOTO'
group by g.code, num
order by num

---split---

-- Inicjowane w formie elektronicznej
select
g.code
,num
,COUNT(ARN) as ilosc
,isnull(SUM(tr_amout), 0) as wartosc
FROM #dane d
right join #geo3 g on d.code = g.code and czy_moto <> 'MOTO'
group by g.code, num
order by num

---split---

-- Niezdalne
select
g.code
,num
,COUNT(ARN) as ilosc
,isnull(SUM(tr_amout), 0) as wartosc
FROM #dane d
right join #geo3 g on d.code = g.code and czy_moto <> 'MOTO'
group by g.code, num
order by num

---split---

-- w tym w podziale na rodzaj płatności:
-- Inicjowane w urządzeniach akceptujących karty płatnicze 
select
g.code
,num
,COUNT(ARN) as ilosc
,isnull(SUM(tr_amout), 0) as wartosc
FROM #dane d
right join #geo3 g on d.code = g.code and czy_moto <> 'MOTO'
group by g.code, num
order by num

-- Inicjowane w bankomacie
-- 0

-- Pozostałe kanały inicjacji 
-- 0

---split---

-- w tym w podziale na schematy:
-- VISA
select
g.code
,num
,COUNT(ARN) as ilosc
,isnull(SUM(tr_amout), 0) as wartosc
FROM #dane d
right join #geo3 g on d.code = g.code and czy_moto <> 'MOTO' and tr_sink_node = 'SN-Visa'
group by g.code, num
order by num

---split---

-- w tym w podziale na rodzaj karty:
	-- karty debetowe
	select
		g.code
		,num
		,COUNT(ARN) as ilosc
		,isnull(SUM(tr_amout), 0) as wartosc
	FROM #dane d
	right join #geo3 g on d.code = g.code and czy_moto <> 'MOTO' and tr_sink_node = 'SN-Visa' and Typ_karty = 'Debit'
	group by g.code, num
	order by num

---split---

	-- karty obciążeniowe
	select
		g.code
		,num
		,COUNT(ARN) as ilosc
		,isnull(SUM(tr_amout), 0) as wartosc
	FROM #dane d
	right join #geo3 g on d.code = g.code and czy_moto <> 'MOTO' and tr_sink_node = 'SN-Visa' and (Typ_karty not in ('Credit', 'Debit') or Typ_karty is null)
	group by g.code, num
	order by num

---split---

	-- karty kredytowe
	select
		g.code
		,num
		,COUNT(ARN) as ilosc
		,isnull(SUM(tr_amout), 0) as wartosc
	FROM #dane d
	right join #geo3 g on d.code = g.code and czy_moto <> 'MOTO' and tr_sink_node = 'SN-Visa' and Typ_karty = 'Credit'
	group by g.code, num
	order by num

-- w tym w podziale na rodzaj uwierzytelnienia:

	-- SCA
		--
		--
		--
		--
		--
		--


	-- non-SCA
		--
		--
		--
		--
		--
		--

---split---

-- MC
select
g.code
,num
,COUNT(ARN) as ilosc
,isnull(SUM(tr_amout), 0) as wartosc
FROM #dane d
right join #geo3 g on d.code = g.code and czy_moto <> 'MOTO' and tr_sink_node = 'SN-MasterC'
group by g.code, num
order by num

---split---

-- w tym w podziale na rodzaj karty:
	-- karty debetowe
	select
		g.code
		,num
		,COUNT(ARN) as ilosc
		,isnull(SUM(tr_amout), 0) as wartosc
	FROM #dane d
	right join #geo3 g on d.code = g.code and czy_moto <> 'MOTO' and tr_sink_node = 'SN-MasterC' and Typ_karty = 'Debit'
	group by g.code, num
	order by num

---split---

	-- karty obciążeniowe
	select
		g.code
		,num
		,COUNT(ARN) as ilosc
		,isnull(SUM(tr_amout), 0) as wartosc
	FROM #dane d
	right join #geo3 g on d.code = g.code and czy_moto <> 'MOTO' and tr_sink_node = 'SN-MasterC' and (Typ_karty not in ('Credit', 'Debit') or Typ_karty is null)
	group by g.code, num
	order by num

---split---

	-- karty kredytowe
	select
		g.code
		,num
		,COUNT(ARN) as ilosc
		,isnull(SUM(tr_amout), 0) as wartosc
	FROM #dane d
	right join #geo3 g on d.code = g.code and czy_moto <> 'MOTO' and tr_sink_node = 'SN-MasterC' and Typ_karty = 'Credit'
	group by g.code, num
	order by num

---split---

-- w tym w podziale na rodzaj uwierzytelnienia:
	-- SCA
	select
		g.code
		,num
		,COUNT(ARN) as ilosc
		,isnull(SUM(tr_amout), 0) as wartosc
	FROM #dane d
	right join #geo3 g on d.code = g.code and czy_moto <> 'MOTO' and tr_sink_node = 'SN-MasterC' and czy_SCA = 'SC1'
	group by g.code, num
	order by num

	  -- w tym nieuczciwe płatności kartami w podziale na źródło nadużycia: 
		  -- Wystawienie zlecenia płatniczego przez oszusta
		  -- Zgubienie lub kradzież karty
		  -- Nieodebrana karta 
		  -- Karta sfałszowana 
		  -- Pozostałe
		  -- Modyfikacja zlecenia płatniczego przez oszusta
		  -- Nakłonienie płatnika do dokonania płatności kartą

---split---

	-- non-SCA
	select
		g.code
		,num
		,COUNT(ARN) as ilosc
		,isnull(SUM(tr_amout), 0) as wartosc
	FROM #dane d
	right join #geo3 g on d.code = g.code and czy_moto <> 'MOTO' and tr_sink_node = 'SN-MasterC' and czy_SCA = 'SC0'
	group by g.code, num
	order by num

	  -- w tym nieuczciwe płatności kartami w podziale na źródło nadużycia: 
		  -- Wystawienie zlecenia płatniczego przez oszusta
		  -- Zgubienie lub kradzież karty
		  -- Nieodebrana karta 
		  -- Karta sfałszowana 
		  -- Pozostałe
		  -- Modyfikacja zlecenia płatniczego przez oszusta
		  -- Nakłonienie płatnika do dokonania płatności kartą

---split---

-- w tym Przyczyny braku silnego uwierzytelnienia klienta:
-- Transakcja cykliczna	   		
-- 0

-- Niskokwotowa płatność zbliżeniowa
select
	g.code
	,num
	,COUNT(ARN) as ilosc
	,isnull(SUM(tr_amout), 0) as wartosc
FROM #dane d
right join #geo3 g on d.code = g.code and czy_moto <> 'MOTO' and czy_SCA = 'SC0' and czy_niskokwotowa_zblizeniowa = 1
group by g.code, num
order by num

-- Terminale samoobsługowe służące do uiszczania opłat za przejazd i opłat za postój
-- 0
---split---
-- Inne
select
	g.code
	,num
	,COUNT(ARN) as ilosc
	,isnull(SUM(tr_amout), 0) as wartosc
FROM #dane d
right join #geo3 g on d.code = g.code and czy_moto <> 'MOTO' and czy_SCA = 'SC0' and czy_niskokwotowa_zblizeniowa = 0
group by g.code, num
order by num