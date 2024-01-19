-- RAPORT NBP zakładka 4a.R.L_PLiW2   oraz  4a.R.W_PLiW2      oraz 6.ab.LiW
--Liczba transakcji - transakcje płatnicze zrealizowane w oparciu o kartę w urządzeniach akceptujących karty płatnicze [w tym krajowe transakcje - W2] [kraj lokalizacji terminala = PL] [otrzymane]
      --  (liczba i wartość transakcji kartowych, bez blika)


--q1 2023 - 5 transakcji gdzie typ karty = null <<----------------- co z tym??
--6 transakcji typ karty = charge  <<----------------- co z tym??

SET TRANSACTION ISOLATION LEVEL READ COMMITTED
USE paytel_olap

declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1, '19000101');
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-0 , '19000101');
select @dtb,@dte

--transakcje VISA
IF OBJECT_ID('tempdb..#dane') IS NOT NULL DROP TABLE #dane
SELECT
	'VISA' as 'karta',
	VT.country
	,mcc
	,CASE WHEN accountFundingSource IN ('C','R') THEN 'Credit'
		WHEN accountFundingSource IN ('P','D') THEN 'Debit' 
		WHEN accountFundingSource = 'H' THEN 'Charge'
		ELSE accountFundingSource
		END AS 'Typ_karty'
	,CASE
		WHEN substring(te_pos_entry_mode, 1, 2) in ('02','90') then 'MS'
		WHEN substring(te_pos_entry_mode, 1, 2) in ('04','05', '95') then 'CHIP'
		WHEN substring(te_pos_entry_mode, 1, 2) in ('07','91') then 'CTLS'
		ELSE te_pos_entry_mode end as te_pos_entry_mode
	,IIF(substring(te_pos_entry_mode, 1, 2) = '01', 'MOTO', 'inne') as czy_moto
	,CASE WHEN abs(tr_amount)<=10000 and substring(te_pos_entry_mode, 1, 2) in ('07','91') THEN 1
	ELSE 0 end as czy_niskokwotowa_zblizeniowa
	,IIF(trsd_tran_nr is null, 0, 1) as czy_SCA
	,count(*) as 'ilosc'
	,sum(convert(money,abs((tr_amount/100)))) as 'wartosc_transakcji'
	,te_tran_type
	,sum(convert(money,abs((tr_cash_req/100))))as 'Wartość wypłat Cash Back'
	,vp_bio as 'category'
	,tr_rsp_code
	,tr_app_id

INTO #dane
FROM paytel_olap.dbo.visa_transaction VT (nolock) 
	join paytel_olap.dbo.if_transaction IT (nolock) on IT.postTranId = VT.postTranId 
	join paytel_olap.dbo.trans (nolock) on tranNr = tr_tran_nr
			and tr_datetime_req between @dtb AND @dte 
		and tr_reversed = 0
		and tr_rsp_code = '00'   
		and tr_message_type in (200, 220)
	join paytel_olap.dbo.trans_ext (nolock) on tr_tran_nr = te_tran_nr
	join paytel_olap.dbo.mcc_visa_group on mcc=merchant_category_code
	left join paytel_olap.dbo.country_codes CS on VT.country=cc_A2
	left join paytel_olap.dbo.visa_product_id on VT.productId=vp_product_id
	left join paytel_olap.dbo.trans_structured_data as sc1 on sc1.trsd_tran_nr = tr_tran_nr  and trsd_log_sc1=1


GROUP BY 
	VT.country
	,mcc
	,CASE 
		WHEN accountFundingSource IN ('C','R') THEN 'Credit'
		WHEN accountFundingSource IN ('P','D') THEN 'Debit' 
		WHEN accountFundingSource = 'H' THEN 'Charge'
		ELSE accountFundingSource
		END
	,CASE
		WHEN substring(te_pos_entry_mode, 1, 2) in ('02','90') then 'MS'
		WHEN substring(te_pos_entry_mode, 1, 2) in ('04','05', '95') then 'CHIP'
		WHEN substring(te_pos_entry_mode, 1, 2) in ('07','91') then 'CTLS'
		ELSE te_pos_entry_mode end
	,IIF(substring(te_pos_entry_mode, 1, 2) = '01', 'MOTO', 'inne')
	,CASE WHEN abs(tr_amount)<=10000 and substring(te_pos_entry_mode, 1, 2) in ('07','91') THEN 1
				ELSE 0 end
	,IIF(trsd_tran_nr is null, 0, 1)
	,te_tran_type
	,tr_cash_req
	,vp_bio
	,tr_rsp_code
	,tr_app_id

UNION ALL
--transakcje MC
SELECT 
	'MC' as 'karta',
	MC.country,
	mcc
	,CASE WHEN ipc_category1 = 'C' THEN 'Credit'
		WHEN ipc_category1 IN ('P','D') THEN 'Debit' 
		WHEN ipc_category1 = 'CH' THEN 'Charge'
		ELSE ipc_category1
		END AS 'Typ_karty'
	,CASE
		WHEN substring(te_pos_entry_mode, 1, 2) in ('02','90') then 'MS'
		WHEN substring(te_pos_entry_mode, 1, 2) in ('04','05', '95') then 'CHIP'
		WHEN substring(te_pos_entry_mode, 1, 2) in ('07','91') then 'CTLS'
		ELSE te_pos_entry_mode end as te_pos_entry_mode
	,IIF(substring(te_pos_entry_mode, 1, 2) = '01', 'MOTO', 'inne') as czy_moto
	,CASE WHEN abs(tr_amount)<=10000 and substring(te_pos_entry_mode, 1, 2) in ('07','91') THEN 1
				ELSE 0 end as czy_niskokwotowa_zblizeniowa
	,IIF(trsd_tran_nr is null, 0, 1) as czy_SCA
	,count(*) as 'ilość transakcji'
	,sum(convert(money,abs(tr_amount/100))) as 'wartosc_transakcji'
	,te_tran_type
	,sum(convert(money,abs((tr_cash_req/100))))as 'Wartość wypłat Cash Back'
	, CASE 
	WHEN ipc_category2 = 'B' THEN 'BUSINESS'
	WHEN ipc_category2 = 'C' THEN 'Individual'
	ELSE 'b.d.' END as 'category'
	,tr_rsp_code
	,tr_app_id

FROM 
	mc_transaction MC (nolock)
	join paytel_olap.dbo.if_transaction TR (nolock) on TR.postTranId = MC.postTranId 
	JOIN paytel_olap.dbo.trans (NOLOCK) ON isnull(tr_prev_tran_nr, tr_tran_nr) = TR.tranNr
		and tr_datetime_req between @dtb AND @dte 
		and tr_reversed = 0
		and tr_rsp_code = '00'   
		and tr_message_type in (200, 220)
	join paytel_olap.dbo.trans_ext (nolock) on tr_tran_nr = te_tran_nr
	left join paytel_olap.dbo.country_codes CS on MC.country = cc_A3
	LEFT JOIN paytel_olap.dbo.if_product_category (NOLOCK) ON gcmsProductId = ipc_product_id
	left join paytel_olap.dbo.trans_structured_data as sc1 on sc1.trsd_tran_nr = tr_tran_nr  and trsd_log_sc1=1

GROUP BY 
	MC.country,
	mcc
	,CASE WHEN ipc_category1 = 'C' THEN 'Credit'
		WHEN ipc_category1 IN ('P','D') THEN 'Debit' 
		WHEN ipc_category1 = 'CH' THEN 'Charge'
		ELSE ipc_category1
			END
	,CASE
		WHEN substring(te_pos_entry_mode, 1, 2) in ('02','90') then 'MS'
		WHEN substring(te_pos_entry_mode, 1, 2) in ('04','05', '95') then 'CHIP'
		WHEN substring(te_pos_entry_mode, 1, 2) in ('07','91') then 'CTLS'
		ELSE te_pos_entry_mode end
	,IIF(substring(te_pos_entry_mode, 1, 2) = '01', 'MOTO', 'inne')
	,CASE WHEN abs(tr_amount)<=10000 and substring(te_pos_entry_mode, 1, 2) in ('07','91') THEN 1
				ELSE 0 end
	,IIF(trsd_tran_nr is null, 0, 1)
	,te_tran_type
	,tr_cash_req
	,CASE 
	WHEN ipc_category2 = 'B' THEN 'BUSINESS'
	WHEN ipc_category2 = 'C' THEN 'Individual'
	ELSE 'b.d.' END
	,tr_rsp_code
	,tr_app_id
