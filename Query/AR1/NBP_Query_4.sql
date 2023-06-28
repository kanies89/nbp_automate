declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1, '19000101');
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-0 , '19000101');
select @dtb,@dte

---split---

declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1, '19000101');
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-0 , '19000101');

--Dane z zakładek:
--MC  
--b)	DATA z AdjCom – daty należące do wybranego kwartału 
--c)	ARB CHB – wartości różne od ARB CHB i Tak ( filtr na nie i puste)
--d)	KRAJ - Zliczyć ilość i wartość transakcji po ustawieniu filtru kraj na POL a   następnie zliczyć dla wszystkich poza POL.
--Visa
--b)	Data CHB – daty należące do wybranego kwartału
--c)	ARB CHB -  wartości różne od ARB CHB i Tak ( filtr na nie i puste)
--d)	KRAJ - Zliczyć ilość i wartość transakcji po ustawieniu filtru kraj na PL a następnie zliczyć dla wszystkich poza PL.

SELECT
		IIF(country in ('POL','PL'), 'PL', 'other') as kraj
		,COUNT(id_c) as ilosc
		,ABS(SUM(tran_amount)) as kwota
  FROM [paytel_olap].[dbo].[v_rs_chargeback]
  where date_CHB between @dtb and @dte and arbitraz is null
group by IIF(country in ('POL','PL'), 'PL', 'other') 


---split---

--Policzyć wartość transakcji na zakładkach Visa i MC ustawiając filtry 
--ARB CHB -  wartości różne od ARB CHB i Tak ( filtr na nie i puste)
--Data CHB (Visa) / DATA z AdjCom (MC)– daty należące do wybranego kwartału 
--Obciążenia Merchanta (Visa) / obciążenie (MC) – wszystkie wartości które zaczynają się od „obciążenie” ( wykluczyć puste, niezrzeszeni, pre-abb itp.) 

declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1, '19000101');
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-0 , '19000101');

SELECT
		COUNT(id_c) as ilosc
		,ABS(SUM(tran_amount)) as kwota
  FROM [paytel_olap].[dbo].[v_rs_chargeback]
  where date_CHB between @dtb and @dte and arbitraz is null and charge_merchant_date is not null

