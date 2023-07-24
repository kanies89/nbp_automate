--NBP - ST.05 CashBack - Trans VISA i MC z podzia³em na (business i Indyvidual)- .sql
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED
USE paytel_olap

declare @dtb as smalldatetime
declare @dte as smalldatetime
declare @te_tran_type as int

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1, '19000101');
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-0 , '19000101');
select @dtb,@dte
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
 --sum(convert(money,abs((tr_amount/100)))) as 'Wartoœæ transakcji typu CashBack',
 sum(convert(money,abs((tr_cash_req/100))))as 'Wartoœæ wyp³at Cash Back'

FROM 
 visa_transaction VT (nolock) 
 join if_transaction IT (nolock) on IT.postTranId = VT.postTranId 
 join trans (nolock) on tranNr = tr_tran_nr
 	 and tr_datetime_req between @dtb AND @dte 
	 and tr_reversed = 0
	 and tr_rsp_code = '00'   
	 and tr_message_type in (200,220)
 join trans_ext (nolock) on tr_tran_nr = te_tran_nr
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
 --sum(convert(money,abs((tr_amount/100)))) as 'Wartoœæ transakcji typu CashBack',
 sum(convert(money,abs((tr_cash_req/100))))as 'Wartoœæ wyp³at Cash Back'

FROM 
 mc_transaction MC (nolock)
 join if_transaction TR (nolock) on TR.postTranId = MC.postTranId
 join trans (nolock) on TR.tranNr = tr_tran_nr 
	 and tr_datetime_req between @dtb AND @dte 
	 and tr_reversed = 0
	 and tr_rsp_code = '00'   
	 and tr_message_type in (200,220)
 join trans_ext (nolock) on tr_tran_nr = te_tran_nr
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