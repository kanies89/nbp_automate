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

--Dane z zak³adek:
--MC  
--b)	DATA z AdjCom – daty nale¿¹ce do wybranego kwarta³u 
--c)	ARB CHB – wartoœci ró¿ne od ARB CHB i Tak ( filtr na nie i puste)
--d)	KRAJ - Zliczyæ iloœæ i wartoœæ transakcji po ustawieniu filtru kraj na POL a   nastêpnie zliczyæ dla wszystkich poza POL.
--Visa
--b)	Data CHB – daty nale¿¹ce do wybranego kwarta³u
--c)	ARB CHB -  wartoœci ró¿ne od ARB CHB i Tak ( filtr na nie i puste)
--d)	KRAJ - Zliczyæ iloœæ i wartoœæ transakcji po ustawieniu filtru kraj na PL a nastêpnie zliczyæ dla wszystkich poza PL.

SELECT
		IIF(country in ('POL','PL'), 'PL', 'other') as kraj
		,COUNT(id_c) as ilosc
		,ABS(SUM(tran_amount)) as kwota
  FROM [paytel_olap].[dbo].[v_rs_chargeback]
  where date_CHB between @dtb and @dte and arbitraz is null
group by IIF(country in ('POL','PL'), 'PL', 'other')

---split---

declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1, '19000101');
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-0 , '19000101');

--Policzyæ wartoœæ transakcji na zak³adkach Visa i MC ustawiaj¹c filtry 
--ARB CHB -  wartoœci ró¿ne od ARB CHB i Tak ( filtr na nie i puste)
--Data CHB (Visa) / DATA z AdjCom (MC)– daty nale¿¹ce do wybranego kwarta³u 
--Obci¹¿enia Merchanta (Visa) / obci¹¿enie (MC) – wszystkie wartoœci które zaczynaj¹ siê od „obci¹¿enie” ( wykluczyæ puste, niezrzeszeni, pre-abb itp.) 

SELECT
		COUNT(id_c) as ilosc
		,ABS(SUM(tran_amount)) as kwota
  FROM [paytel_olap].[dbo].[v_rs_chargeback]
  where date_CHB between @dtb and @dte and arbitraz is null and charge_merchant_date is not null

