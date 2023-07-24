--NBP - ST.06 Trans VISA i MC z podzia³em na Inne Kraje .sql
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED
USE paytel_olap

declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1, '19000101');
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-0 , '19000101');
select @dtb,@dte

--transakcje VISA
SELECT
'VISA'as 'karta',
 CASE
	WHEN  VT.country = 'ROM' THEN 'Romania'
	WHEN  VT.country in ('QZ', 'QZZ') THEN 'Kosowo'
	WHEN  cc_name = 'Germany' THEN 'Niemcy'
	WHEN cc_name = 'Spain' THEN 'Hiszpania'  ELSE cc_name end as CountryName, VT.country as CountryCode, 
 count(*) as 'ilosc', 
 sum(convert(money,abs((tr_amount))))/100 as 'wartoœæ transakcji',
  0 as 'ilosc_internet',
    0 as 'wartosc_internet',
 count(case when tr_cash_req > 0 then 1 END) as 'iloœæ transakcji CashBack',
 sum(convert(money,abs((tr_cash_req/100))))as 'Wartoœæ wyp³at CashBack',

 case 
  WHEN cc_name in (
  'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Greece', 
  'Spain', 'Netherlands', 'Ireland', 'Lithuania', 'Luxembourg', 'Latvia', 'Germany', 'Malta', 'Portugal', 'Romania', 'Slovakia', 
  'Slovenia', 'Sweden', 'Hungary', 'Italy', 'Norway', 'Liechtenstein', 'Iceland') THEN 'wyró¿nione'
 ELSE 'reszta œwiata' END 'podzia³ NBP'

FROM 
 visa_transaction VT (nolock) 
 join if_transaction IT (nolock) on IT.postTranId = VT.postTranId 
 join trans (nolock) on tranNr = tr_tran_nr
	 and  tr_datetime_req between @dtb AND @dte
	 and tr_reversed = 0 AND tr_rsp_code = '00'
	 and tr_message_type in (200, 220)
 join trans_ext (nolock) on tr_tran_nr = te_tran_nr
 join mcc_visa_group on mcc=merchant_category_code
 left join country_codes CS on VT.country=cc_A2
    left join visa_product_id on VT.productId=vp_product_id

WHERE 
 VT.country <> 'PL' --Kraje poza polsk¹

GROUP BY 
 cc_name, VT.country 
 
UNION ALL

--transakcje MC
SELECT 
'MC' as 'karta',
 CASE
	WHEN MC.country = 'ROM' THEN 'Romania'
	WHEN MC.country in ('QZ', 'QZZ') THEN 'Kosowo'
	WHEN cc_name = 'Germany' THEN 'Niemcy' 
	WHEN cc_name = 'Spain' THEN 'Hiszpania' 
	ELSE cc_name end as CountryName, MC.country as CountryCode, 
 count(*) as 'iloœæ transakcji', 
 sum(convert(money,abs(tr_amount)))/100 as 'wartoœæ transakcji',
   0 as 'ilosc_internet',
    0 as 'wartosc_internet',
 count(case when tr_cash_req > 0 then 1 END) as 'iloœæ transakcji CashBack',
 sum(convert(money,abs(tr_cash_req/100)))as 'Wartoœæ wyp³at CashBack',

 case 
  WHEN MC.country IN ('AUT','BEL','BGR','HRV','CYP','CZE','DNK','EST','FIN','FRA','GRC','ESP','NLD','IRL','LTU',
  'LUX','LVA','DEU','MLT','PRT','ROM','SVK','SVN','SWE','HUN','ITA', 'IS', 'LI', 'NO', 'GB') THEN 'wyró¿nione'
  ELSE 'reszta œwiata' END 'podzia³ NBP'
    
 -- 'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Greece', 
 -- 'Spain', 'Netherlands', 'Ireland', 'Lithuania', 'Luxembourg', 'Latvia', 'Germany', 'Malta', 'Portugal', 'Romania', 'Slovakia', 
 -- 'Slovenia', 'Sweden', 'Hungary', 'United Kingdom of Great Britain and Northern Ireland', 'Italy', 'Norway', 'Liechtenstein', 'Iceland', 'United Kingdom of Great Britain and Northern Ireland') THEN 'wyró¿nione'
 --ELSE 'reszta œwiata' END 'podzia³ NBP'

FROM 
 mc_transaction MC (nolock)
 join if_transaction TR (nolock) on TR.postTranId = MC.postTranId
 join trans (nolock) on TR.tranNr = tr_tran_nr 
	and tr_datetime_req between @dtb AND @dte 
	 and tr_reversed = 0
	 and tr_rsp_code = '00'   
	 and tr_message_type in (200, 220)
 join trans_ext (nolock) on tr_tran_nr = te_tran_nr
 --left Join mcipm_ip0072t1 on MC.memberId = mcipm_ip0072t1.member_id 
 left join country_codes CS on MC.country = cc_A3   

WHERE 
 MC.country <> 'POL'   --Kraje poza polsk¹

GROUP BY 
	cc_name, MC.country
  --case 
  --WHEN MC.country IN ('AUT','BEL','BGR','HRV','CYP','CZE','DNK','EST','FIN','FRA','GRC','ESP','NLD','IRL','LTU',
  --'LUX','LVA','DEU','MLT','PRT','ROM','SVK','SVN','SWE','HUN','GBR','ITA', 'IS', 'LI', 'NO', 'GB') THEN 'wyró¿nione'
  --ELSE 'reszta œwiata' END

ORDER BY 8 desc, 1, 2, 3 DESC