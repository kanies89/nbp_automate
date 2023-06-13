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
	'VISA'as 'karta'
	,case 
		WHEN VT.country IN ('AUT', 'AT') THEN 'Austria'
		WHEN VT.country IN ('BEL', 'BE') THEN 'Belgia'
		WHEN VT.country IN ('BG', 'BGR') THEN 'Bułgaria'
		WHEN VT.country IN ('HR', 'HRV') THEN 'Chorwacja'
		WHEN VT.country IN ('CY', 'CYP') THEN 'Cypr'
		WHEN VT.country IN ('CZ', 'CZE') THEN 'Czechy'
		WHEN VT.country IN ('DK', 'DNK') THEN 'Dania'
		WHEN VT.country IN ('EE', 'EST') THEN 'Estonia'
		WHEN VT.country IN ('FIN', 'FI') THEN 'Finlandia'
		WHEN VT.country IN ('FR', 'FRA') THEN 'Francja'
		WHEN VT.country IN ('GE', 'GEO') THEN 'Grecja'
		WHEN VT.country IN ('ES', 'ESP') THEN 'Hiszpania'
		WHEN VT.country IN ('NL', 'NLD') THEN 'Holandia'
		WHEN VT.country IN ('IE', 'IRL') THEN 'Irlandia'
		WHEN VT.country IN ('IS', 'ISL') THEN 'Islandia'
		WHEN VT.country IN ('LT', 'LTU') THEN 'Litwa'
		WHEN VT.country IN ('LI', 'LIE') THEN 'Liechtenstein'
		WHEN VT.country IN ('LU', 'LUX') THEN 'Luksemburg'
		WHEN VT.country IN ('LV', 'LVA') THEN 'Łotwa'
		WHEN VT.country IN ('MLT', 'MT') THEN 'Malta'
		WHEN VT.country IN ('DE', 'DEU') THEN 'Niemcy'
		WHEN VT.country IN ('NO', 'NOR') THEN 'Norwegia'
		WHEN VT.country IN ('PRT', 'PT') THEN 'Portugalia'
		WHEN VT.country IN ('RO', 'ROM') THEN 'Rumunia'
		WHEN VT.country IN ('SK', 'SVK') THEN 'Słowacja'
		WHEN VT.country IN ('SI', 'SVN') THEN 'Słowenia'
		WHEN VT.country IN ('SE', 'SWE') THEN 'Szwecja'
		WHEN VT.country IN ('HU', 'HUN') THEN 'Węgry'
		WHEN VT.country IN ('IT', 'ITA') THEN 'Włochy'
		WHEN VT.country = 'PL'   THEN 'KRAJOWE'
		ELSE 'Pozostałe kraje świata (poza EOG)' 
		END as podzial_NBP
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
	case 
		WHEN VT.country IN ('AUT', 'AT') THEN 'Austria'
		WHEN VT.country IN ('BEL', 'BE') THEN 'Belgia'
		WHEN VT.country IN ('BG', 'BGR') THEN 'Bułgaria'
		WHEN VT.country IN ('HR', 'HRV') THEN 'Chorwacja'
		WHEN VT.country IN ('CY', 'CYP') THEN 'Cypr'
		WHEN VT.country IN ('CZ', 'CZE') THEN 'Czechy'
		WHEN VT.country IN ('DK', 'DNK') THEN 'Dania'
		WHEN VT.country IN ('EE', 'EST') THEN 'Estonia'
		WHEN VT.country IN ('FIN', 'FI') THEN 'Finlandia'
		WHEN VT.country IN ('FR', 'FRA') THEN 'Francja'
		WHEN VT.country IN ('GE', 'GEO') THEN 'Grecja'
		WHEN VT.country IN ('ES', 'ESP') THEN 'Hiszpania'
		WHEN VT.country IN ('NL', 'NLD') THEN 'Holandia'
		WHEN VT.country IN ('IE', 'IRL') THEN 'Irlandia'
		WHEN VT.country IN ('IS', 'ISL') THEN 'Islandia'
		WHEN VT.country IN ('LT', 'LTU') THEN 'Litwa'
		WHEN VT.country IN ('LI', 'LIE') THEN 'Liechtenstein'
		WHEN VT.country IN ('LU', 'LUX') THEN 'Luksemburg'
		WHEN VT.country IN ('LV', 'LVA') THEN 'Łotwa'
		WHEN VT.country IN ('MLT', 'MT') THEN 'Malta'
		WHEN VT.country IN ('DE', 'DEU') THEN 'Niemcy'
		WHEN VT.country IN ('NO', 'NOR') THEN 'Norwegia'
		WHEN VT.country IN ('PRT', 'PT') THEN 'Portugalia'
		WHEN VT.country IN ('RO', 'ROM') THEN 'Rumunia'
		WHEN VT.country IN ('SK', 'SVK') THEN 'Słowacja'
		WHEN VT.country IN ('SI', 'SVN') THEN 'Słowenia'
		WHEN VT.country IN ('SE', 'SWE') THEN 'Szwecja'
		WHEN VT.country IN ('HU', 'HUN') THEN 'Węgry'
		WHEN VT.country IN ('IT', 'ITA') THEN 'Włochy'
		WHEN VT.country = 'PL'   THEN 'KRAJOWE'
		ELSE 'Pozostałe kraje świata (poza EOG)' 
		END
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

UNION ALL
--transakcje MC
SELECT 
	'MC' as 'karta'
	,case 
		WHEN MC.country IN ('AUT', 'AT') THEN 'Austria'
		WHEN MC.country IN ('BEL', 'BE') THEN 'Belgia'
		WHEN MC.country IN ('BG', 'BGR') THEN 'Bułgaria'
		WHEN MC.country IN ('HR', 'HRV') THEN 'Chorwacja'
		WHEN MC.country IN ('CY', 'CYP') THEN 'Cypr'
		WHEN MC.country IN ('CZ', 'CZE') THEN 'Czechy'
		WHEN MC.country IN ('DK', 'DNK') THEN 'Dania'
		WHEN MC.country IN ('EE', 'EST') THEN 'Estonia'
		WHEN MC.country IN ('FIN', 'FI') THEN 'Finlandia'
		WHEN MC.country IN ('FR', 'FRA') THEN 'Francja'
		WHEN MC.country IN ('GE', 'GEO') THEN 'Grecja'
		WHEN MC.country IN ('ES', 'ESP') THEN 'Hiszpania'
		WHEN MC.country IN ('NL', 'NLD') THEN 'Holandia'
		WHEN MC.country IN ('IE', 'IRL') THEN 'Irlandia'
		WHEN MC.country IN ('IS', 'ISL') THEN 'Islandia'
		WHEN MC.country IN ('LT', 'LTU') THEN 'Litwa'
		WHEN MC.country IN ('LI', 'LIE') THEN 'Liechtenstein'
		WHEN MC.country IN ('LU', 'LUX') THEN 'Luksemburg'
		WHEN MC.country IN ('LV', 'LVA') THEN 'Łotwa'
		WHEN MC.country IN ('MLT', 'MT') THEN 'Malta'
		WHEN MC.country IN ('DE', 'DEU') THEN 'Niemcy'
		WHEN MC.country IN ('NO', 'NOR') THEN 'Norwegia'
		WHEN MC.country IN ('PRT', 'PT') THEN 'Portugalia'
		WHEN MC.country IN ('RO', 'ROM') THEN 'Rumunia'
		WHEN MC.country IN ('SK', 'SVK') THEN 'Słowacja'
		WHEN MC.country IN ('SI', 'SVN') THEN 'Słowenia'
		WHEN MC.country IN ('SE', 'SWE') THEN 'Szwecja'
		WHEN MC.country IN ('HU', 'HUN') THEN 'Węgry'
		WHEN MC.country IN ('IT', 'ITA') THEN 'Włochy'
		WHEN MC.country = 'POL'   THEN 'KRAJOWE'
		ELSE 'Pozostałe kraje świata (poza EOG)' 
		END as podzial_NBP
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
	case 
		WHEN MC.country IN ('AUT', 'AT') THEN 'Austria'
		WHEN MC.country IN ('BEL', 'BE') THEN 'Belgia'
		WHEN MC.country IN ('BG', 'BGR') THEN 'Bułgaria'
		WHEN MC.country IN ('HR', 'HRV') THEN 'Chorwacja'
		WHEN MC.country IN ('CY', 'CYP') THEN 'Cypr'
		WHEN MC.country IN ('CZ', 'CZE') THEN 'Czechy'
		WHEN MC.country IN ('DK', 'DNK') THEN 'Dania'
		WHEN MC.country IN ('EE', 'EST') THEN 'Estonia'
		WHEN MC.country IN ('FIN', 'FI') THEN 'Finlandia'
		WHEN MC.country IN ('FR', 'FRA') THEN 'Francja'
		WHEN MC.country IN ('GE', 'GEO') THEN 'Grecja'
		WHEN MC.country IN ('ES', 'ESP') THEN 'Hiszpania'
		WHEN MC.country IN ('NL', 'NLD') THEN 'Holandia'
		WHEN MC.country IN ('IE', 'IRL') THEN 'Irlandia'
		WHEN MC.country IN ('IS', 'ISL') THEN 'Islandia'
		WHEN MC.country IN ('LT', 'LTU') THEN 'Litwa'
		WHEN MC.country IN ('LI', 'LIE') THEN 'Liechtenstein'
		WHEN MC.country IN ('LU', 'LUX') THEN 'Luksemburg'
		WHEN MC.country IN ('LV', 'LVA') THEN 'Łotwa'
		WHEN MC.country IN ('MLT', 'MT') THEN 'Malta'
		WHEN MC.country IN ('DE', 'DEU') THEN 'Niemcy'
		WHEN MC.country IN ('NO', 'NOR') THEN 'Norwegia'
		WHEN MC.country IN ('PRT', 'PT') THEN 'Portugalia'
		WHEN MC.country IN ('RO', 'ROM') THEN 'Rumunia'
		WHEN MC.country IN ('SK', 'SVK') THEN 'Słowacja'
		WHEN MC.country IN ('SI', 'SVN') THEN 'Słowenia'
		WHEN MC.country IN ('SE', 'SWE') THEN 'Szwecja'
		WHEN MC.country IN ('HU', 'HUN') THEN 'Węgry'
		WHEN MC.country IN ('IT', 'ITA') THEN 'Włochy'
		WHEN MC.country = 'POL'   THEN 'KRAJOWE'
		ELSE 'Pozostałe kraje świata (poza EOG)'
		END
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

--select * from #dane





IF OBJECT_ID('tempdb..#geo3') IS NOT NULL DROP TABLE #geo3
CREATE TABLE #geo3 (num smallint, code varchar(2), name varchar(256))
INSERT INTO #geo3 VALUES (1, 'AT', 'Austria')
INSERT INTO #geo3 VALUES (2, 'BE', 'Belgia')
INSERT INTO #geo3 VALUES (3, 'BG', 'Bułgaria')
INSERT INTO #geo3 VALUES (4, 'HR', 'Chorwacja')
INSERT INTO #geo3 VALUES (5, 'CY', 'Cypr')
INSERT INTO #geo3 VALUES (6, 'CZ', 'Czechy')
INSERT INTO #geo3 VALUES (7, 'DK', 'Dania')
INSERT INTO #geo3 VALUES (8, 'EE', 'Estonia')
INSERT INTO #geo3 VALUES (9, 'FI', 'Finlandia')
INSERT INTO #geo3 VALUES (10, 'FR', 'Francja')
INSERT INTO #geo3 VALUES (11, 'GR', 'Grecja')
INSERT INTO #geo3 VALUES (12, 'ES', 'Hiszpania')
INSERT INTO #geo3 VALUES (13, 'NL', 'Holandia')
INSERT INTO #geo3 VALUES (14, 'IE', 'Irlandia')
INSERT INTO #geo3 VALUES (15, 'IS', 'Islandia')
INSERT INTO #geo3 VALUES (16, 'LT', 'Litwa ')
INSERT INTO #geo3 VALUES (17, 'LI', 'Liechtenstein')
INSERT INTO #geo3 VALUES (18, 'LU', 'Luksemburg')
INSERT INTO #geo3 VALUES (19, 'LV', 'Łotwa')
INSERT INTO #geo3 VALUES (20, 'MT', 'Malta')
INSERT INTO #geo3 VALUES (21, 'DE', 'Niemcy')
INSERT INTO #geo3 VALUES (22, 'NO', 'Norwegia')
INSERT INTO #geo3 VALUES (23, 'PL', 'Polska')
INSERT INTO #geo3 VALUES (24, 'PT', 'Portugalia')
INSERT INTO #geo3 VALUES (25, 'RO', 'Rumunia')
INSERT INTO #geo3 VALUES (26, 'SK', 'Słowacja')
INSERT INTO #geo3 VALUES (27, 'SI', 'Słowenia')
INSERT INTO #geo3 VALUES (28, 'SE', 'Szwecja')
INSERT INTO #geo3 VALUES (29, 'HU', 'Węgry')
INSERT INTO #geo3 VALUES (30, 'IT', 'Włochy')
INSERT INTO #geo3 VALUES (31, 'W2', 'Krajowe')
INSERT INTO #geo3 VALUES (32, 'G1', 'Pozostałe kraje świata (poza EOG)') 