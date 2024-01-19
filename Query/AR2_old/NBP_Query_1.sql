--Transakcje płatnicze realizowane w oparciu o kartę [otrzymane]
SELECT num, name
	, SUM(ilosc) as ilosc, SUM(wartosc_transakcji) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name
GROUP BY num,name
ORDER BY num

---split---

--Inicjowane w formie innej niż elektroniczna (imprinter, zlecenie pocztowe i MOTO)
SELECT num, name
,ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto = 'MOTO'
GROUP BY num,name
ORDER BY num

---split---

--Niezdalne
--0
--Zdalne        (moto to zdalne - odpowiedz nbp transakcja typu CNP)
SELECT num, name
, ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto = 'MOTO'
GROUP BY num,name
ORDER BY num

---split---

--Inicjowane w formie elektronicznej
SELECT num, name
, ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO'
GROUP BY num,name
ORDER BY num

---split---

--Niezdalne   (jak wyżej)
SELECT num, name
, ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO'
GROUP BY num,name
ORDER BY num

---split---

--w tym w podziale na rodzaj płatności:
--Inicjowane w urządzeniach akceptujących karty płatnicze   (jak wyżej)
SELECT num, name
, ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO'
GROUP BY num,name
ORDER BY num

---split---

--w tym w podziale na schematy:
--VISA
SELECT num, name
, ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO' and karta = 'VISA'
GROUP BY num,name
ORDER BY num

---split---

--karty debetowe
SELECT num, name
, ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO' and karta = 'VISA' and Typ_karty = 'debit'
GROUP BY num,name
ORDER BY num

---split---

--karty obciążeniowe
SELECT num, name
, ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO' and karta = 'VISA' and (Typ_karty not in ( 'debit', 'credit') or Typ_karty is null)
GROUP BY num,name
ORDER BY num

---split---

--karty kredytowe
SELECT num, name
, ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO' and karta = 'VISA' and Typ_karty = 'credit'
GROUP BY num,name
ORDER BY num

---split---

--SCA
SELECT num, name
, ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO' and karta = 'VISA' and czy_SCA = 1
GROUP BY num,name
ORDER BY num

---split---

--non-SCA
SELECT num, name
, ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO' and karta = 'VISA' and czy_SCA = 0
GROUP BY num,name
ORDER BY num

---split---

--MASTERCARD
SELECT num, name
, ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO' and karta = 'MC'
GROUP BY num,name
ORDER BY num

---split---

--karty debetowe
SELECT num, name
, ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO' and karta = 'MC' and Typ_karty = 'debit'
GROUP BY num,name
ORDER BY num

---split---

--karty obciążeniowe
SELECT num, name
, ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO' and karta = 'MC' and (Typ_karty not in ( 'debit', 'credit') or Typ_karty is null)
GROUP BY num,name
ORDER BY num

---split---

--karty kredytowe
SELECT num, name
, ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO' and karta = 'MC' and Typ_karty = 'credit'
GROUP BY num,name
ORDER BY num

---split---

--SCA
SELECT num, name
, ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO' and karta = 'MC' and czy_SCA = 1
GROUP BY num,name
ORDER BY num

---split---

--non-SCA
SELECT num, name
, ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO' and karta = 'MC' and czy_SCA = 0
GROUP BY num,name
ORDER BY num

---split---

--w tym Przyczyny braku silnego uwierzytelnienia klienta:
--Transakcja cykliczna

--Niskokwotowa płatność zbliżeniowa
SELECT num, name
,ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO' and czy_SCA = 0 and czy_niskokwotowa_zblizeniowa = 1
GROUP BY num,name
ORDER BY num

---split---

--Terminale samoobsługowe służące do uiszczania opłat za przejazd i opłat za postój

--Inne
SELECT num, name
,ISNULL(SUM(ilosc), 0) as ilosc, ISNULL(SUM(wartosc_transakcji), 0) as wartosc
FROM #geo3 
LEFT JOIN #dane on podzial_NBP = name and czy_moto <> 'MOTO' and czy_SCA = 0 and czy_niskokwotowa_zblizeniowa = 0
GROUP BY num,name
ORDER BY num

---split---

-- formularz 6.ab.LiW ---- ilość oraz wartość transakcji w podziale na karty polskie vs pozostałe

--LICZBA TRANSAKCJI
--WARTOŚĆ TRANSAKCJI
--a) Transakcje w terminalach rezydentów z użyciem kart wydanych przez krajowych dostawców usług płatniczych                     <------- TYLKO PL
--Transakcje w urządzeniach akceptujących karty płatnicze (POS)

SELECT SUM(ilosc) as ilosc, SUM(wartosc_transakcji) as wartosc
FROM #dane
WHERE podzial_NBP = 'KRAJOWE'	
ORDER BY 1

---split---

--LICZBA TRANSAKCJI
--WARTOŚĆ TRANSAKCJI
--b)Transakcje w terminalach rezydentów z użyciem kart wydanych przez zagranicznych dostawców usług płatniczych					<------- WSZYSTKO POZA PL
--Transakcje w urządzeniach akceptujących karty płatnicze (POS)


SELECT SUM(ilosc) as ilosc, SUM(wartosc_transakcji) as wartosc
FROM #dane
WHERE podzial_NBP <> 'KRAJOWE'
ORDER BY 1






