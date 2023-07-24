--NBP - ST.05 Trans VISA i MC z podzia³em na (business i Indyvidual)- .sql
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED
USE paytel_olap

/*
distinct z ostatniego kwarta³u:
0 - zbli¿eniowo i moto
1 - PIN
5 - podpis
6 - inne


9 - Consumer device cardholder verification
B - Consumer device cardholder verification with code
D - Consumer device cardholder verification with biometric

Dodatkowo:
A - Unknown (ale raczej te¿ elektronicznie)
C - Consumer device cardholder verification with pattern

*/
declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1, '19000101');
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-0 , '19000101');
select @dtb,@dte

IF OBJECT_ID('tempdb..#dane_zwroty') IS NOT NULL DROP TABLE #dane_zwroty
--transakcje VISA
SELECT
 'VISA' as 'karta',
  CASE 
  WHEN  VT.country = 'PL' THEN 'POLSKA'
  WHEN VT.country is null THEN 'NULL'
 ELSE 'INNE KRAJE' END as 'KRAJE',
 vp_bio as 'category',
 count(*) as ilosc, sum(convert(money,(abs(tr_amount/100)))) as wartosc
INTO #dane_zwroty
FROM 
 visa_transaction VT (nolock) 
 join if_transaction IT (nolock) on IT.postTranId = VT.postTranId 
 join trans (nolock) on tranNr = tr_tran_nr
	 and tr_datetime_req BETWEEN @dtb AND @dte
	 AND tr_reversed = 0 
	 AND tr_rsp_code IN ('00')
	 AND tr_message_type in (200, 220)
 join mcc_visa_group (nolock) on mcc=merchant_category_code
 join trans_ext (nolock) on tr_tran_nr = te_tran_nr
  and te_tran_type ='20'
 left join country_codes CS (nolock) on VT.country=cc_A2
 left join visa_product_id (nolock) on VT.productId=vp_product_id


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
  WHEN MC.country is null THEN 'kto wie'
   ELSE 'INNE KRAJE' END AS 'KRAJE',

 CASE 
  WHEN ipc_category2 = 'B' THEN 'BUSINESS'
  WHEN ipc_category2 = 'C' THEN 'Individual'
    ELSE 'b.d.' END as 'category',
 COUNT(*) as TotalTrans, sum(convert(money,abs(tr_amount/100))) as ValueofTrans

FROM 
 mc_transaction MC (nolock)
 join if_transaction TR (nolock) on TR.postTranId = MC.postTranId
 join trans (nolock) on TR.tranNr = tr_tran_nr 
 	 and   tr_datetime_req BETWEEN @dtb AND @dte
	 AND tr_reversed = 0 
	 AND tr_rsp_code IN ('00')
	 AND tr_message_type in (200, 220)
 join trans_ext (nolock) on tr_tran_nr = te_tran_nr
  and te_tran_type ='20'
 --left Join mcipm_ip0072t1 on MC.memberId=mcipm_ip0072t1.member_id 
 --left join country_codes CS on mcipm_ip0072t1.country_code=cc_A3
 left join if_product_category (NOLOCK) ON gcmsProductId = ipc_product_id   
 
group by
 
 CASE
  WHEN MC.country ='POL' THEN 'POLSKA'
    WHEN MC.country is null THEN 'kto wie'
   ELSE 'INNE KRAJE' END,

 CASE 
	WHEN ipc_category2 = 'B' THEN 'BUSINESS'
	 WHEN ipc_category2 = 'C' THEN 'Individual'
  ELSE 'b.d.' END
 ORDER BY 1, 2, 3 DESC

 select 
 KRAJE
 ,category
 ,SUM(ilosc) as ilosc
 ,SUM(wartosc) as wartosc

 from #dane_zwroty
 group by
  KRAJE
 ,category

 
