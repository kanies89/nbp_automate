SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED
USE paytel_olap

declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1, '19000101');
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-0 , '19000101');
select @dtb,@dte
-- STATUSY na [paytel_olap].[dbo].[v_rs_chargeback]
-- zamkni�ta - przegrana ---> strata merchanta/sklepu
-- strata operacyjna Paytel ----> strata agenta rozliczeniowego (czyli Paytel)
-- zamkni�ta - wygrana -------> strata posiadacza karty


--Dane z zak�adek:
--MC  
--b)	DATA z AdjCom � daty nale��ce do wybranego kwarta�u 
--c)	ARB CHB � warto�ci r�ne od ARB CHB i Tak ( filtr na nie i puste)
--d)	KRAJ - Zliczy� ilo�� i warto�� transakcji po ustawieniu filtru kraj na POL a   nast�pnie zliczy� dla wszystkich poza POL.
--Visa
--b)	Data CHB � daty nale��ce do wybranego kwarta�u
--c)	ARB CHB -  warto�ci r�ne od ARB CHB i Tak ( filtr na nie i puste)
--d)	KRAJ - Zliczy� ilo�� i warto�� transakcji po ustawieniu filtru kraj na PL a nast�pnie zliczy� dla wszystkich poza PL.

SELECT
	IIF(country in ('POL','PL'), 'PL', 'other') as kraj
	,COUNT(id_c) as ilosc
	,ABS(SUM(tran_amount)) as kwota
FROM [paytel_olap].[dbo].[v_rs_chargeback]
where date_CHB between @dtb and @dte and arbitraz is null
group by IIF(country in ('POL','PL'), 'PL', 'other') 


--Policzy� warto�� transakcji na zak�adkach Visa i MC ustawiaj�c filtry 
--ARB CHB -  warto�ci r�ne od ARB CHB i Tak ( filtr na nie i puste)
--Data CHB (Visa) / DATA z AdjCom (MC)� daty nale��ce do wybranego kwarta�u 
--Obci��enia Merchanta (Visa) / obci��enie (MC) � wszystkie warto�ci kt�re zaczynaj� si� od �obci��enie� ( wykluczy� puste, niezrzeszeni, pre-abb itp.) 

SELECT
	COUNT(id_c) as ilosc,
	ABS(SUM(tran_amount)) as kwota
FROM [paytel_olap].[dbo].[v_rs_chargeback]
where date_CHB between @dtb and @dte and arbitraz is null and status = 'zamkni�ta- przegrana'--charge_merchant_date is not null
  
SELECT 
	COUNT(id_c) as ilosc,
	ABS(SUM(tran_amount)) as kwota
FROM [paytel_olap].[dbo].[v_rs_chargeback]
WHERE [status] LIKE '%strata%'
AND date_CHB  between @dtb and @dte

