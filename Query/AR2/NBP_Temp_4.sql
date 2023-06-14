-- RAPORT NBP zakładka 9.R.L.MCC oraz 9.R.W.MCC
-- Liczba transakcji - transakcje płatnicze zrealizowane w oparciu o kartę w podziale na kody MCC [otrzymane]
      --  (liczba i wartość transakcji kartowych, bez blika)
use paytel_olap

set transaction isolation level read uncommitted

declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1, '19000101');
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-0 , '19000101');

--transakcje VISA
IF OBJECT_ID('tempdb..#dane') IS NOT NULL DROP TABLE #dane
SELECT
	'VISA'as 'karta'
	,merchant_category_code
	,CASE
		WHEN VT.country = 'QZ' THEN 'ZZ'   --- KOSOWO zaliczamy do D09 - Extra UE not allocated - wytyczne NBP, ZZ jako pomoc w sortowaniu
		WHEN VT.country = 'PR' THEN 'US'    -- Puerto Rico zaliczamy do US - wytyczne NBP
		WHEN VT.country = 'PL' THEN 'WA'    -- Polske oznaczamy jako W2 -wewnętrzne - wytyczne NBP , WA jako pomoc w sortowaniu
		WHEN VT.country is null THEN 'uwaga - coś nowego'
		ELSE VT.country
		END as country_code_NBP

	,CASE
		WHEN VT.country = 'QZ' THEN 'Extra UE not allocated'   --- KOSOWO zaliczamy do D09 - Extra UE not allocated - wytyczne NBP
		WHEN VT.country = 'PR' THEN 'United States of America'    -- Puerto Rico zaliczamy do US - wytyczne NBP
		WHEN VT.country = 'PL' THEN 'Poland'    -- Polske oznaczamy jako W2 -wewnętrzne - wytyczne NBP
		WHEN VT.country is null THEN 'uwaga - coś nowego'
		ELSE cc_name end as country_name
	,IIF(substring(te_pos_entry_mode, 1, 2) = '01', 'MOTO', 'inne') as czy_moto
	,count(*) as 'ilosc'
	,sum(convert(money,abs((tr_amount/100)))) as 'wartosc_transakcji'
INTO #dane
FROM visa_transaction VT (nolock) 
	join if_transaction IT (nolock) on IT.postTranId = VT.postTranId 
	join trans (nolock) on tranNr = tr_tran_nr
		and tr_datetime_req between @dtb AND @dte
		and tr_reversed = 0 AND tr_rsp_code = '00'
		and tr_message_type in (200, 220)
	join trans_ext (nolock) on tr_tran_nr = te_tran_nr
	join mcc_visa_group on mcc=merchant_category_code
	left join country_codes CS on VT.country=cc_A2
	left join visa_product_id on VT.productId=vp_product_id

GROUP BY 
	merchant_category_code
	,VT.country
	,CASE
		WHEN VT.country = 'QZ' THEN 'ZZ'   --- KOSOWO zaliczamy do D09 - Extra UE not allocated - wytyczne NBP, ZZ jako pomoc w sortowaniu
		WHEN VT.country = 'PR' THEN 'US'    -- Puerto Rico zaliczamy do US - wytyczne NBP
		WHEN VT.country = 'PL' THEN 'WA'    -- Polske oznaczamy jako W2 -wewnętrzne - wytyczne NBP , WA jako pomoc w sortowaniu
		WHEN VT.country is null THEN 'uwaga - coś nowego'
		ELSE VT.country
		END 
	,CASE
		WHEN VT.country = 'QZ' THEN 'Extra UE not allocated'   --- KOSOWO zaliczamy do D09 - Extra UE not allocated - wytyczne NBP
		WHEN VT.country = 'PR' THEN 'United States of America'    -- Puerto Rico zaliczamy do US - wytyczne NBP
		WHEN VT.country = 'PL' THEN 'Poland'    -- Polske oznaczamy jako W2 -wewnętrzne - wytyczne NBP
		WHEN VT.country is null THEN 'uwaga - coś nowego'
		ELSE cc_name end
	,IIF(substring(te_pos_entry_mode, 1, 2) = '01', 'MOTO', 'inne')
UNION ALL
--transakcje MC
SELECT 
	'MC' as 'karta'
	,merchant_category_code
	,CASE
-- przekształcenia kodow MC na standard VISA(NBP)
		WHEN MC.country ='AFG' THEN 'AF'
		WHEN MC.country ='ALB' THEN 'AL'
		WHEN MC.country ='DZA' THEN 'DZ'
		WHEN MC.country ='ASM' THEN 'AS'
		WHEN MC.country ='AND' THEN 'AD'
		WHEN MC.country ='AGO' THEN 'AO'
		WHEN MC.country ='AIA' THEN 'AI'
		WHEN MC.country ='ATA' THEN 'AQ'
		WHEN MC.country ='ATG' THEN 'AG'
		WHEN MC.country ='ARG' THEN 'AR'
		WHEN MC.country ='ARM' THEN 'AM'
		WHEN MC.country ='ABW' THEN 'AW'
		WHEN MC.country ='AUS' THEN 'AU'
		WHEN MC.country ='AUT' THEN 'AT'
		WHEN MC.country ='AZE' THEN 'AZ'
		WHEN MC.country ='BHS' THEN 'BS'
		WHEN MC.country ='BHR' THEN 'BH'
		WHEN MC.country ='BGD' THEN 'BD'
		WHEN MC.country ='BRB' THEN 'BB'
		WHEN MC.country ='BLR' THEN 'BY'
		WHEN MC.country ='BEL' THEN 'BE'
		WHEN MC.country ='BLZ' THEN 'BZ'
		WHEN MC.country ='BEN' THEN 'BJ'
		WHEN MC.country ='BMU' THEN 'BM'
		WHEN MC.country ='BTN' THEN 'BT'
		WHEN MC.country ='BOL' THEN 'BO'
		WHEN MC.country ='BES' THEN 'BQ'
		WHEN MC.country ='BIH' THEN 'BA'
		WHEN MC.country ='BWA' THEN 'BW'
		WHEN MC.country ='BVT' THEN 'BV'
		WHEN MC.country ='BRA' THEN 'BR'
		WHEN MC.country ='IOT' THEN 'IO'
		WHEN MC.country ='BRN' THEN 'BN'
		WHEN MC.country ='BGR' THEN 'BG'
		WHEN MC.country ='BFA' THEN 'BF'
		WHEN MC.country ='BDI' THEN 'BI'
		WHEN MC.country ='CPV' THEN 'CV'
		WHEN MC.country ='KHM' THEN 'KH'
		WHEN MC.country ='CMR' THEN 'CM'
		WHEN MC.country ='CAN' THEN 'CA'
		WHEN MC.country ='CYM' THEN 'KY'
		WHEN MC.country ='CAF' THEN 'CF'
		WHEN MC.country ='TCD' THEN 'TD'
		WHEN MC.country ='CHL' THEN 'CL'
		WHEN MC.country ='CHN' THEN 'CN'
		WHEN MC.country ='CXR' THEN 'CX'
		WHEN MC.country ='CCK' THEN 'CC'
		WHEN MC.country ='COL' THEN 'CO'
		WHEN MC.country ='COM' THEN 'KM'
		WHEN MC.country ='COD' THEN 'CD'
		WHEN MC.country ='COG' THEN 'CG'
		WHEN MC.country ='COK' THEN 'CK'
		WHEN MC.country ='CRI' THEN 'CR'
		WHEN MC.country ='HRV' THEN 'HR'
		WHEN MC.country ='CUB' THEN 'CU'
		WHEN MC.country ='CUW' THEN 'CW'
		WHEN MC.country ='CYP' THEN 'CY'
		WHEN MC.country ='CZE' THEN 'CZ'
		WHEN MC.country ='CIV' THEN 'CI'
		WHEN MC.country ='DNK' THEN 'DK'
		WHEN MC.country ='DJI' THEN 'DJ'
		WHEN MC.country ='DMA' THEN 'DM'
		WHEN MC.country ='DOM' THEN 'DO'
		WHEN MC.country ='ECU' THEN 'EC'
		WHEN MC.country ='EGY' THEN 'EG'
		WHEN MC.country ='SLV' THEN 'SV'
		WHEN MC.country ='GNQ' THEN 'GQ'
		WHEN MC.country ='ERI' THEN 'ER'
		WHEN MC.country ='EST' THEN 'EE'
		WHEN MC.country ='SWZ' THEN 'SZ'
		WHEN MC.country ='ETH' THEN 'ET'
		WHEN MC.country ='FLK' THEN 'FK'
		WHEN MC.country ='FRO' THEN 'FO'
		WHEN MC.country ='FJI' THEN 'FJ'
		WHEN MC.country ='FIN' THEN 'FI'
		WHEN MC.country ='FRA' THEN 'FR'
		WHEN MC.country ='GUF' THEN 'GF'
		WHEN MC.country ='PYF' THEN 'PF'
		WHEN MC.country ='ATF' THEN 'TF'
		WHEN MC.country ='GAB' THEN 'GA'
		WHEN MC.country ='GMB' THEN 'GM'
		WHEN MC.country ='GEO' THEN 'GE'
		WHEN MC.country ='DEU' THEN 'DE'
		WHEN MC.country ='GHA' THEN 'GH'
		WHEN MC.country ='GIB' THEN 'GI'
		WHEN MC.country ='GRC' THEN 'GR'
		WHEN MC.country ='GRL' THEN 'GL'
		WHEN MC.country ='GRD' THEN 'GD'
		WHEN MC.country ='GLP' THEN 'GP'
		WHEN MC.country ='GUM' THEN 'GU'
		WHEN MC.country ='GTM' THEN 'GT'
		WHEN MC.country ='GGY' THEN 'GG'
		WHEN MC.country ='GIN' THEN 'GN'
		WHEN MC.country ='GNB' THEN 'GW'
		WHEN MC.country ='GUY' THEN 'GY'
		WHEN MC.country ='HTI' THEN 'HT'
		WHEN MC.country ='HMD' THEN 'HM'
		WHEN MC.country ='VAT' THEN 'VA'
		WHEN MC.country ='HND' THEN 'HN'
		WHEN MC.country ='HKG' THEN 'HK'
		WHEN MC.country ='HUN' THEN 'HU'
		WHEN MC.country ='ISL' THEN 'IS'
		WHEN MC.country ='IND' THEN 'IN'
		WHEN MC.country ='IDN' THEN 'ID'
		WHEN MC.country ='IRN' THEN 'IR'
		WHEN MC.country ='IRQ' THEN 'IQ'
		WHEN MC.country ='IRL' THEN 'IE'
		WHEN MC.country ='IMN' THEN 'IM'
		WHEN MC.country ='ISR' THEN 'IL'
		WHEN MC.country ='ITA' THEN 'IT'
		WHEN MC.country ='JAM' THEN 'JM'
		WHEN MC.country ='JPN' THEN 'JP'
		WHEN MC.country ='JEY' THEN 'JE'
		WHEN MC.country ='JOR' THEN 'JO'
		WHEN MC.country ='KAZ' THEN 'KZ'
		WHEN MC.country ='KEN' THEN 'KE'
		WHEN MC.country ='KIR' THEN 'KI'
		WHEN MC.country ='PRK' THEN 'KP'
		WHEN MC.country ='KOR' THEN 'KR'
		WHEN MC.country ='KWT' THEN 'KW'
		WHEN MC.country ='KGZ' THEN 'KG'
		WHEN MC.country ='LAO' THEN 'LA'
		WHEN MC.country ='LVA' THEN 'LV'
		WHEN MC.country ='LBN' THEN 'LB'
		WHEN MC.country ='LSO' THEN 'LS'
		WHEN MC.country ='LBR' THEN 'LR'
		WHEN MC.country ='LBY' THEN 'LY'
		WHEN MC.country ='LIE' THEN 'LI'
		WHEN MC.country ='LTU' THEN 'LT'
		WHEN MC.country ='LUX' THEN 'LU'
		WHEN MC.country ='MAC' THEN 'MO'
		WHEN MC.country ='MDG' THEN 'MG'
		WHEN MC.country ='MWI' THEN 'MW'
		WHEN MC.country ='MYS' THEN 'MY'
		WHEN MC.country ='MDV' THEN 'MV'
		WHEN MC.country ='MLI' THEN 'ML'
		WHEN MC.country ='MLT' THEN 'MT'
		WHEN MC.country ='MHL' THEN 'MH'
		WHEN MC.country ='MTQ' THEN 'MQ'
		WHEN MC.country ='MRT' THEN 'MR'
		WHEN MC.country ='MUS' THEN 'MU'
		WHEN MC.country ='MYT' THEN 'YT'
		WHEN MC.country ='MEX' THEN 'MX'
		WHEN MC.country ='FSM' THEN 'FM'
		WHEN MC.country ='MDA' THEN 'MD'
		WHEN MC.country ='MCO' THEN 'MC'
		WHEN MC.country ='MNG' THEN 'MN'
		WHEN MC.country ='MNE' THEN 'ME'
		WHEN MC.country ='MSR' THEN 'MS'
		WHEN MC.country ='MAR' THEN 'MA'
		WHEN MC.country ='MOZ' THEN 'MZ'
		WHEN MC.country ='MMR' THEN 'MM'
		WHEN MC.country ='NAM' THEN 'NA'
		WHEN MC.country ='NRU' THEN 'NR'
		WHEN MC.country ='NPL' THEN 'NP'
		WHEN MC.country ='NLD' THEN 'NL'
		WHEN MC.country ='NCL' THEN 'NC'
		WHEN MC.country ='NZL' THEN 'NZ'
		WHEN MC.country ='NIC' THEN 'NI'
		WHEN MC.country ='NER' THEN 'NE'
		WHEN MC.country ='NGA' THEN 'NG'
		WHEN MC.country ='NIU' THEN 'NU'
		WHEN MC.country ='NFK' THEN 'NF'
		WHEN MC.country ='MNP' THEN 'MP'
		WHEN MC.country ='NOR' THEN 'NO'
		WHEN MC.country ='OMN' THEN 'OM'
		WHEN MC.country ='PAK' THEN 'PK'
		WHEN MC.country ='PLW' THEN 'PW'
		WHEN MC.country ='PSE' THEN 'PS'
		WHEN MC.country ='PAN' THEN 'PA'
		WHEN MC.country ='PNG' THEN 'PG'
		WHEN MC.country ='PRY' THEN 'PY'
		WHEN MC.country ='PER' THEN 'PE'
		WHEN MC.country ='PHL' THEN 'PH'
		WHEN MC.country ='PCN' THEN 'PN'
		WHEN MC.country ='POL' THEN 'WA' -- Polske oznaczamy jako W2 -wewnętrzne - wytyczne NBP, WA jako pomoc w sortowaniu
		WHEN MC.country ='PRT' THEN 'PT'
		WHEN MC.country ='PRI' THEN 'US' --  Puerto Rico zaliczamy do US - wytyczne NBP
		WHEN MC.country ='QAT' THEN 'QA'
		WHEN MC.country ='MKD' THEN 'MK'
		WHEN MC.country ='ROU' THEN 'RO'
		WHEN MC.country ='RUS' THEN 'RU'
		WHEN MC.country ='RWA' THEN 'RW'
		WHEN MC.country ='REU' THEN 'RE'
		WHEN MC.country ='BLM' THEN 'BL'
		WHEN MC.country ='SHN' THEN 'SH'
		WHEN MC.country ='KNA' THEN 'KN'
		WHEN MC.country ='LCA' THEN 'LC'
		WHEN MC.country ='MAF' THEN 'MF'
		WHEN MC.country ='SPM' THEN 'PM'
		WHEN MC.country ='VCT' THEN 'VC'
		WHEN MC.country ='WSM' THEN 'WS'
		WHEN MC.country ='SMR' THEN 'SM'
		WHEN MC.country ='STP' THEN 'ST'
		WHEN MC.country ='SAU' THEN 'SA'
		WHEN MC.country ='SEN' THEN 'SN'
		WHEN MC.country ='SRB' THEN 'RS'
		WHEN MC.country ='SYC' THEN 'SC'
		WHEN MC.country ='SLE' THEN 'SL'
		WHEN MC.country ='SGP' THEN 'SG'
		WHEN MC.country ='SXM' THEN 'SX'
		WHEN MC.country ='SVK' THEN 'SK'
		WHEN MC.country ='SVN' THEN 'SI'
		WHEN MC.country ='SLB' THEN 'SB'
		WHEN MC.country ='SOM' THEN 'SO'
		WHEN MC.country ='ZAF' THEN 'ZA'
		WHEN MC.country ='SGS' THEN 'GS'
		WHEN MC.country ='SSD' THEN 'SS'
		WHEN MC.country ='ESP' THEN 'ES'
		WHEN MC.country ='LKA' THEN 'LK'
		WHEN MC.country ='SDN' THEN 'SD'
		WHEN MC.country ='SUR' THEN 'SR'
		WHEN MC.country ='SJM' THEN 'SJ'
		WHEN MC.country ='SWE' THEN 'SE'
		WHEN MC.country ='CHE' THEN 'CH'
		WHEN MC.country ='SYR' THEN 'SY'
		WHEN MC.country ='TWN' THEN 'TW'
		WHEN MC.country ='TJK' THEN 'TJ'
		WHEN MC.country ='TZA' THEN 'TZ'
		WHEN MC.country ='THA' THEN 'TH'
		WHEN MC.country ='TLS' THEN 'TL'
		WHEN MC.country ='TGO' THEN 'TG'
		WHEN MC.country ='TKL' THEN 'TK'
		WHEN MC.country ='TON' THEN 'TO'
		WHEN MC.country ='TTO' THEN 'TT'
		WHEN MC.country ='TUN' THEN 'TN'
		WHEN MC.country ='TUR' THEN 'TR'
		WHEN MC.country ='TKM' THEN 'TM'
		WHEN MC.country ='TCA' THEN 'TC'
		WHEN MC.country ='TUV' THEN 'TV'
		WHEN MC.country ='UGA' THEN 'UG'
		WHEN MC.country ='UKR' THEN 'UA'
		WHEN MC.country ='ARE' THEN 'AE'
		WHEN MC.country ='GBR' THEN 'GB'
		WHEN MC.country ='UMI' THEN 'UM'
		WHEN MC.country ='USA' THEN 'US'
		WHEN MC.country ='URY' THEN 'UY'
		WHEN MC.country ='UZB' THEN 'UZ'
		WHEN MC.country ='VUT' THEN 'VU'
		WHEN MC.country ='VEN' THEN 'VE'
		WHEN MC.country ='VNM' THEN 'VN'
		WHEN MC.country ='VGB' THEN 'VG'
		WHEN MC.country ='VIR' THEN 'VI'
		WHEN MC.country ='WLF' THEN 'WF'
		WHEN MC.country ='ESH' THEN 'EH'
		WHEN MC.country ='YEM' THEN 'YE'
		WHEN MC.country ='ZMB' THEN 'ZM'
		WHEN MC.country ='ZWE' THEN 'ZW'
		WHEN MC.country ='ALA' THEN 'AX'
		--- dodatkowe zamiany:
		WHEN MC.country = 'ROM' THEN 'RO' 
		WHEN MC.country = 'QZZ' THEN 'ZZ'   --- KOSOWO , ZZ jako pomoc w sortowaniu
		ELSE 'uwaga - coś nowego'
		END as country_code_NBP
	,CASE
		WHEN MC.country = 'QZZ' THEN 'Extra UE not allocated'   --- KOSOWO zaliczamy do D09 - Extra UE not allocated - wytyczne NBP, ZZ jako pomoc w sortowaniu
		WHEN MC.country = 'PRI' THEN 'United States of America'    -- Puerto Rico zaliczamy do US - wytyczne NBP
		WHEN MC.country = 'PL' THEN 'Poland'    -- Polske oznaczamy jako W2 -wewnętrzne - wytyczne NBP, WA jako pomoc w sortowaniu
		WHEN MC.country is null THEN 'uwaga - coś nowego'
		WHEN MC.country = 'ROM' THEN 'Romania'
		ELSE cc_name end as country_name
	,IIF(substring(te_pos_entry_mode, 1, 2) = '01', 'MOTO', 'inne') as czy_moto
	,count(*) as 'ilość transakcji'
	,sum(convert(money,abs(tr_amount/100))) as 'wartosc_transakcji'
FROM 
	mc_transaction MC (nolock)
	join if_transaction TR (nolock) on TR.postTranId = MC.postTranId
	JOIN trans (NOLOCK) ON isnull(tr_prev_tran_nr, tr_tran_nr) = TR.tranNr
		and tr_datetime_req between @dtb AND @dte 
		and tr_reversed = 0
		and tr_rsp_code = '00'   
		and tr_message_type in (200,220)
	join trans_ext (nolock) on tr_tran_nr = te_tran_nr
	join mcc_visa_group on mcc=merchant_category_code
	left join country_codes CS on MC.country = cc_A3
	LEFT JOIN if_product_category (NOLOCK) ON gcmsProductId = ipc_product_id

GROUP BY 
	merchant_category_code
	,CASE
-- przekształcenia kodow MC na standard VISA(NBP)
		WHEN MC.country ='AFG' THEN 'AF'
		WHEN MC.country ='ALB' THEN 'AL'
		WHEN MC.country ='DZA' THEN 'DZ'
		WHEN MC.country ='ASM' THEN 'AS'
		WHEN MC.country ='AND' THEN 'AD'
		WHEN MC.country ='AGO' THEN 'AO'
		WHEN MC.country ='AIA' THEN 'AI'
		WHEN MC.country ='ATA' THEN 'AQ'
		WHEN MC.country ='ATG' THEN 'AG'
		WHEN MC.country ='ARG' THEN 'AR'
		WHEN MC.country ='ARM' THEN 'AM'
		WHEN MC.country ='ABW' THEN 'AW'
		WHEN MC.country ='AUS' THEN 'AU'
		WHEN MC.country ='AUT' THEN 'AT'
		WHEN MC.country ='AZE' THEN 'AZ'
		WHEN MC.country ='BHS' THEN 'BS'
		WHEN MC.country ='BHR' THEN 'BH'
		WHEN MC.country ='BGD' THEN 'BD'
		WHEN MC.country ='BRB' THEN 'BB'
		WHEN MC.country ='BLR' THEN 'BY'
		WHEN MC.country ='BEL' THEN 'BE'
		WHEN MC.country ='BLZ' THEN 'BZ'
		WHEN MC.country ='BEN' THEN 'BJ'
		WHEN MC.country ='BMU' THEN 'BM'
		WHEN MC.country ='BTN' THEN 'BT'
		WHEN MC.country ='BOL' THEN 'BO'
		WHEN MC.country ='BES' THEN 'BQ'
		WHEN MC.country ='BIH' THEN 'BA'
		WHEN MC.country ='BWA' THEN 'BW'
		WHEN MC.country ='BVT' THEN 'BV'
		WHEN MC.country ='BRA' THEN 'BR'
		WHEN MC.country ='IOT' THEN 'IO'
		WHEN MC.country ='BRN' THEN 'BN'
		WHEN MC.country ='BGR' THEN 'BG'
		WHEN MC.country ='BFA' THEN 'BF'
		WHEN MC.country ='BDI' THEN 'BI'
		WHEN MC.country ='CPV' THEN 'CV'
		WHEN MC.country ='KHM' THEN 'KH'
		WHEN MC.country ='CMR' THEN 'CM'
		WHEN MC.country ='CAN' THEN 'CA'
		WHEN MC.country ='CYM' THEN 'KY'
		WHEN MC.country ='CAF' THEN 'CF'
		WHEN MC.country ='TCD' THEN 'TD'
		WHEN MC.country ='CHL' THEN 'CL'
		WHEN MC.country ='CHN' THEN 'CN'
		WHEN MC.country ='CXR' THEN 'CX'
		WHEN MC.country ='CCK' THEN 'CC'
		WHEN MC.country ='COL' THEN 'CO'
		WHEN MC.country ='COM' THEN 'KM'
		WHEN MC.country ='COD' THEN 'CD'
		WHEN MC.country ='COG' THEN 'CG'
		WHEN MC.country ='COK' THEN 'CK'
		WHEN MC.country ='CRI' THEN 'CR'
		WHEN MC.country ='HRV' THEN 'HR'
		WHEN MC.country ='CUB' THEN 'CU'
		WHEN MC.country ='CUW' THEN 'CW'
		WHEN MC.country ='CYP' THEN 'CY'
		WHEN MC.country ='CZE' THEN 'CZ'
		WHEN MC.country ='CIV' THEN 'CI'
		WHEN MC.country ='DNK' THEN 'DK'
		WHEN MC.country ='DJI' THEN 'DJ'
		WHEN MC.country ='DMA' THEN 'DM'
		WHEN MC.country ='DOM' THEN 'DO'
		WHEN MC.country ='ECU' THEN 'EC'
		WHEN MC.country ='EGY' THEN 'EG'
		WHEN MC.country ='SLV' THEN 'SV'
		WHEN MC.country ='GNQ' THEN 'GQ'
		WHEN MC.country ='ERI' THEN 'ER'
		WHEN MC.country ='EST' THEN 'EE'
		WHEN MC.country ='SWZ' THEN 'SZ'
		WHEN MC.country ='ETH' THEN 'ET'
		WHEN MC.country ='FLK' THEN 'FK'
		WHEN MC.country ='FRO' THEN 'FO'
		WHEN MC.country ='FJI' THEN 'FJ'
		WHEN MC.country ='FIN' THEN 'FI'
		WHEN MC.country ='FRA' THEN 'FR'
		WHEN MC.country ='GUF' THEN 'GF'
		WHEN MC.country ='PYF' THEN 'PF'
		WHEN MC.country ='ATF' THEN 'TF'
		WHEN MC.country ='GAB' THEN 'GA'
		WHEN MC.country ='GMB' THEN 'GM'
		WHEN MC.country ='GEO' THEN 'GE'
		WHEN MC.country ='DEU' THEN 'DE'
		WHEN MC.country ='GHA' THEN 'GH'
		WHEN MC.country ='GIB' THEN 'GI'
		WHEN MC.country ='GRC' THEN 'GR'
		WHEN MC.country ='GRL' THEN 'GL'
		WHEN MC.country ='GRD' THEN 'GD'
		WHEN MC.country ='GLP' THEN 'GP'
		WHEN MC.country ='GUM' THEN 'GU'
		WHEN MC.country ='GTM' THEN 'GT'
		WHEN MC.country ='GGY' THEN 'GG'
		WHEN MC.country ='GIN' THEN 'GN'
		WHEN MC.country ='GNB' THEN 'GW'
		WHEN MC.country ='GUY' THEN 'GY'
		WHEN MC.country ='HTI' THEN 'HT'
		WHEN MC.country ='HMD' THEN 'HM'
		WHEN MC.country ='VAT' THEN 'VA'
		WHEN MC.country ='HND' THEN 'HN'
		WHEN MC.country ='HKG' THEN 'HK'
		WHEN MC.country ='HUN' THEN 'HU'
		WHEN MC.country ='ISL' THEN 'IS'
		WHEN MC.country ='IND' THEN 'IN'
		WHEN MC.country ='IDN' THEN 'ID'
		WHEN MC.country ='IRN' THEN 'IR'
		WHEN MC.country ='IRQ' THEN 'IQ'
		WHEN MC.country ='IRL' THEN 'IE'
		WHEN MC.country ='IMN' THEN 'IM'
		WHEN MC.country ='ISR' THEN 'IL'
		WHEN MC.country ='ITA' THEN 'IT'
		WHEN MC.country ='JAM' THEN 'JM'
		WHEN MC.country ='JPN' THEN 'JP'
		WHEN MC.country ='JEY' THEN 'JE'
		WHEN MC.country ='JOR' THEN 'JO'
		WHEN MC.country ='KAZ' THEN 'KZ'
		WHEN MC.country ='KEN' THEN 'KE'
		WHEN MC.country ='KIR' THEN 'KI'
		WHEN MC.country ='PRK' THEN 'KP'
		WHEN MC.country ='KOR' THEN 'KR'
		WHEN MC.country ='KWT' THEN 'KW'
		WHEN MC.country ='KGZ' THEN 'KG'
		WHEN MC.country ='LAO' THEN 'LA'
		WHEN MC.country ='LVA' THEN 'LV'
		WHEN MC.country ='LBN' THEN 'LB'
		WHEN MC.country ='LSO' THEN 'LS'
		WHEN MC.country ='LBR' THEN 'LR'
		WHEN MC.country ='LBY' THEN 'LY'
		WHEN MC.country ='LIE' THEN 'LI'
		WHEN MC.country ='LTU' THEN 'LT'
		WHEN MC.country ='LUX' THEN 'LU'
		WHEN MC.country ='MAC' THEN 'MO'
		WHEN MC.country ='MDG' THEN 'MG'
		WHEN MC.country ='MWI' THEN 'MW'
		WHEN MC.country ='MYS' THEN 'MY'
		WHEN MC.country ='MDV' THEN 'MV'
		WHEN MC.country ='MLI' THEN 'ML'
		WHEN MC.country ='MLT' THEN 'MT'
		WHEN MC.country ='MHL' THEN 'MH'
		WHEN MC.country ='MTQ' THEN 'MQ'
		WHEN MC.country ='MRT' THEN 'MR'
		WHEN MC.country ='MUS' THEN 'MU'
		WHEN MC.country ='MYT' THEN 'YT'
		WHEN MC.country ='MEX' THEN 'MX'
		WHEN MC.country ='FSM' THEN 'FM'
		WHEN MC.country ='MDA' THEN 'MD'
		WHEN MC.country ='MCO' THEN 'MC'
		WHEN MC.country ='MNG' THEN 'MN'
		WHEN MC.country ='MNE' THEN 'ME'
		WHEN MC.country ='MSR' THEN 'MS'
		WHEN MC.country ='MAR' THEN 'MA'
		WHEN MC.country ='MOZ' THEN 'MZ'
		WHEN MC.country ='MMR' THEN 'MM'
		WHEN MC.country ='NAM' THEN 'NA'
		WHEN MC.country ='NRU' THEN 'NR'
		WHEN MC.country ='NPL' THEN 'NP'
		WHEN MC.country ='NLD' THEN 'NL'
		WHEN MC.country ='NCL' THEN 'NC'
		WHEN MC.country ='NZL' THEN 'NZ'
		WHEN MC.country ='NIC' THEN 'NI'
		WHEN MC.country ='NER' THEN 'NE'
		WHEN MC.country ='NGA' THEN 'NG'
		WHEN MC.country ='NIU' THEN 'NU'
		WHEN MC.country ='NFK' THEN 'NF'
		WHEN MC.country ='MNP' THEN 'MP'
		WHEN MC.country ='NOR' THEN 'NO'
		WHEN MC.country ='OMN' THEN 'OM'
		WHEN MC.country ='PAK' THEN 'PK'
		WHEN MC.country ='PLW' THEN 'PW'
		WHEN MC.country ='PSE' THEN 'PS'
		WHEN MC.country ='PAN' THEN 'PA'
		WHEN MC.country ='PNG' THEN 'PG'
		WHEN MC.country ='PRY' THEN 'PY'
		WHEN MC.country ='PER' THEN 'PE'
		WHEN MC.country ='PHL' THEN 'PH'
		WHEN MC.country ='PCN' THEN 'PN'
		WHEN MC.country ='POL' THEN 'WA' -- Polske oznaczamy jako W2 -wewnętrzne - wytyczne NBP
		WHEN MC.country ='PRT' THEN 'PT'
		WHEN MC.country ='PRI' THEN 'US' --  Puerto Rico zaliczamy do US - wytyczne NBP
		WHEN MC.country ='QAT' THEN 'QA'
		WHEN MC.country ='MKD' THEN 'MK'
		WHEN MC.country ='ROU' THEN 'RO'
		WHEN MC.country ='RUS' THEN 'RU'
		WHEN MC.country ='RWA' THEN 'RW'
		WHEN MC.country ='REU' THEN 'RE'
		WHEN MC.country ='BLM' THEN 'BL'
		WHEN MC.country ='SHN' THEN 'SH'
		WHEN MC.country ='KNA' THEN 'KN'
		WHEN MC.country ='LCA' THEN 'LC'
		WHEN MC.country ='MAF' THEN 'MF'
		WHEN MC.country ='SPM' THEN 'PM'
		WHEN MC.country ='VCT' THEN 'VC'
		WHEN MC.country ='WSM' THEN 'WS'
		WHEN MC.country ='SMR' THEN 'SM'
		WHEN MC.country ='STP' THEN 'ST'
		WHEN MC.country ='SAU' THEN 'SA'
		WHEN MC.country ='SEN' THEN 'SN'
		WHEN MC.country ='SRB' THEN 'RS'
		WHEN MC.country ='SYC' THEN 'SC'
		WHEN MC.country ='SLE' THEN 'SL'
		WHEN MC.country ='SGP' THEN 'SG'
		WHEN MC.country ='SXM' THEN 'SX'
		WHEN MC.country ='SVK' THEN 'SK'
		WHEN MC.country ='SVN' THEN 'SI'
		WHEN MC.country ='SLB' THEN 'SB'
		WHEN MC.country ='SOM' THEN 'SO'
		WHEN MC.country ='ZAF' THEN 'ZA'
		WHEN MC.country ='SGS' THEN 'GS'
		WHEN MC.country ='SSD' THEN 'SS'
		WHEN MC.country ='ESP' THEN 'ES'
		WHEN MC.country ='LKA' THEN 'LK'
		WHEN MC.country ='SDN' THEN 'SD'
		WHEN MC.country ='SUR' THEN 'SR'
		WHEN MC.country ='SJM' THEN 'SJ'
		WHEN MC.country ='SWE' THEN 'SE'
		WHEN MC.country ='CHE' THEN 'CH'
		WHEN MC.country ='SYR' THEN 'SY'
		WHEN MC.country ='TWN' THEN 'TW'
		WHEN MC.country ='TJK' THEN 'TJ'
		WHEN MC.country ='TZA' THEN 'TZ'
		WHEN MC.country ='THA' THEN 'TH'
		WHEN MC.country ='TLS' THEN 'TL'
		WHEN MC.country ='TGO' THEN 'TG'
		WHEN MC.country ='TKL' THEN 'TK'
		WHEN MC.country ='TON' THEN 'TO'
		WHEN MC.country ='TTO' THEN 'TT'
		WHEN MC.country ='TUN' THEN 'TN'
		WHEN MC.country ='TUR' THEN 'TR'
		WHEN MC.country ='TKM' THEN 'TM'
		WHEN MC.country ='TCA' THEN 'TC'
		WHEN MC.country ='TUV' THEN 'TV'
		WHEN MC.country ='UGA' THEN 'UG'
		WHEN MC.country ='UKR' THEN 'UA'
		WHEN MC.country ='ARE' THEN 'AE'
		WHEN MC.country ='GBR' THEN 'GB'
		WHEN MC.country ='UMI' THEN 'UM'
		WHEN MC.country ='USA' THEN 'US'
		WHEN MC.country ='URY' THEN 'UY'
		WHEN MC.country ='UZB' THEN 'UZ'
		WHEN MC.country ='VUT' THEN 'VU'
		WHEN MC.country ='VEN' THEN 'VE'
		WHEN MC.country ='VNM' THEN 'VN'
		WHEN MC.country ='VGB' THEN 'VG'
		WHEN MC.country ='VIR' THEN 'VI'
		WHEN MC.country ='WLF' THEN 'WF'
		WHEN MC.country ='ESH' THEN 'EH'
		WHEN MC.country ='YEM' THEN 'YE'
		WHEN MC.country ='ZMB' THEN 'ZM'
		WHEN MC.country ='ZWE' THEN 'ZW'
		WHEN MC.country ='ALA' THEN 'AX'
		--- dodatkowe zamiany:
		WHEN MC.country = 'ROM' THEN 'RO' 
		WHEN MC.country = 'QZZ' THEN 'ZZ'   --- KOSOWO , ZZ jako pomoc w sortowaniu
		ELSE 'uwaga - coś nowego'
		END
		,CASE
		WHEN MC.country = 'QZZ' THEN 'Extra UE not allocated'   --- KOSOWO zaliczamy do D09 - Extra UE not allocated - wytyczne NBP, ZZ jako pomoc w sortowaniu
		WHEN MC.country = 'PRI' THEN 'United States of America'    -- Puerto Rico zaliczamy do US - wytyczne NBP
		WHEN MC.country = 'PL' THEN 'Poland'    -- Polske oznaczamy jako W2 -wewnętrzne - wytyczne NBP , WA jako pomoc w sortowaniu
		WHEN MC.country is null THEN 'uwaga - coś nowego'
		WHEN MC.country = 'ROM' THEN 'Romania'
		ELSE cc_name end
		,IIF(substring(te_pos_entry_mode, 1, 2) = '01', 'MOTO', 'inne')
--SELECT distinct country_code_NBP, country_name FROM #dane where karta = 'VISA' order by 1

IF OBJECT_ID('tempdb..#dane_2') IS NOT NULL DROP TABLE #dane_2
SELECT country_code_NBP, country_name, merchant_category_code, czy_moto, SUM(ilosc) as ilosc, SUM(wartosc_transakcji) as wartosc_transakcji
into #dane_2
FROM #dane 
group by country_code_NBP, country_name, merchant_category_code, czy_moto
order by 1
--select * from #dane_2


IF OBJECT_ID('tempdb..#mcc') IS NOT NULL DROP TABLE #mcc
CREATE TABLE #mcc (mcc varchar(4), opis varchar(256))
INSERT INTO #mcc VALUES ('0742','Usługi weterynaryjne')
INSERT INTO #mcc VALUES ('0743','Producenci wina')
INSERT INTO #mcc VALUES ('0744','Producenci szampana')
INSERT INTO #mcc VALUES ('0763','Spółdzielnie Rolnicze')
INSERT INTO #mcc VALUES ('0780','Usługi ogrodnicze, usługi architektury obrazu')
INSERT INTO #mcc VALUES ('1353','Dia (Hiszpania)-Hipermarkety')
INSERT INTO #mcc VALUES ('1406','H&M Moda (Hiszpania)-Sprzedawcy detaliczni')
INSERT INTO #mcc VALUES ('1520','Generalni Wykonawcy – obiekty mieszkalne i komercyjne')
INSERT INTO #mcc VALUES ('1711','Wykonawcy instalacji klimatyzacyjnej - sprzedaż i montaż, wykonawcy instalacji centralnego ogrzewania – sprzedaż, serwis, montaż')
INSERT INTO #mcc VALUES ('1731','Wykonawcy instalacji elektrycznej')
INSERT INTO #mcc VALUES ('1740','Wykonawcy izolacji, prace kamieniarskie, tynkarskie, dekarskie')
INSERT INTO #mcc VALUES ('1750','Wykonawcy – prace ciesielskie')
INSERT INTO #mcc VALUES ('1761','Wykonawcy – pokrycia dachowe, blacharstwo')
INSERT INTO #mcc VALUES ('1771','Wykonawcy – prace betonowe')
INSERT INTO #mcc VALUES ('1799','Wykonawcy – zawody specjalne, nigdzie indziej nie sklasyfikowane')
INSERT INTO #mcc VALUES ('2741','Różne wydawnictwa, drukarnie')
INSERT INTO #mcc VALUES ('2791','Skład tekstu, wytwarzanie matryc, usługi powiązane')
INSERT INTO #mcc VALUES ('2842','Czyszczenie, polerowanie oraz preparaty sanitarne')
INSERT INTO #mcc VALUES ('G300','Linie lotnicze (kody MCC od 3000 do 3350)')
INSERT INTO #mcc VALUES ('G335','Wypożyczalnie samochodów (kody MCC od 3351 do 3500)')
INSERT INTO #mcc VALUES ('G350','Hotele (kody MCC od 3501 do 3999)')
INSERT INTO #mcc VALUES ('4011','Railroads')
INSERT INTO #mcc VALUES ('4111','Lokalny/Podmiejski transport pasażerski – koleje, promy, lokalny transport wodny')
INSERT INTO #mcc VALUES ('4112','Koleje pasażerskie')
INSERT INTO #mcc VALUES ('4119','Pogotowie ratunkowe')
INSERT INTO #mcc VALUES ('4121','Taksówki i limuzyny')
INSERT INTO #mcc VALUES ('4131','Linie autobusowe, w tym czarterowane, autobusy turystyczne')
INSERT INTO #mcc VALUES ('4214','Usługi transortowe, transport towarowy, ciężarowy - przewozy lokalne i długodystansowe, firmy przewozowe i magazynowe oraz lokalni dostawcy')
INSERT INTO #mcc VALUES ('4215','Spedycja, usługi kurierskie - powietrzne lub naziemne')
INSERT INTO #mcc VALUES ('4225','Magazyny, hurtownie')
INSERT INTO #mcc VALUES ('4411','Linie wycieczkowe, parowce')
INSERT INTO #mcc VALUES ('4457','Czartery i dzierżawa jachtów')
INSERT INTO #mcc VALUES ('4468','Przystanie jachtowe, obsługa i zaopatrzenie jachtów')
INSERT INTO #mcc VALUES ('4511','Linie lotnicze, przewoźnicy lotniczy (nigdzie indziej nie wymienieni)')
INSERT INTO #mcc VALUES ('4582','Lotniska, terminale lotnicze, lądowiska')
INSERT INTO #mcc VALUES ('4722','Biura podróży i agencje podróży')
INSERT INTO #mcc VALUES ('4723','Przewoźnicy towarowi (do stosowania tylko w Niemczech)')
INSERT INTO #mcc VALUES ('4784','Opłaty drogowe i za przeprawy mostowe')
INSERT INTO #mcc VALUES ('4789','Usługi transportowe, nigdzie indziej nie sklasyfikowane')
INSERT INTO #mcc VALUES ('4812','Urządzenia telekomunikacyjne, w tym sprzedaż telefonów')
INSERT INTO #mcc VALUES ('4813','Połączenia telefoniczne przy użyciu centralnego numeru dostępu')
INSERT INTO #mcc VALUES ('4814','Usługi telekomunikacyjne w tym połączenia lokalne i międzystrefowe, połączenia z kart kredytowych, rozmowy telefoniczne wykonywane kartami telefonicznymi oraz usługi faksowe')
INSERT INTO #mcc VALUES ('4815','VisaPhone miesięczne opłaty telefoniczne')
INSERT INTO #mcc VALUES ('4816','Sieć komputerowa/usługi informacyjne')
INSERT INTO #mcc VALUES ('4821','Usługi telegraficzne')
INSERT INTO #mcc VALUES ('4829','Przekazy pieniężne')
INSERT INTO #mcc VALUES ('4899','Telewizja kablowa i inne usługi płatnej telewizji')
INSERT INTO #mcc VALUES ('4900','Media - elektryczne, gazowe, wodne i sanitarne')
INSERT INTO #mcc VALUES ('5013','Zaopatrzenie samochodowe, nowe części samochodowe')
INSERT INTO #mcc VALUES ('5021','Meble sklepowe i biurowe')
INSERT INTO #mcc VALUES ('5039','Materiały budowlane, nigdzie indziej nie sklasyfikowane')
INSERT INTO #mcc VALUES ('5044','Wyposażenie biurowe, fotograficzne, fotokopii i mikrofilmów')
INSERT INTO #mcc VALUES ('5045','Oprogramowanie, komputerowe urządzenia peryferyjne - gdzie indziej nie sklasyfikowane')
INSERT INTO #mcc VALUES ('5046','Wyposażenie handlowe, nigdzie indziej nie sklasyfikowane')
INSERT INTO #mcc VALUES ('5047','Sprzęt szpitalny i zaopatrzenie medyczne, stomatologiczne i okulistyczne')
INSERT INTO #mcc VALUES ('5051','Centra Serwisowe i biurowe')
INSERT INTO #mcc VALUES ('5065','Części i urządzenia elektryczne')
INSERT INTO #mcc VALUES ('5072','Sprzęt komputerowy i materiały eksploatacyjne')
INSERT INTO #mcc VALUES ('5074','Sprzęt sanitarny i grzejny')
INSERT INTO #mcc VALUES ('5085','Dostawy przemysłowe, nigdzie indziej niesklasyfikowane')
INSERT INTO #mcc VALUES ('5094','Szlachetne kamienie i metale, zegarki i biżuteria')
INSERT INTO #mcc VALUES ('5099','Dobra trwałe, nigdzie indziej niesklasyfikowana')
INSERT INTO #mcc VALUES ('5111','Artykuły papiernicze, biurowe, drukarnie i papier')
INSERT INTO #mcc VALUES ('5122','Środki odurzające, właściciele aptek')
INSERT INTO #mcc VALUES ('5131','Towary w kawałkach, galanteria i inne suche towary')
INSERT INTO #mcc VALUES ('5137','Ubiory męskie, damskie i dziecięce')
INSERT INTO #mcc VALUES ('5139','Obuwie')
INSERT INTO #mcc VALUES ('5169','Chemikalia i produkty związane z nimi, nigdzie indziej nie sklasyfikowane')
INSERT INTO #mcc VALUES ('5172','Ropa naftowa i produkty naftowe – paliwo')
INSERT INTO #mcc VALUES ('5192','Książki, czasopisma i prasa')
INSERT INTO #mcc VALUES ('5193','Artykuły kwiaciarskie, materiał szkółkarski i kwiaty')
INSERT INTO #mcc VALUES ('5198','Farby, lakiery i akcesoria')
INSERT INTO #mcc VALUES ('5199','Towary nietrwałe, nigdzie indziej nie sklasyfikowane')
INSERT INTO #mcc VALUES ('5200','Dostawy domowe ze sklepów')
INSERT INTO #mcc VALUES ('5211','Sklepy z drewnem i materiałami budowlanymi')
INSERT INTO #mcc VALUES ('5231','Sklepy ze szkłem, sklepy z farbami i tapetami')
INSERT INTO #mcc VALUES ('5251','Sklepy ze sprzętem')
INSERT INTO #mcc VALUES ('5261','Sklepy z zaopatrzeniem ogrodowym, trawniki, szkółki')
INSERT INTO #mcc VALUES ('5262','Targowiska (internetowe targowiska)')
INSERT INTO #mcc VALUES ('5271','Dealerzy mobilnych domków')
INSERT INTO #mcc VALUES ('5299','Warehouse Club Gas')
INSERT INTO #mcc VALUES ('5300','Hurtownie')
INSERT INTO #mcc VALUES ('5309','Sklepy wolnocłowe')
INSERT INTO #mcc VALUES ('5310','Sklepy dyskontowe')
INSERT INTO #mcc VALUES ('5311','Domy handlowe')
INSERT INTO #mcc VALUES ('5331','Sklepy z różnościami')
INSERT INTO #mcc VALUES ('5399','Różnorodne gadżety')
INSERT INTO #mcc VALUES ('5411','Sklepy spożywcze, supermarkety')
INSERT INTO #mcc VALUES ('5422','Zamrażarki i szafki mięsne')
INSERT INTO #mcc VALUES ('5441','Sklepy cukiernicze, cukiernie, sklepy z orzechami')
INSERT INTO #mcc VALUES ('5451','Sklepy z nabiałem, mleczarnie')
INSERT INTO #mcc VALUES ('5462','Piekarnie')
INSERT INTO #mcc VALUES ('5499','Sklepy spożywcze, sklepy pierwszej potrzeby i specjalne')
INSERT INTO #mcc VALUES ('5511','Dealerzy samochodów osobowych i ciężarowych (nowe i używane) – sprzedaż, serwis, naprawy, części, leasing')
INSERT INTO #mcc VALUES ('5521','Dealerzy samochodów i ciężarówek (tylko używane)')
INSERT INTO #mcc VALUES ('5531','Sklepy samochodowe')
INSERT INTO #mcc VALUES ('5532','Sklepy z oponami do samochodów')
INSERT INTO #mcc VALUES ('5533','Sklepy z częściami i akcesoriami do samochodów')
INSERT INTO #mcc VALUES ('5541','Stacje serwisowe (z lub bez usług dodatkowych)')
INSERT INTO #mcc VALUES ('5542','Samoobsługowe stacje benzynowe')
INSERT INTO #mcc VALUES ('5551','Dealerzy łodzi')
INSERT INTO #mcc VALUES ('5552','Ładowanie samochodów elektrycznych')
INSERT INTO #mcc VALUES ('5561','Dealerzy przyczep kampingowych, rekreacyjnych')
INSERT INTO #mcc VALUES ('5571','Dealerzy motocykli')
INSERT INTO #mcc VALUES ('5592','Dealerzy samochodów kempingowych')
INSERT INTO #mcc VALUES ('5598','Dealerzy pojazdów śniegowych')
INSERT INTO #mcc VALUES ('5599','Dealerzy urządzeń motoryzacyjnych, lotniczych i rolniczych, nigdzie indziej nie sklasyfikowani ')
INSERT INTO #mcc VALUES ('5611','Sklepy z akcesoriami i odzieżą męską i chłopięcą')
INSERT INTO #mcc VALUES ('5621','Sklepy z odzieżą damską')
INSERT INTO #mcc VALUES ('5631','Sklepy specjalistyczne z damskimi akcesoriami')
INSERT INTO #mcc VALUES ('5641','Odzież dla dzieci i niemowląt')
INSERT INTO #mcc VALUES ('5651','Sklepy odzieżowe rodzinne')
INSERT INTO #mcc VALUES ('5655','Stroje i akcesoria sportowe')
INSERT INTO #mcc VALUES ('5661','Sklepy obuwnicze')
INSERT INTO #mcc VALUES ('5681','Kuśnierze i sklepy z futrami')
INSERT INTO #mcc VALUES ('5691','Sklepy z odzieżą męską i damską')
INSERT INTO #mcc VALUES ('5697','Krawiec, szwaczka, cerowania')
INSERT INTO #mcc VALUES ('5698','Sklepy z perukami i czapkami')
INSERT INTO #mcc VALUES ('5699','Sklepy z innymi akcesoriami i odzieżą')
INSERT INTO #mcc VALUES ('5712','Meble, wyposażenie wnętrz, wyposażenie magazynów, z wyjątkiem urządzeń')
INSERT INTO #mcc VALUES ('5713','Sklepy z wykładzinami podłogowymi')
INSERT INTO #mcc VALUES ('5714','Sklepy z firanami, zasłonami do okien oraz sklepy tapicerskie')
INSERT INTO #mcc VALUES ('5718','Sklepy z kominkami, ekrany kominkowe i akcesoria')
INSERT INTO #mcc VALUES ('5719','Sklepy z akcesoriami meblowymi')
INSERT INTO #mcc VALUES ('5722','Sklepy z urządzeniami AGD')
INSERT INTO #mcc VALUES ('5732','Sprzedaż urządzeń elektronicznych')
INSERT INTO #mcc VALUES ('5733','Sklepy muzyczne, z instrumentami muzycznymi, papierem muzycznym')
INSERT INTO #mcc VALUES ('5734','Sklepy z oprogramowaniem komputerowym')
INSERT INTO #mcc VALUES ('5735','Sklepy muzyczne')
INSERT INTO #mcc VALUES ('5811','Firmy cateringowe')
INSERT INTO #mcc VALUES ('5812','Restauracje, gastronomia')
INSERT INTO #mcc VALUES ('5813','Pijalnie (napoje alkoholowe), bary, tawerny, kluby nocne i dyskoteki')
INSERT INTO #mcc VALUES ('5814','Fast foody')
INSERT INTO #mcc VALUES ('5815','Cyfrowe nośniki - książki, filmy, muzyka')
INSERT INTO #mcc VALUES ('5816','Cyfrowe nośniki - gry')
INSERT INTO #mcc VALUES ('5817','Cyfrowe nośniki - aplikacje (z wyłączeniem gier)')
INSERT INTO #mcc VALUES ('5818','Cyfrowe nośniki - Sprzedawcy towarów cyfrowych')
INSERT INTO #mcc VALUES ('5912','Drogerie i apteki')
INSERT INTO #mcc VALUES ('5921','Sklepy z piwem, winem, alkoholem')
INSERT INTO #mcc VALUES ('5931','Sklep z rzeczami używanymi, gadżetami')
INSERT INTO #mcc VALUES ('5932','Antykwariaty – sprzedaż, naprawa i usługi konserwatorskie')
INSERT INTO #mcc VALUES ('5933','Lombardy')
INSERT INTO #mcc VALUES ('5935','Rozbiórki')
INSERT INTO #mcc VALUES ('5937','Reprodukcje antyków')
INSERT INTO #mcc VALUES ('5940','Sklepy rowerowe – sprzedaż i serwis')
INSERT INTO #mcc VALUES ('5941','Sprzęt sportowy')
INSERT INTO #mcc VALUES ('5942','Księgarnie')
INSERT INTO #mcc VALUES ('5943','Sklepy papiernicze, artykułów biurowych i szkolnych')
INSERT INTO #mcc VALUES ('5944','Sklepy z zegarkami, biżuterią i srebrem – Jubilerzy')
INSERT INTO #mcc VALUES ('5945','Sklepy z zabawkami, grami')
INSERT INTO #mcc VALUES ('5946','Sklepy z aparatami fotograficznymi oraz osprzętem')
INSERT INTO #mcc VALUES ('5947','Sklepy z prezentami, gadżetami oraz sklepy z pamiątkami')
INSERT INTO #mcc VALUES ('5948','Sklepy ze skórą')
INSERT INTO #mcc VALUES ('5949','Sklepy z artykułami do szycia, igły, tkaniny')
INSERT INTO #mcc VALUES ('5950','Sklepy ze szkłem / kryształami')
INSERT INTO #mcc VALUES ('5960','Marketing bezpośredni – usługi ubezpieczenia')
INSERT INTO #mcc VALUES ('5961','Domy sprzedaży wysyłkowej włącznie z zamówieniami z katalogów')
INSERT INTO #mcc VALUES ('5962','Telemarketing – usługi biur podróży')
INSERT INTO #mcc VALUES ('5963','Sprzedaż bezpośrednia (drzwi w drzwi)')
INSERT INTO #mcc VALUES ('5964','Marketing bezpośredni – Katalogi sprzedawcy')
INSERT INTO #mcc VALUES ('5965','Marketing bezpośredni – Katalogi i wykazy sprzedawcy detalicznego')
INSERT INTO #mcc VALUES ('5966','Marketing bezpośredni – telemarketing')
INSERT INTO #mcc VALUES ('5967','Marketing bezpośredni – TeleSerwis')
INSERT INTO #mcc VALUES ('5968','Marketing bezpośredni – Subskrypcje')
INSERT INTO #mcc VALUES ('5969','Marketing bezpośredni – nigdzie indziej nie sklasyfikowane')
INSERT INTO #mcc VALUES ('5970','Sklepy z artykułami artystycznymi, rękodziełem')
INSERT INTO #mcc VALUES ('5971','Marszandzi i galerie sztuki')
INSERT INTO #mcc VALUES ('5972','Sklepy z pieczątkami i pieniędzmi – akcesoria filatelistyczne i numizmatyczne')
INSERT INTO #mcc VALUES ('5973','Dewocjonalia')
INSERT INTO #mcc VALUES ('5974','Sklep z pieczątkami')
INSERT INTO #mcc VALUES ('5975','Sklepy z aparatami słuchowymi – sprzedaż, serwis')
INSERT INTO #mcc VALUES ('5976','Sprzęt ortopedyczny – urządzenia protetyczne')
INSERT INTO #mcc VALUES ('5977','Sklepy kosmetyczne – drogerie')
INSERT INTO #mcc VALUES ('5978','Sklepy z maszynami do pisania – sprzedaż, wynajem, serwis')
INSERT INTO #mcc VALUES ('5983','Stacje benzynowe – olej opałowy, drewno, węgiel, benzyna')
INSERT INTO #mcc VALUES ('5992','Kwiaciarnie')
INSERT INTO #mcc VALUES ('5993','Sklepy z cygarami')
INSERT INTO #mcc VALUES ('5994','Kolportarz gazet')
INSERT INTO #mcc VALUES ('5995','Sklepy zoologiczne, pokarm dla zwierząt domowych, akcesoria')
INSERT INTO #mcc VALUES ('5996','Baseny – sprzedaż, serwis i materiały eksploatacyjne')
INSERT INTO #mcc VALUES ('5997','Sklepy z golarkami elektrycznymi – sprzedaż i serwis')
INSERT INTO #mcc VALUES ('5998','Sklepy z namiotami')
INSERT INTO #mcc VALUES ('5999','Sklepy z różnościami')
INSERT INTO #mcc VALUES ('6010','Instytucje finansowe - ręczna wypłata środków pieniężnych')
INSERT INTO #mcc VALUES ('6011','Instytucje finansowe automatyczna wypłata środków pieniężnych')
INSERT INTO #mcc VALUES ('6012','Instytucje finansowe – towary i usługi')
INSERT INTO #mcc VALUES ('6050','Quasi Cash')
INSERT INTO #mcc VALUES ('6051','Instytucje niefinansowe – waluty obce, przekazy pieniężne (nie przelewy) i czeki podróżne')
INSERT INTO #mcc VALUES ('6211','Brokerzy/dealerzy usług ochrony')
INSERT INTO #mcc VALUES ('6236','Aero Servicio Carabobo')
INSERT INTO #mcc VALUES ('6300','Sprzedaż ubezpieczeń')
INSERT INTO #mcc VALUES ('6381','Składki ubezpieczeniowe')
INSERT INTO #mcc VALUES ('6399','Ubezpieczenia, nigdzie indziej nie sklasyfikowane')
INSERT INTO #mcc VALUES ('6513','Agenci i zarządcy nieruchomości')
INSERT INTO #mcc VALUES ('6529','Remote Stored Value Load — instytucja finansowa')
INSERT INTO #mcc VALUES ('6530','Remove Stored Value Load — Merchant')
INSERT INTO #mcc VALUES ('6532','Transakcja płatnicza — instytucja finansowa klienta')
INSERT INTO #mcc VALUES ('6533','Transakcja płatnicza — sprzedawca')
INSERT INTO #mcc VALUES ('6535','Value Purchase–Member Financial Institution')
INSERT INTO #mcc VALUES ('6536','MoneySend wewnątrz kraju')
INSERT INTO #mcc VALUES ('6537','MoneySend za granicą')
INSERT INTO #mcc VALUES ('6538','MoneySend finansowanie')
INSERT INTO #mcc VALUES ('6539','Funding Transaction (Excluding MoneySend)')
INSERT INTO #mcc VALUES ('6540','Instytucje niefinansowe – zakup i doładowanie kart przedpłaconych')
INSERT INTO #mcc VALUES ('6611','Overpayments')
INSERT INTO #mcc VALUES ('6760','Savings Bonds')
INSERT INTO #mcc VALUES ('7011','Noclegi – Hotele, motele, usługi centralnej rezerwacji (nigdzie indziej nie sklasyfikowane)')
INSERT INTO #mcc VALUES ('7012','Współwłasność')
INSERT INTO #mcc VALUES ('7032','Obozy sportowe i rekreacyjne')
INSERT INTO #mcc VALUES ('7033','Parki naczep, przyczep oraz kampingów')
INSERT INTO #mcc VALUES ('7210','Usługi czyszczenia odzieży, pralnie')
INSERT INTO #mcc VALUES ('7211','Usługi pralni – Rodzina i handlowe')
INSERT INTO #mcc VALUES ('7216','Pralnie chemiczne')
INSERT INTO #mcc VALUES ('7217','Czyszczenie dywanów i tapicerki')
INSERT INTO #mcc VALUES ('7221','Studia fotograficzne')
INSERT INTO #mcc VALUES ('7230','Fryzjerzy')
INSERT INTO #mcc VALUES ('7251','Czyszczenie i reparacja butów i kapeluszy')
INSERT INTO #mcc VALUES ('7261','Krematoria oraz usługi pogrzebowe')
INSERT INTO #mcc VALUES ('7273','Usługi ogłoszeniowe, randki')
INSERT INTO #mcc VALUES ('7276','Usługi podatkowe')
INSERT INTO #mcc VALUES ('7277','Poradnie – długi, małżeństwo')
INSERT INTO #mcc VALUES ('7278','Usługi zakupów')
INSERT INTO #mcc VALUES ('7280','Hospital Patient-Personal Funds Withdrawal')
INSERT INTO #mcc VALUES ('7295','Opieka nad dziećmi')
INSERT INTO #mcc VALUES ('7296','Wynajem odzieży – kostiumy, odzież wizytowa, mundury')
INSERT INTO #mcc VALUES ('7297','Salony masażu')
INSERT INTO #mcc VALUES ('7298','Zdrowie i Uroda – sklepy')
INSERT INTO #mcc VALUES ('7299','Zawody różne (nigdzie indziej nie klasyfikowane)')
INSERT INTO #mcc VALUES ('7311','Usługi reklamowe')
INSERT INTO #mcc VALUES ('7321','Agencje raportowania zdolności kredytowej klentów')
INSERT INTO #mcc VALUES ('7322','Agencje windykacyjne')
INSERT INTO #mcc VALUES ('7332','Usługi fotokopiowania i wykonywania odbitek')
INSERT INTO #mcc VALUES ('7333','Fotografia i grafika')
INSERT INTO #mcc VALUES ('7338','Usługi kopiowania, reprodukcji i wykonywania odbitek')
INSERT INTO #mcc VALUES ('7339','Usługi stenograficzne')
INSERT INTO #mcc VALUES ('7342','Usługi dezynfekcyjne')
INSERT INTO #mcc VALUES ('7349','Usługi czyszczenia, konserwacji i sprzątania')
INSERT INTO #mcc VALUES ('7361','Agencje zatrudnienia')
INSERT INTO #mcc VALUES ('7372','Programowanie komputerowe, zintegrowane systemy projektowania i usługi przetwarzania danych')
INSERT INTO #mcc VALUES ('7375','Usługi wyszukiwania informacji')
INSERT INTO #mcc VALUES ('7379','Usługi konserwacji i naprawy komputerów nigdzie indziej niesklasyfikowane')
INSERT INTO #mcc VALUES ('7392','Usługi zarządzania, doradztwa i PR')
INSERT INTO #mcc VALUES ('7393','Usługi ochrony – w tym przy użyciu samochodów pancernych i psów obronnych')
INSERT INTO #mcc VALUES ('7394','Wypożyczalnie sprzętu, narzędzi, mebli i AGD')
INSERT INTO #mcc VALUES ('7395','Laboratoria obróbki fotograficznej')
INSERT INTO #mcc VALUES ('7399','Usługi dla firm, nigdzie indziej niesklasyfikowane')
INSERT INTO #mcc VALUES ('7511','Postój ciężarówek')
INSERT INTO #mcc VALUES ('7512','Wypożyczalnia samochodów (niewymienione poniżej)')
INSERT INTO #mcc VALUES ('7513','Wynajem ciężarówek')
INSERT INTO #mcc VALUES ('7519','Wynajem samochodów kempingowych i rekreacyjnych')
INSERT INTO #mcc VALUES ('7523','Parkingi samochodowe i garaże')
INSERT INTO #mcc VALUES ('7524','Express Payment Service Merchants–Parking Lots and Garages')
INSERT INTO #mcc VALUES ('7531','Sklepy motoryzacyjne – blacharstwo')
INSERT INTO #mcc VALUES ('7534','Stacje obsługi – bieżnikowanie opon')
INSERT INTO #mcc VALUES ('7535','Sklepy motoryzacyjne – lakiernictwo')
INSERT INTO #mcc VALUES ('7538','Salony serwisowe samochodowe /Auto Serwis')
INSERT INTO #mcc VALUES ('7539','Serwisy samochodowe (Hiszpania) - inne kategorie sprzedawców')
INSERT INTO #mcc VALUES ('7542','Myjnie samochodowe')
INSERT INTO #mcc VALUES ('7549','Usługi holowania')
INSERT INTO #mcc VALUES ('7622','Warsztaty naprawy radia')
INSERT INTO #mcc VALUES ('7623','Stacje obsługi – klimatyzacja i chłodnictwo')
INSERT INTO #mcc VALUES ('7629','Naprawa urządzeń elektrycznych')
INSERT INTO #mcc VALUES ('7631','Naprawa zegarków, biżuterii')
INSERT INTO #mcc VALUES ('7641','Meble, renowacja mebli, naprawa mebli')
INSERT INTO #mcc VALUES ('7692','Spawalnictwo')
INSERT INTO #mcc VALUES ('7699','Naprawa rzeczy różnych')
INSERT INTO #mcc VALUES ('7800','Loterie nie należące do rządu (tylko region USA)')
INSERT INTO #mcc VALUES ('7801','Licencja rządowa - kasyna online ( gry hazardowe online) (tylko region USA)')
INSERT INTO #mcc VALUES ('7802','Licencja rządowa - wyścigi konne/psów (tylko region USA)')
INSERT INTO #mcc VALUES ('7829','Produkcja filmów i produkcji taśmy video – dystrybucja')
INSERT INTO #mcc VALUES ('7832','Kina')
INSERT INTO #mcc VALUES ('7833','Express Payment Service — Motion Picture Theater')
INSERT INTO #mcc VALUES ('7841','Wypożyczalnie wideo')
INSERT INTO #mcc VALUES ('7911','Studia i szkoły tańca')
INSERT INTO #mcc VALUES ('7922','Producenci teatralni (z wyjątkiem filmów), agencje biletów')
INSERT INTO #mcc VALUES ('7929','Zespoły, orkiestry i artyści różni (nigdzie indziej nie sklasyfikowane)')
INSERT INTO #mcc VALUES ('7932','Bilard')
INSERT INTO #mcc VALUES ('7933','Kręgielnie')
INSERT INTO #mcc VALUES ('7941','Sporty, zawodowe kluby sportowe i promotorzy sportowi')
INSERT INTO #mcc VALUES ('7991','Atrakcje turystyczne')
INSERT INTO #mcc VALUES ('7992','Pola golfowe – publiczne')
INSERT INTO #mcc VALUES ('7993','Rozrywkowe gry wideo')
INSERT INTO #mcc VALUES ('7994','Gry wideo')
INSERT INTO #mcc VALUES ('7995','Zakłady (w tym kupony loteryjne, żetony do gier kasynowych, zakłady)')
INSERT INTO #mcc VALUES ('7996','Parki rozrywki, karnawały, cyrki, wróżki')
INSERT INTO #mcc VALUES ('7997','Kluby członkostwa (sport, rekreacja, atletyka), kluby krajowe i prywatne pola golfowe')
INSERT INTO #mcc VALUES ('7998','Akwaria, delfinaria')
INSERT INTO #mcc VALUES ('7999','Usługi rekreacyjne (nigdzie indziej nie sklasyfikowane)')
INSERT INTO #mcc VALUES ('8011','Lekarze (nigdzie indziej nie sklasyfikowane)')
INSERT INTO #mcc VALUES ('8021','Lekarze dentyści i ortodonci')
INSERT INTO #mcc VALUES ('8031','Osteopaci')
INSERT INTO #mcc VALUES ('8041','Kręgarze')
INSERT INTO #mcc VALUES ('8042','Optycy i okuliści')
INSERT INTO #mcc VALUES ('8043','Optycy, sklepy z okularami i akcesoriami optycznymi')
INSERT INTO #mcc VALUES ('8044','Optycy, sklepy z okularami i akcesoriami optycznymi')
INSERT INTO #mcc VALUES ('8049','Podiatra i podolog')
INSERT INTO #mcc VALUES ('8050','Pielęgniarstwo i opieka osobista')
INSERT INTO #mcc VALUES ('8062','Szpitale')
INSERT INTO #mcc VALUES ('8071','Laboratoria medyczne i stomatologiczne')
INSERT INTO #mcc VALUES ('8099','Usługi medyczne i praktyki lekarskie (nigdzie indziej nie sklasyfikowane)')
INSERT INTO #mcc VALUES ('8111','Usługi prawnicze, adwokackie')
INSERT INTO #mcc VALUES ('8211','Szkoły podstawowe i gimnazja')
INSERT INTO #mcc VALUES ('8220','Uczelnie, uniwersytety i szkoły doskonalenia zawodowego')
INSERT INTO #mcc VALUES ('8241','Szkoły korespondencyjne')
INSERT INTO #mcc VALUES ('8244','Szkoły biznesu')
INSERT INTO #mcc VALUES ('8249','Szkoły policealne i szkoły zawodowe')
INSERT INTO #mcc VALUES ('8299','Szkoły i usługi oświatowe (nigdzie indziej nie sklasyfikowane)')
INSERT INTO #mcc VALUES ('8351','Usługi opieki nad dziećmi')
INSERT INTO #mcc VALUES ('8398','Organizacje charytatywne i społeczne')
INSERT INTO #mcc VALUES ('8641','Stowarzyszeń społecznych')
INSERT INTO #mcc VALUES ('8651','Organizacje polityczne')
INSERT INTO #mcc VALUES ('8661','Organizacje religijne')
INSERT INTO #mcc VALUES ('8675','Stowarzyszenia samochodowe')
INSERT INTO #mcc VALUES ('8699','Inne organizacje członkowskie (nigdzie indziej nie sklasyfikowane)')
INSERT INTO #mcc VALUES ('8734','Laboratoria badawczych (niemedyczne)')
INSERT INTO #mcc VALUES ('8911','Usługi architektoniczno – inżynieryjne i pomiarowe')
INSERT INTO #mcc VALUES ('8931','Usługi księgowości, audyty księgowe')
INSERT INTO #mcc VALUES ('8999','Wolnych zawodów (nigdzie indziej nie zdefiniowane)')
INSERT INTO #mcc VALUES ('9034','I-Purchasing Pilot')
INSERT INTO #mcc VALUES ('9211','Kosztów sądowe, w tym wsparcie alimentacyjne dziecka')
INSERT INTO #mcc VALUES ('9222','Grzywny')
INSERT INTO #mcc VALUES ('9223','Poręczenia, obligacje')
INSERT INTO #mcc VALUES ('9311','Podatki')
INSERT INTO #mcc VALUES ('9399','Usługi rządowych (nigdzie indziej nie sklasyfikowane)')
INSERT INTO #mcc VALUES ('9402','Usługi pocztowe – rząd tylko')
INSERT INTO #mcc VALUES ('9405','Transakcje rządowe')
INSERT INTO #mcc VALUES ('9406','Loterie należące do rządu (region poza USA)')
INSERT INTO #mcc VALUES ('9700','Zautomatyzowana usługa referencyjna (jedynie Visa)')
INSERT INTO #mcc VALUES ('9701','Usługa Visa')
INSERT INTO #mcc VALUES ('9702','Usługi awaryjne GCAS (jedynie Visa)')
INSERT INTO #mcc VALUES ('9751','UK Supermarkets, Electronic Hot File')
INSERT INTO #mcc VALUES ('9752','UK Petrol Stations, Electronic Hot File')
INSERT INTO #mcc VALUES ('9754','Hazard - konie, wyścigi psów, loterie państwowe')
INSERT INTO #mcc VALUES ('9950','Zakup przedsiębiorstwa (jedynie Visa)')
INSERT INTO #mcc VALUES ('R999','Tymczasowy niezdefiniowany kod MCC')
--select * from #mcc where mcc

IF OBJECT_ID('tempdb..#geo6') IS NOT NULL DROP TABLE #geo6
CREATE TABLE #geo6 (code varchar(2), name varchar(256))
INSERT INTO #geo6 VALUES ('AD', 'Andorra')
INSERT INTO #geo6 VALUES ('AE','United Arab Emirates (the)')
INSERT INTO #geo6 VALUES ('AF','Afghanistan')
INSERT INTO #geo6 VALUES ('AG','Antigua and Barbuda')
INSERT INTO #geo6 VALUES ('AI','Anguilla')
INSERT INTO #geo6 VALUES ('AL','Albania')
INSERT INTO #geo6 VALUES ('AM','Armenia')
INSERT INTO #geo6 VALUES ('AO','Angola')
INSERT INTO #geo6 VALUES ('AQ','Antarctica')
INSERT INTO #geo6 VALUES ('AR','Argentina')
INSERT INTO #geo6 VALUES ('AS','American Samoa')
INSERT INTO #geo6 VALUES ('AT','Austria')
INSERT INTO #geo6 VALUES ('AU','Australia')
INSERT INTO #geo6 VALUES ('AW','Aruba')
INSERT INTO #geo6 VALUES ('AZ','Azerbaijan')
INSERT INTO #geo6 VALUES ('BA','Bosnia and Herzegovina')
INSERT INTO #geo6 VALUES ('BB','Barbados')
INSERT INTO #geo6 VALUES ('BD','Bangladesh')
INSERT INTO #geo6 VALUES ('BE','Belgium')
INSERT INTO #geo6 VALUES ('BF','Burkina Faso')
INSERT INTO #geo6 VALUES ('BG','Bulgaria')
INSERT INTO #geo6 VALUES ('BH','Bahrain')
INSERT INTO #geo6 VALUES ('BI','Burundi')
INSERT INTO #geo6 VALUES ('BJ','Benin')
INSERT INTO #geo6 VALUES ('BM','Bermuda')
INSERT INTO #geo6 VALUES ('BN','Brunei Darussalam')
INSERT INTO #geo6 VALUES ('BO','Bolivia (Plurinational State of)')
INSERT INTO #geo6 VALUES ('BQ','Bonaire, Sint Eustatius and Saba')
INSERT INTO #geo6 VALUES ('BR','Brazil')
INSERT INTO #geo6 VALUES ('BS','Bahamas (the)')
INSERT INTO #geo6 VALUES ('BT','Bhutan')
INSERT INTO #geo6 VALUES ('BV','Bouvet Island')
INSERT INTO #geo6 VALUES ('BW','Botswana')
INSERT INTO #geo6 VALUES ('BY','Belarus')
INSERT INTO #geo6 VALUES ('BZ','Belize')
INSERT INTO #geo6 VALUES ('CA','Canada')
INSERT INTO #geo6 VALUES ('CC','Cocos (Keeling) Islands (the)')
INSERT INTO #geo6 VALUES ('CD','Congo (the Democratic Republic of the)')
INSERT INTO #geo6 VALUES ('CF','Central African Republic (the)')
INSERT INTO #geo6 VALUES ('CG','Congo (the)')
INSERT INTO #geo6 VALUES ('CH','Switzerland')
INSERT INTO #geo6 VALUES ('CI','Côte dIvoire')
INSERT INTO #geo6 VALUES ('CK','Cook Islands (the)')
INSERT INTO #geo6 VALUES ('CL','Chile')
INSERT INTO #geo6 VALUES ('CM','Cameroon')
INSERT INTO #geo6 VALUES ('CN','China')
INSERT INTO #geo6 VALUES ('CO','Colombia')
INSERT INTO #geo6 VALUES ('CR','Costa Rica')
INSERT INTO #geo6 VALUES ('CU','Cuba')
INSERT INTO #geo6 VALUES ('CV','Cabo Verde')
INSERT INTO #geo6 VALUES ('CW','Curaçao')
INSERT INTO #geo6 VALUES ('CX','Christmas Island')
INSERT INTO #geo6 VALUES ('CY','Cyprus')
INSERT INTO #geo6 VALUES ('CZ','Czechia')
INSERT INTO #geo6 VALUES ('DE','Germany')
INSERT INTO #geo6 VALUES ('DJ','Djibouti')
INSERT INTO #geo6 VALUES ('DK','Denmark')
INSERT INTO #geo6 VALUES ('DM','Dominica')
INSERT INTO #geo6 VALUES ('DO','Dominican Republic (the)')
INSERT INTO #geo6 VALUES ('DZ','Algeria')
INSERT INTO #geo6 VALUES ('EC','Ecuador')
INSERT INTO #geo6 VALUES ('EE','Estonia')
INSERT INTO #geo6 VALUES ('EG','Egypt')
INSERT INTO #geo6 VALUES ('EH','Western Sahara*')
INSERT INTO #geo6 VALUES ('ER','Eritrea')
INSERT INTO #geo6 VALUES ('ES','Spain')
INSERT INTO #geo6 VALUES ('ET','Ethiopia')
INSERT INTO #geo6 VALUES ('FI','Finland')
INSERT INTO #geo6 VALUES ('FJ','Fiji')
INSERT INTO #geo6 VALUES ('FK','Falkland Islands (the) [Malvinas]')
INSERT INTO #geo6 VALUES ('FM','Micronesia (Federated States of)')
INSERT INTO #geo6 VALUES ('FO','Faroe Islands (the)')
INSERT INTO #geo6 VALUES ('FR','France')
INSERT INTO #geo6 VALUES ('GA','Gabon')
INSERT INTO #geo6 VALUES ('GB','United Kingdom of Great Britain and Northern Ireland (the)')
INSERT INTO #geo6 VALUES ('GD','Grenada')
INSERT INTO #geo6 VALUES ('GE','Georgia')
INSERT INTO #geo6 VALUES ('GG','Guernsey')
INSERT INTO #geo6 VALUES ('GH','Ghana')
INSERT INTO #geo6 VALUES ('GI','Gibraltar')
INSERT INTO #geo6 VALUES ('GL','Greenland')
INSERT INTO #geo6 VALUES ('GM','Gambia (the)')
INSERT INTO #geo6 VALUES ('GN','Guinea')
INSERT INTO #geo6 VALUES ('GQ','Equatorial Guinea')
INSERT INTO #geo6 VALUES ('GR','Greece')
INSERT INTO #geo6 VALUES ('GS','South Georgia and the South Sandwich Islands')
INSERT INTO #geo6 VALUES ('GT','Guatemala')
INSERT INTO #geo6 VALUES ('GU','Guam')
INSERT INTO #geo6 VALUES ('GW','Guinea-Bissau')
INSERT INTO #geo6 VALUES ('GY','Guyana')
INSERT INTO #geo6 VALUES ('HK','Hong Kong')
INSERT INTO #geo6 VALUES ('HM','Heard Island and McDonald Islands')
INSERT INTO #geo6 VALUES ('HN','Honduras')
INSERT INTO #geo6 VALUES ('HR','Croatia')
INSERT INTO #geo6 VALUES ('HT','Haiti')
INSERT INTO #geo6 VALUES ('HU','Hungary')
INSERT INTO #geo6 VALUES ('ID','Indonesia')
INSERT INTO #geo6 VALUES ('IE','Ireland')
INSERT INTO #geo6 VALUES ('IL','Israel')
INSERT INTO #geo6 VALUES ('IM','Isle of Man')
INSERT INTO #geo6 VALUES ('IN','India')
INSERT INTO #geo6 VALUES ('IO','British Indian Ocean Territory (the)')
INSERT INTO #geo6 VALUES ('IQ','Iraq')
INSERT INTO #geo6 VALUES ('IR','Iran (Islamic Republic of)')
INSERT INTO #geo6 VALUES ('IS','Iceland')
INSERT INTO #geo6 VALUES ('IT','Italy')
INSERT INTO #geo6 VALUES ('JE','Jersey')
INSERT INTO #geo6 VALUES ('JM','Jamaica')
INSERT INTO #geo6 VALUES ('JO','Jordan')
INSERT INTO #geo6 VALUES ('JP','Japan')
INSERT INTO #geo6 VALUES ('KE','Kenya')
INSERT INTO #geo6 VALUES ('KG','Kyrgyzstan')
INSERT INTO #geo6 VALUES ('KH','Cambodia')
INSERT INTO #geo6 VALUES ('KI','Kiribati')
INSERT INTO #geo6 VALUES ('KM','Comoros (the)')
INSERT INTO #geo6 VALUES ('KN','Saint Kitts and Nevis')
INSERT INTO #geo6 VALUES ('KP','Korea (the Democratic Peoples Republic of)')
INSERT INTO #geo6 VALUES ('KR','Korea (the Republic of)')
INSERT INTO #geo6 VALUES ('KW','Kuwait')
INSERT INTO #geo6 VALUES ('KY','Cayman Islands (the)')
INSERT INTO #geo6 VALUES ('KZ','Kazakhstan')
INSERT INTO #geo6 VALUES ('LA','Lao Peoples Democratic Republic (the)')
INSERT INTO #geo6 VALUES ('LB','Lebanon')
INSERT INTO #geo6 VALUES ('LC','Saint Lucia')
INSERT INTO #geo6 VALUES ('LI','Liechtenstein')
INSERT INTO #geo6 VALUES ('LK','Sri Lanka')
INSERT INTO #geo6 VALUES ('LR','Liberia')
INSERT INTO #geo6 VALUES ('LS','Lesotho')
INSERT INTO #geo6 VALUES ('LT','Lithuania')
INSERT INTO #geo6 VALUES ('LU','Luxembourg')
INSERT INTO #geo6 VALUES ('LV','Latvia')
INSERT INTO #geo6 VALUES ('LY','Libya')
INSERT INTO #geo6 VALUES ('MA','Morocco')
INSERT INTO #geo6 VALUES ('MD','Moldova (the Republic of)')
INSERT INTO #geo6 VALUES ('ME','Montenegro')
INSERT INTO #geo6 VALUES ('MG','Madagascar')
INSERT INTO #geo6 VALUES ('MH','Marshall Islands (the)')
INSERT INTO #geo6 VALUES ('MK','North Macedonia')
INSERT INTO #geo6 VALUES ('ML','Mali')
INSERT INTO #geo6 VALUES ('MM','Myanmar')
INSERT INTO #geo6 VALUES ('MN','Mongolia')
INSERT INTO #geo6 VALUES ('MO','Macao')
INSERT INTO #geo6 VALUES ('MP','Northern Mariana Islands (the)')
INSERT INTO #geo6 VALUES ('MR','Mauritania')
INSERT INTO #geo6 VALUES ('MS','Montserrat')
INSERT INTO #geo6 VALUES ('MT','Malta')
INSERT INTO #geo6 VALUES ('MU','Mauritius')
INSERT INTO #geo6 VALUES ('MV','Maldives')
INSERT INTO #geo6 VALUES ('MW','Malawi')
INSERT INTO #geo6 VALUES ('MX','Mexico')
INSERT INTO #geo6 VALUES ('MY','Malaysia')
INSERT INTO #geo6 VALUES ('MZ','Mozambique')
INSERT INTO #geo6 VALUES ('NA','Namibia')
INSERT INTO #geo6 VALUES ('NC','New Caledonia')
INSERT INTO #geo6 VALUES ('NE','Niger (the)')
INSERT INTO #geo6 VALUES ('NF','Norfolk Island')
INSERT INTO #geo6 VALUES ('NG','Nigeria')
INSERT INTO #geo6 VALUES ('NI','Nicaragua')
INSERT INTO #geo6 VALUES ('NL','Netherlands')
INSERT INTO #geo6 VALUES ('NO','Norway')
INSERT INTO #geo6 VALUES ('NP','Nepal')
INSERT INTO #geo6 VALUES ('NR','Nauru')
INSERT INTO #geo6 VALUES ('NU','Niue')
INSERT INTO #geo6 VALUES ('NZ','New Zealand')
INSERT INTO #geo6 VALUES ('OM','Oman')
INSERT INTO #geo6 VALUES ('PA','Panama')
INSERT INTO #geo6 VALUES ('PE','Peru')
INSERT INTO #geo6 VALUES ('PF','French Polynesia')
INSERT INTO #geo6 VALUES ('PG','Papua New Guinea')
INSERT INTO #geo6 VALUES ('PH','Philippines (the)')
INSERT INTO #geo6 VALUES ('PK','Pakistan')
--INSERT INTO #geo6 VALUES ('PL','Poland')
INSERT INTO #geo6 VALUES ('PN','Pitcairn')
INSERT INTO #geo6 VALUES ('PS','Palestine, State of')
INSERT INTO #geo6 VALUES ('PT','Portugal')
INSERT INTO #geo6 VALUES ('PW','Palau')
INSERT INTO #geo6 VALUES ('PY','Paraguay')
INSERT INTO #geo6 VALUES ('QA','Qatar')
INSERT INTO #geo6 VALUES ('RO','Romania')
INSERT INTO #geo6 VALUES ('RS','Serbia')
INSERT INTO #geo6 VALUES ('RU','Russian Federation (the)')
INSERT INTO #geo6 VALUES ('RW','Rwanda')
INSERT INTO #geo6 VALUES ('SA','Saudi Arabia')
INSERT INTO #geo6 VALUES ('SB','Solomon Islands')
INSERT INTO #geo6 VALUES ('SC','Seychelles')
INSERT INTO #geo6 VALUES ('SD','Sudan (the)')
INSERT INTO #geo6 VALUES ('SE','Sweden')
INSERT INTO #geo6 VALUES ('SG','Singapore')
INSERT INTO #geo6 VALUES ('SH','Saint Helena, Ascension and Tristan da Cunha')
INSERT INTO #geo6 VALUES ('SI','Slovenia')
INSERT INTO #geo6 VALUES ('SJ','Svalbard and Jan Mayen')
INSERT INTO #geo6 VALUES ('SK','Slovakia')
INSERT INTO #geo6 VALUES ('SL','Sierra Leone')
INSERT INTO #geo6 VALUES ('SM','San Marino')
INSERT INTO #geo6 VALUES ('SN','Senegal')
INSERT INTO #geo6 VALUES ('SO','Somalia')
INSERT INTO #geo6 VALUES ('SR','Suriname')
INSERT INTO #geo6 VALUES ('SS','South Sudan')
INSERT INTO #geo6 VALUES ('ST','Sao Tome and Principe')
INSERT INTO #geo6 VALUES ('SV','El Salvador')
INSERT INTO #geo6 VALUES ('SX','Sint Maarten (Dutch part)')
INSERT INTO #geo6 VALUES ('SY','Syrian Arab Republic (the)')
INSERT INTO #geo6 VALUES ('SZ','Eswatini')
INSERT INTO #geo6 VALUES ('TC','Turks and Caicos Islands (the)')
INSERT INTO #geo6 VALUES ('TD','Chad')
INSERT INTO #geo6 VALUES ('TF','French Southern Territories (the)')
INSERT INTO #geo6 VALUES ('TG','Togo')
INSERT INTO #geo6 VALUES ('TH','Thailand')
INSERT INTO #geo6 VALUES ('TJ','Tajikistan')
INSERT INTO #geo6 VALUES ('TK','Tokelau')
INSERT INTO #geo6 VALUES ('TL','Timor-Leste')
INSERT INTO #geo6 VALUES ('TM','Turkmenistan')
INSERT INTO #geo6 VALUES ('TN','Tunisia')
INSERT INTO #geo6 VALUES ('TO','Tonga')
INSERT INTO #geo6 VALUES ('TR','Turkey')
INSERT INTO #geo6 VALUES ('TT','Trinidad and Tobago')
INSERT INTO #geo6 VALUES ('TV','Tuvalu')
INSERT INTO #geo6 VALUES ('TW','Taiwan (Province of China)')
INSERT INTO #geo6 VALUES ('TZ','Tanzania, the United Republic of')
INSERT INTO #geo6 VALUES ('UA','Ukraine')
INSERT INTO #geo6 VALUES ('UG','Uganda')
INSERT INTO #geo6 VALUES ('UM','United States Minor Outlying Islands (the)')
INSERT INTO #geo6 VALUES ('US','United States of America (the)')
INSERT INTO #geo6 VALUES ('UY','Uruguay')
INSERT INTO #geo6 VALUES ('UZ','Uzbekistan')
INSERT INTO #geo6 VALUES ('VA','Holy See (the)')
INSERT INTO #geo6 VALUES ('VC','Saint Vincent and the Grenadines')
INSERT INTO #geo6 VALUES ('VE','Venezuela (Bolivarian Republic of)')
INSERT INTO #geo6 VALUES ('VG','Virgin Islands (British)')
INSERT INTO #geo6 VALUES ('VI','Virgin Islands (U.S.)')
INSERT INTO #geo6 VALUES ('VN','Viet Nam')
INSERT INTO #geo6 VALUES ('VU','Vanuatu')
INSERT INTO #geo6 VALUES ('WA','Domestic')    -- W2
INSERT INTO #geo6 VALUES ('WF','Wallis and Futuna')
INSERT INTO #geo6 VALUES ('WS','Samoa')
INSERT INTO #geo6 VALUES ('YE','Yemen')
INSERT INTO #geo6 VALUES ('ZA','South Africa')
INSERT INTO #geo6 VALUES ('ZM','Zambia')
INSERT INTO #geo6 VALUES ('ZW','Zimbabwe')
INSERT INTO #geo6 VALUES ('ZZ','Extra UE not allocated') -- D09
--SELECT * from #geo6

--select distinct code, country_code_NBP, country_name
--from #geo6
--left join #dane on code = #dane.country_code_NBP

--select distinct code, country_code_NBP, country_name
--from #dane 
--left join #geo6 on code = #dane.country_code_NBP

--select distinct merchant_category_code, mcc
--from #dane 
--left join #mcc on merchant_category_code = #mcc.mcc

--select distinct mcc, merchant_category_code
--from #mcc 
--left join #dane on merchant_category_code = #mcc.mcc

---split---

IF OBJECT_ID('tempdb..#start') IS NOT NULL DROP TABLE #start
SELECT *
into #start
FROM #geo6
cross join #mcc
SELECT * FROM #start
-- 80 065
