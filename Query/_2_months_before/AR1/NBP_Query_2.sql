declare @dtb as smalldatetime
declare @dte as smalldatetime
declare @te_tran_type as int

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-2, '19000101'); --changed from -1 to -2 due to checking 2 quaters in the past
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1 , '19000101'); --changed from 0 to -1 due to checking 2 quaters in the past
select @dtb,@dte

---split---

declare @dtb as smalldatetime
declare @dte as smalldatetime
declare @te_tran_type as int

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-2, '19000101'); --changed from -1 to -2 due to checking 2 quaters in the past
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1 , '19000101'); --changed from 0 to -1 due to checking 2 quaters in the past
set @te_tran_type = '09' --tylko CashBack
     /*
     '20 - Refund'
     '00 - Goods and services'
     '09 - Goods and services with cash back'
     '91 - General admin (see extended transaction type)'
     '93 - Dead-end general admin (see extended transaction type)'
     */

--transakcje VISA
SELECT
 'VISA' as 'karta',
  CASE 
  WHEN  VT.country = 'PL' THEN 'POLSKA'
  WHEN VT.country is null THEN 'NULL'
 ELSE 'INNE KRAJE' END as 'KRAJE',
 vp_bio as 'category',
 count(*) as 'Liczba transakcji CashBack',
 --sum(convert(money,abs((tr_amount/100)))) as 'Wartość transakcji typu CashBack',
 sum(convert(money,abs((tr_cash_req/100))))as 'Wartość wypłat Cash Back'

FROM 
 visa_transaction VT (nolock) 
 join if_transaction IT (nolock) on IT.postTranId = VT.postTranId 
 join v_trans (nolock) on tranNr = tr_tran_nr
 	 and tr_datetime_req between @dtb AND @dte 
	 and tr_reversed = 0
	 and tr_rsp_code = '00'   
	 and tr_message_type in (200,220)
 join v_trans_ext (nolock) on tr_tran_nr = te_tran_nr
   and [te_tran_type] = @te_tran_type
 join mcc_visa_group on mcc=merchant_category_code
 left join country_codes CS on VT.country=cc_A2
    left join visa_product_id on VT.productId=vp_product_id


GROUP BY 
  CASE 
  WHEN  VT.country = 'PL' THEN 'POLSKA'
  WHEN VT.country is null THEN 'NULL'
 ELSE 'INNE KRAJE' END,
 vp_bio
 
UNION ALL

--transakcje MC
SELECT 
 'MC' as 'karta',
 CASE
  WHEN MC.country ='POL' THEN 'POLSKA'
  
 ELSE 'INNE KRAJE' END AS 'KRAJE',

 CASE 
  WHEN ipc_category2 = 'B' THEN 'BUSINESS'
  WHEN ipc_category2 = 'C' THEN 'Individual'
  ELSE 'b.d.' END as 'category',
 count(*) as 'Liczba transakcji CashBack',
 --sum(convert(money,abs((tr_amount/100)))) as 'Wartość transakcji typu CashBack',
 sum(convert(money,abs((tr_cash_req/100))))as 'Wartość wypłat Cash Back'

FROM 
 mc_transaction MC (nolock)
 join if_transaction TR (nolock) on TR.postTranId = MC.postTranId
 join v_trans (nolock) on TR.tranNr = tr_tran_nr 
	 and tr_datetime_req between @dtb AND @dte 
	 and tr_reversed = 0
	 and tr_rsp_code = '00'   
	 and tr_message_type in (200,220)
 join v_trans_ext (nolock) on tr_tran_nr = te_tran_nr
  and [te_tran_type] = @te_tran_type
 
 --left Join mcipm_ip0072t1 on MC.memberId=mcipm_ip0072t1.member_id 
 --left join country_codes CS on mcipm_ip0072t1.country_code=cc_A3
 left join if_product_category (NOLOCK) ON gcmsProductId = ipc_product_id    



group by
 
 CASE
  WHEN MC.country ='POL' THEN 'POLSKA'
  
 ELSE 'INNE KRAJE' END,

 CASE 
  WHEN ipc_category2 = 'B' THEN 'BUSINESS'
  WHEN ipc_category2 = 'C' THEN 'Individual'
  ELSE 'b.d.' END

 ORDER BY 1, 2, 3 DESC
 
 
 ---split---
 
 /*
Wynikiem zapytania jest lista transakcji BLIK.
Dotyczy:		Raport kwartalny NBP. 
Autor:			Damian Witkowski
Odbiorca:		Zespół Przetwarzania
Serwer:			PRDBI
Baza danych:	paytel_olap
*/

declare @dtb as smalldatetime
declare @dte as smalldatetime
declare @te_tran_type as int

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-2, '19000101'); --changed from -1 to -2 due to checking 2 quaters in the past
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1 , '19000101'); --changed from 0 to -1 due to checking 2 quaters in the past
 
 SELECT
	count(*) AS 'Liczba transakcji BLIK',
	SUM(convert(money,ABS(tr_amount/100))) AS 'Kwota transakcji BLIK'
	
FROM
	v_trans WITH (NOLOCK)-- w przypadku starszych niż 90 dni v_trans

WHERE
	tr_reversed = 0
  	and tr_rsp_code = '00'
	AND tr_message_type IN (200, 220)
	and tr_app_id = '25'
	and tr_datetime_local between @dtb and @dte
	
 ---split---
 
 --NBP - ST.05 v_trans VISA i MC z podziałem na (business i Indyvidual)- .sql

/*
distinct z ostatniego kwartału:
0 - zbliżeniowo i moto
1 - PIN
5 - podpis
6 - inne


9 - Consumer device cardholder verification
B - Consumer device cardholder verification with code
D - Consumer device cardholder verification with biometric

Dodatkowo:
A - Unknown (ale raczej też elektronicznie)
C - Consumer device cardholder verification with pattern

*/

 select 
 KRAJE
 ,CASE
	WHEN category in ('b.d.', 'Other') THEN 'Individual' ELSE category END as 'category'
 ,SUM(ilosc) as ilosc
 ,SUM(wartosc) as wartosc

 from #dane
 group by
  KRAJE
 ,CASE
	WHEN category in ('b.d.', 'Other') THEN 'Individual' ELSE category END
order by 2

---split---

 select 
 KRAJE
 ,CASE
	WHEN category in ('b.d.', 'Other') THEN 'Individual' ELSE category END as 'category'
 ,pos_entry_mode
 ,SUM(ilosc) as ilosc
 ,SUM(wartosc) as wartosc

 from #dane
  where pos_entry_mode = 'CTLS'
 group by
  KRAJE
 ,CASE
	WHEN category in ('b.d.', 'Other') THEN 'Individual' ELSE category END
 ,pos_entry_mode

 order by 2
 
 ---split---
 
 --NBP - ST.05 v_trans VISA i MC z podziałem na (business i Indyvidual)- .sql

/*
distinct z ostatniego kwartału:
0 - zbliżeniowo i moto
1 - PIN
5 - podpis
6 - inne


9 - Consumer device cardholder verification
B - Consumer device cardholder verification with code
D - Consumer device cardholder verification with biometric

Dodatkowo:
A - Unknown (ale raczej też elektronicznie)
C - Consumer device cardholder verification with pattern

*/

 select 
 KRAJE
 ,category
 ,SUM(ilosc) as ilosc
 ,SUM(wartosc) as wartosc

 from #dane_zwroty
 group by
  KRAJE
 ,category

 
