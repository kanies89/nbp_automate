--NBP - ST.06 Trans VISA i MC z podzia³em na Inne Kraje .sql
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED
USE paytel_olap

declare @dtb as smalldatetime  = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1, '19000101');
declare @dte as smalldatetime =  DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-0 , '19000101');
select @dtb,@dte

IF OBJECT_ID('tempdb..#transakcje') IS NOT NULL DROP TABLE #transakcje
--transakcje VISA
SELECT
'VISA'as 'karta'
,CASE
	WHEN  VT.country = 'ROM' THEN 'Romania'
	WHEN  VT.country in ('QZ', 'QZZ', 'SZ') THEN 'Extra UE not allocated' --- Kosowo i  Eswatini - brak na liœcie od nbp, wrzucone do extra not allocated - ale to nie jest ue - trzeba by skonsultowaæ z nbp   
	WHEN  VT.country = 'PR' THEN 'United States of America'
	ELSE cc_name end as CountryName
,CASE 
	WHEN VT.country = 'ROM' THEN 'RO'
	WHEN VT.country in ('QZ', 'QZZ', 'SZ') THEN 'D09' --- Kosowo i  Eswatini - brak na liœcie od nbp, wrzucone do extra not allocated - ale to nie jest ue - trzeba by skonsultowaæ z nbp
	WHEN VT.country = 'PR' THEN 'US' 
	ELSE VT.country end as CountryCode, 
	count(*) as 'ilosc', 
	sum(convert(money,abs((tr_amount))))/100 as 'wartoœæ transakcji',
	0 as 'ilosc_internet',
    0 as 'wartosc_internet',
	count(case when tr_cash_req > 0 then 1 END) as 'iloœæ transakcji CashBack',
	sum(convert(money,abs((tr_cash_req/100))))as 'Wartoœæ wyp³at CashBack'
,CASE 
	WHEN cc_name in (
	'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Greece', 
	'Spain', 'Netherlands', 'Ireland', 'Lithuania', 'Luxembourg', 'Latvia', 'Germany', 'Malta', 'Portugal', 'Romania', 'Slovakia', 
	'Slovenia', 'Sweden', 'Hungary', 'Italy', 'Norway', 'Liechtenstein', 'Iceland') THEN 'wyró¿nione'
	ELSE 'reszta œwiata' END 'podzia³ NBP'
into #transakcje
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
'MC' as 'karta'
,CASE
	WHEN MC.country = 'ROM' THEN 'Romania'
	WHEN MC.country in ('QZ', 'QZZ', 'SZ') THEN 'Extra UE not allocated'  --- Kosowo i  Eswatini - brak na liœcie od nbp, wrzucone do extra not allocated - ale to nie jest ue - trzeba by skonsultowaæ z nbp
	WHEN MC.country = 'PRI' THEN 'United States of America'
	ELSE cc_name end as CountryName
,CASE
-- przekszta³cenia kodow MC na standard VISA(NBP)
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
	WHEN MC.country ='SWZ' THEN 'D09'    --- Eswatini - brak na liœcie od nbp, wrzucone do extra not allocated - ale to nie jest ue - trzeba by skonsultowaæ z nbp
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
	WHEN MC.country = 'QZZ' THEN 'D09'   --- KOSOWO zaliczamy do extra ue not allocated
	WHEN MC.country = 'ZAR' THEN 'CD'
	ELSE 'uwaga - coœ nowego'
	END as 'CountryCode'
,COUNT(*) as 'iloœæ transakcji'
,SUM(convert(money,abs(tr_amount)))/100 as 'wartoœæ transakcji'
,0 as 'ilosc_internet'
,0 as 'wartosc_internet'
,COUNT(case when tr_cash_req > 0 then 1 END) as 'iloœæ transakcji CashBack'
,SUM(convert(money,abs(tr_cash_req/100)))as 'Wartoœæ wyp³at CashBack'
,CASE 
	WHEN MC.country IN ('AUT','BEL','BGR','HRV','CYP','CZE','DNK','EST','FIN','FRA','GRC','ESP','NLD','IRL','LTU',
	'LUX','LVA','DEU','MLT','PRT','ROM','SVK','SVN','SWE','HUN','ITA', 'ISL', 'LIE', 'NOR') THEN 'wyró¿nione'
	ELSE 'reszta œwiata' END 'podzia³ NBP'
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
ORDER BY 8 desc, 1, 2, 3 DESC

--select * from #transakcje where CountryCode = 'D09'

IF OBJECT_ID('tempdb..#geo6') IS NOT NULL DROP TABLE #geo6
CREATE TABLE #geo6 (code varchar(3), name varchar(256), name_PL varchar(256))
INSERT INTO #geo6 VALUES ('AD', 'Andorra', 'Andora')
INSERT INTO #geo6 VALUES ('AE', 'United Arab Emirates (the)', 'Zjednoczone Emiraty Arabskie')
INSERT INTO #geo6 VALUES ('AF', 'Afghanistan', 'Afganistan')
INSERT INTO #geo6 VALUES ('AG', 'Antigua and Barbuda', 'Antigua i Barbuda')
INSERT INTO #geo6 VALUES ('AI', 'Anguilla', 'Anguilla')
INSERT INTO #geo6 VALUES ('AL', 'Albania', 'Albania')
INSERT INTO #geo6 VALUES ('AM', 'Armenia', 'Armenia')
INSERT INTO #geo6 VALUES ('AO', 'Angola', 'Angola ³¹cznie z Kabinda')
INSERT INTO #geo6 VALUES ('AQ', 'Antarctica', 'Antarktyda')
INSERT INTO #geo6 VALUES ('AR', 'Argentina', 'Argentyna')
INSERT INTO #geo6 VALUES ('AS', 'American Samoa', 'Samoa Amerykañskie')
INSERT INTO #geo6 VALUES ('AT', 'Austria', 'Austria')
INSERT INTO #geo6 VALUES ('AU', 'Australia', 'Australia')
INSERT INTO #geo6 VALUES ('AW', 'Aruba', 'Aruba')
INSERT INTO #geo6 VALUES ('AZ', 'Azerbaijan', 'Azerbejd¿an')
INSERT INTO #geo6 VALUES ('BA', 'Bosnia and Herzegovina', 'Boœnia i Hercegowina')
INSERT INTO #geo6 VALUES ('BB', 'Barbados', 'Barbados')
INSERT INTO #geo6 VALUES ('BD', 'Bangladesh', 'Bangladesz')
INSERT INTO #geo6 VALUES ('BE', 'Belgium', 'Belgia')
INSERT INTO #geo6 VALUES ('BF', 'Burkina Faso', 'Burkina Faso')
INSERT INTO #geo6 VALUES ('BG', 'Bulgaria', 'Bu³garia')
INSERT INTO #geo6 VALUES ('BH', 'Bahrain', 'Bahrajn')
INSERT INTO #geo6 VALUES ('BI', 'Burundi', 'Burundi')
INSERT INTO #geo6 VALUES ('BJ', 'Benin', 'Benin')
INSERT INTO #geo6 VALUES ('BM', 'Bermuda', 'Bermudy')
INSERT INTO #geo6 VALUES ('BN', 'Brunei Darussalam', 'Brunei Darussalam')
INSERT INTO #geo6 VALUES ('BO', 'Bolivia (Plurinational State of)', 'Boliwia')
INSERT INTO #geo6 VALUES ('BQ', 'Bonaire, Sint Eustatius and Saba', 'Bonaire, St Eustatius i Saba')
INSERT INTO #geo6 VALUES ('BR', 'Brazil', 'Brazylia')
INSERT INTO #geo6 VALUES ('BS', 'Bahamas (the)', 'Bahamy')
INSERT INTO #geo6 VALUES ('BT', 'Bhutan', 'Bhutan')
INSERT INTO #geo6 VALUES ('BV', 'Bouvet Island', 'Wyspa Bouveta')
INSERT INTO #geo6 VALUES ('BW', 'Botswana', 'Botswana')
INSERT INTO #geo6 VALUES ('BY', 'Belarus', 'Bia³oruœ')
INSERT INTO #geo6 VALUES ('BZ', 'Belize', 'Belize')
INSERT INTO #geo6 VALUES ('CA', 'Canada', 'Kanada')
INSERT INTO #geo6 VALUES ('CC', 'Cocos (Keeling) Islands (the)', 'Wyspy Kokosowe (Keelinga)')
INSERT INTO #geo6 VALUES ('CD', 'Congo (the Democratic Republic of the)', 'Kongo, Republika Demokratyczna')
INSERT INTO #geo6 VALUES ('CF', 'Central African Republic (the)', 'Republika Œrodkowoafrykañska')
INSERT INTO #geo6 VALUES ('CG', 'Congo (the)', 'Kongo')
INSERT INTO #geo6 VALUES ('CH', 'Switzerland', 'Szwajcaria')
INSERT INTO #geo6 VALUES ('CI', 'Côte d' + char(39)+ 'Ivoire', 'Wybrze¿e Koœci S³oniowej')
INSERT INTO #geo6 VALUES ('CK', 'Cook Islands (the)', 'Wyspy Cooka')
INSERT INTO #geo6 VALUES ('CL', 'Chile', 'Chile')
INSERT INTO #geo6 VALUES ('CM', 'Cameroon', 'Kamerun')
INSERT INTO #geo6 VALUES ('CN', 'China', 'Chiny')
INSERT INTO #geo6 VALUES ('CO', 'Colombia', 'Kolumbia')
INSERT INTO #geo6 VALUES ('CR', 'Costa Rica', 'Kostaryka')
INSERT INTO #geo6 VALUES ('CU', 'Cuba', 'Kuba')
INSERT INTO #geo6 VALUES ('CV', 'Cabo Verde', 'Wyspy Zielonego Przyl¹dka')
INSERT INTO #geo6 VALUES ('CW', 'Curaçao', 'Curacao')
INSERT INTO #geo6 VALUES ('CX', 'Christmas Island', 'Wyspa Bo¿ego Narodzenia')
INSERT INTO #geo6 VALUES ('CY', 'Cyprus', 'Cypr')
INSERT INTO #geo6 VALUES ('CZ', 'Czechia', 'Czechy')
INSERT INTO #geo6 VALUES ('DE', 'Germany', 'Niemcy')
INSERT INTO #geo6 VALUES ('DJ', 'Djibouti', 'D¿ibuti')
INSERT INTO #geo6 VALUES ('DK', 'Denmark', 'Dania')
INSERT INTO #geo6 VALUES ('DM', 'Dominica', 'Dominika')
INSERT INTO #geo6 VALUES ('DO', 'Dominican Republic (the)', 'Republika Dominikany')
INSERT INTO #geo6 VALUES ('DZ', 'Algeria', 'Algieria')
INSERT INTO #geo6 VALUES ('EC', 'Ecuador', 'Ekwador ')
INSERT INTO #geo6 VALUES ('EE', 'Estonia', 'Estonia')
INSERT INTO #geo6 VALUES ('EG', 'Egypt', 'Egipt')
INSERT INTO #geo6 VALUES ('EH', 'Western Sahara*', 'Sahara Zachodnia')
INSERT INTO #geo6 VALUES ('ER', 'Eritrea', 'Erytrea')
INSERT INTO #geo6 VALUES ('ES', 'Spain', 'Hiszpania')
INSERT INTO #geo6 VALUES ('ET', 'Ethiopia', 'Etiopia')
INSERT INTO #geo6 VALUES ('FI', 'Finland', 'Finlandia')
INSERT INTO #geo6 VALUES ('FJ', 'Fiji', 'Republika Fid¿i')
INSERT INTO #geo6 VALUES ('FK', 'Falkland Islands (the) [Malvinas]', 'Wyspy Falklandy (Malwiny)')
INSERT INTO #geo6 VALUES ('FM', 'Micronesia (Federated States of)', 'Federacja Mikronezji')
INSERT INTO #geo6 VALUES ('FO', 'Faroe Islands (the)', 'Wyspy Owcze')
INSERT INTO #geo6 VALUES ('FR', 'France', 'Francja')
INSERT INTO #geo6 VALUES ('GA', 'Gabon', 'Gabon')
INSERT INTO #geo6 VALUES ('GB', 'United Kingdom of Great Britain and Northern Ireland (the)', 'Wielka Brytania')
INSERT INTO #geo6 VALUES ('GD', 'Grenada', 'Grenada')
INSERT INTO #geo6 VALUES ('GE', 'Georgia', 'Gruzja')
INSERT INTO #geo6 VALUES ('GG', 'Guernsey', 'Guernsey')
INSERT INTO #geo6 VALUES ('GH', 'Ghana', 'Ghana')
INSERT INTO #geo6 VALUES ('GI', 'Gibraltar', 'Gibraltar')
INSERT INTO #geo6 VALUES ('GL', 'Greenland', 'Grenlandia')
INSERT INTO #geo6 VALUES ('GM', 'Gambia (the)', 'Gambia')
INSERT INTO #geo6 VALUES ('GN', 'Guinea', 'Gwinea')
INSERT INTO #geo6 VALUES ('GQ', 'Equatorial Guinea', 'Gwinea Równikowa')
INSERT INTO #geo6 VALUES ('GR', 'Greece', 'Grecja')
INSERT INTO #geo6 VALUES ('GS', 'South Georgia and the South Sandwich Islands', 'Georgia Po³udniowa i Sandwich Po³udniowy')
INSERT INTO #geo6 VALUES ('GT', 'Guatemala', 'Gwatemala')
INSERT INTO #geo6 VALUES ('GU', 'Guam', 'Guam')
INSERT INTO #geo6 VALUES ('GW', 'Guinea-Bissau', 'Gwinea Bissau')
INSERT INTO #geo6 VALUES ('GY', 'Guyana', 'Gujana')
INSERT INTO #geo6 VALUES ('HK', 'Hong Kong', 'Hongkong')
INSERT INTO #geo6 VALUES ('HM', 'Heard Island and McDonald Islands', 'Wyspa Heard i Wyspy McDonald')
INSERT INTO #geo6 VALUES ('HN', 'Honduras', 'Honduras')
INSERT INTO #geo6 VALUES ('HR', 'Croatia', 'Chorwacja')
INSERT INTO #geo6 VALUES ('HT', 'Haiti', 'Haiti')
INSERT INTO #geo6 VALUES ('HU', 'Hungary', 'Wêgry')
INSERT INTO #geo6 VALUES ('ID', 'Indonesia', 'Indonezja')
INSERT INTO #geo6 VALUES ('IE', 'Ireland', 'Irlandia')
INSERT INTO #geo6 VALUES ('IL', 'Israel', 'Izrael')
INSERT INTO #geo6 VALUES ('IM', 'Isle of Man', 'Wyspa Man')
INSERT INTO #geo6 VALUES ('IN', 'India', 'Indie')
INSERT INTO #geo6 VALUES ('IO', 'British Indian Ocean Territory (the)', 'Brytyjskie Terytorium Oceanu Indyjskiego ')
INSERT INTO #geo6 VALUES ('IQ', 'Iraq', 'Irak')
INSERT INTO #geo6 VALUES ('IR', 'Iran (Islamic Republic of)', 'Iran')
INSERT INTO #geo6 VALUES ('IS', 'Iceland', 'Islandia')
INSERT INTO #geo6 VALUES ('IT', 'Italy', 'W³ochy')
INSERT INTO #geo6 VALUES ('JE', 'Jersey', 'Jersey ')
INSERT INTO #geo6 VALUES ('JM', 'Jamaica', 'Jamajka')
INSERT INTO #geo6 VALUES ('JO', 'Jordan', 'Jordania')
INSERT INTO #geo6 VALUES ('JP', 'Japan', 'Japonia')
INSERT INTO #geo6 VALUES ('KE', 'Kenya', 'Kenia')
INSERT INTO #geo6 VALUES ('KG', 'Kyrgyzstan', 'Kirgistan')
INSERT INTO #geo6 VALUES ('KH', 'Cambodia', 'Kambod¿a (Kampucza)')
INSERT INTO #geo6 VALUES ('KI', 'Kiribati', 'Kiribati')
INSERT INTO #geo6 VALUES ('KM', 'Comoros (the)', 'Komory')
INSERT INTO #geo6 VALUES ('KN', 'Saint Kitts and Nevis', 'Saint Kitts i Nevis')
INSERT INTO #geo6 VALUES ('KP', 'Korea (the Democratic People' + char(39) + 's Republic of)', 'Koreañska Republika Ludowo-Demokratyczna (Korea Pó³nocna)')
INSERT INTO #geo6 VALUES ('KR', 'Korea (the Republic of)', 'Republika Korei (Korea Po³udniowa)')
INSERT INTO #geo6 VALUES ('KW', 'Kuwait', 'Kuwejt')
INSERT INTO #geo6 VALUES ('KY', 'Cayman Islands (the)', 'Kajmany')
INSERT INTO #geo6 VALUES ('KZ', 'Kazakhstan', 'Kazachstan')
INSERT INTO #geo6 VALUES ('LA', 'Lao People' + char(39) + 's Democratic Republic (the)', 'Laos')
INSERT INTO #geo6 VALUES ('LB', 'Lebanon', 'Liban')
INSERT INTO #geo6 VALUES ('LC', 'Saint Lucia', 'Saint Lucia')
INSERT INTO #geo6 VALUES ('LI', 'Liechtenstein', 'Liechtenstein')
INSERT INTO #geo6 VALUES ('LK', 'Sri Lanka', 'Sri Lanka')
INSERT INTO #geo6 VALUES ('LR', 'Liberia', 'Liberia')
INSERT INTO #geo6 VALUES ('LS', 'Lesotho', 'Lesotho')
INSERT INTO #geo6 VALUES ('LT', 'Lithuania', 'Litwa')
INSERT INTO #geo6 VALUES ('LU', 'Luxembourg', 'Luksemburg')
INSERT INTO #geo6 VALUES ('LV', 'Latvia', '£otwa')
INSERT INTO #geo6 VALUES ('LY', 'Libya', 'Libia')
INSERT INTO #geo6 VALUES ('MA', 'Morocco', 'Maroko')
INSERT INTO #geo6 VALUES ('MD', 'Moldova (the Republic of)', 'Mo³dowa')
INSERT INTO #geo6 VALUES ('ME', 'Montenegro', 'Czarnogóra')
INSERT INTO #geo6 VALUES ('MG', 'Madagascar', 'Madagaskar')
INSERT INTO #geo6 VALUES ('MH', 'Marshall Islands (the)', 'Wyspy Marshalla')
INSERT INTO #geo6 VALUES ('MK', 'North Macedonia', 'Macedonia')
INSERT INTO #geo6 VALUES ('ML', 'Mali', 'Mali')
INSERT INTO #geo6 VALUES ('MM', 'Myanmar', 'Myanmar (Birma)')
INSERT INTO #geo6 VALUES ('MN', 'Mongolia', 'Mongolia')
INSERT INTO #geo6 VALUES ('MO', 'Macao', 'Makao')
INSERT INTO #geo6 VALUES ('MP', 'Northern Mariana Islands (the)', 'Mariany Pó³nocne')
INSERT INTO #geo6 VALUES ('MR', 'Mauritania', 'Mauretania')
INSERT INTO #geo6 VALUES ('MS', 'Montserrat', 'Montserrat')
INSERT INTO #geo6 VALUES ('MT', 'Malta', 'Malta')
INSERT INTO #geo6 VALUES ('MU', 'Mauritius', 'Mauritius')
INSERT INTO #geo6 VALUES ('MV', 'Maldives', 'Malediwy')
INSERT INTO #geo6 VALUES ('MW', 'Malawi', 'Malawi')
INSERT INTO #geo6 VALUES ('MX', 'Mexico', 'Meksyk')
INSERT INTO #geo6 VALUES ('MY', 'Malaysia', 'Malezja')
INSERT INTO #geo6 VALUES ('MZ', 'Mozambique', 'Mozambik')
INSERT INTO #geo6 VALUES ('NA', 'Namibia', 'Namibia')
INSERT INTO #geo6 VALUES ('NC', 'New Caledonia', 'Nowa Kaledonia')
INSERT INTO #geo6 VALUES ('NE', 'Niger (the)', 'Niger')
INSERT INTO #geo6 VALUES ('NF', 'Norfolk Island', 'Wyspa Norfolk')
INSERT INTO #geo6 VALUES ('NG', 'Nigeria', 'Nigeria')
INSERT INTO #geo6 VALUES ('NI', 'Nicaragua', 'Nikaragua')
INSERT INTO #geo6 VALUES ('NL', 'Netherlands', 'Niderlandy')
INSERT INTO #geo6 VALUES ('NO', 'Norway', 'Norwegia ')
INSERT INTO #geo6 VALUES ('NP', 'Nepal', 'Nepal')
INSERT INTO #geo6 VALUES ('NR', 'Nauru', 'Nauru')
INSERT INTO #geo6 VALUES ('NU', 'Niue', 'Niue')
INSERT INTO #geo6 VALUES ('NZ', 'New Zealand', 'Nowa Zelandia')
INSERT INTO #geo6 VALUES ('OM', 'Oman', 'Oman ')
INSERT INTO #geo6 VALUES ('PA', 'Panama', 'Panama')
INSERT INTO #geo6 VALUES ('PE', 'Peru', 'Peru')
INSERT INTO #geo6 VALUES ('PF', 'French Polynesia', 'Polinezja Francuska')
INSERT INTO #geo6 VALUES ('PG', 'Papua New Guinea', 'Papua Nowa Gwinea')
INSERT INTO #geo6 VALUES ('PH', 'Philippines (the)', 'Filipiny')
INSERT INTO #geo6 VALUES ('PK', 'Pakistan', 'Pakistan')
--INSERT INTO #geo6 VALUES ('PL', 'Poland', 'Polska')
INSERT INTO #geo6 VALUES ('PN', 'Pitcairn', 'Pitcairn')
INSERT INTO #geo6 VALUES ('PS', 'Palestine, State of', 'Palestyna')
INSERT INTO #geo6 VALUES ('PT', 'Portugal', 'Portugalia ')
INSERT INTO #geo6 VALUES ('PW', 'Palau', 'Palau')
INSERT INTO #geo6 VALUES ('PY', 'Paraguay', 'Paragwaj')
INSERT INTO #geo6 VALUES ('QA', 'Qatar', 'Katar')
INSERT INTO #geo6 VALUES ('RO', 'Romania', 'Rumunia')
INSERT INTO #geo6 VALUES ('RS', 'Serbia', 'Serbia')
INSERT INTO #geo6 VALUES ('RU', 'Russian Federation (the)', 'Federacja Rosyjska')
INSERT INTO #geo6 VALUES ('RW', 'Rwanda', 'Rwanda')
INSERT INTO #geo6 VALUES ('SA', 'Saudi Arabia', 'Arabia Saudyjska')
INSERT INTO #geo6 VALUES ('SB', 'Solomon Islands', 'Wyspy Salomona')
INSERT INTO #geo6 VALUES ('SC', 'Seychelles', 'Seszele')
INSERT INTO #geo6 VALUES ('SD', 'Sudan (the)', 'Sudan')
INSERT INTO #geo6 VALUES ('SE', 'Sweden', 'Szwecja')
INSERT INTO #geo6 VALUES ('SG', 'Singapore', 'Singapur')
INSERT INTO #geo6 VALUES ('SH', 'Saint Helena, Ascension and Tristan da Cunha', 'Wyspa Œwiêtej Heleny')
INSERT INTO #geo6 VALUES ('SI', 'Slovenia', 'S³owenia')
INSERT INTO #geo6 VALUES ('SJ', 'Svalbard and Jan Mayen', 'Svalbard i Jan Mayen')
INSERT INTO #geo6 VALUES ('SK', 'Slovakia', 'S³owacja')
INSERT INTO #geo6 VALUES ('SL', 'Sierra Leone', 'Sierra Leone')
INSERT INTO #geo6 VALUES ('SM', 'San Marino', 'San Marino')
INSERT INTO #geo6 VALUES ('SN', 'Senegal', 'Senegal')
INSERT INTO #geo6 VALUES ('SO', 'Somalia', 'Somalia')
INSERT INTO #geo6 VALUES ('SR', 'Suriname', 'Surinam')
INSERT INTO #geo6 VALUES ('SS', 'South Sudan', 'Sudan Po³udniowy')
INSERT INTO #geo6 VALUES ('ST', 'Sao Tome and Principe', 'Wyspy Œwiêtego Tomasza i Ksi¹¿êca')
INSERT INTO #geo6 VALUES ('SV', 'El Salvador', 'Salwador')
INSERT INTO #geo6 VALUES ('SX', 'Sint Maarten (Dutch part)', 'Sint Maarten')
INSERT INTO #geo6 VALUES ('SY', 'Syrian Arab Republic (the)', 'Syria')
INSERT INTO #geo6 VALUES ('SZ', 'Eswatini', 'Eswatin')
INSERT INTO #geo6 VALUES ('TC', 'Turks and Caicos Islands (the)', 'Wyspy Turks i Caicos')
INSERT INTO #geo6 VALUES ('TD', 'Chad', 'Czad')
INSERT INTO #geo6 VALUES ('TF', 'French Southern Territories (the)', 'Francuskie Terytoria Po³udniowe')
INSERT INTO #geo6 VALUES ('TG', 'Togo', 'Togo')
INSERT INTO #geo6 VALUES ('TH', 'Thailand', 'Tajlandia')
INSERT INTO #geo6 VALUES ('TJ', 'Tajikistan', 'Tad¿ykistan')
INSERT INTO #geo6 VALUES ('TK', 'Tokelau', 'Tokelau')
INSERT INTO #geo6 VALUES ('TL', 'Timor-Leste', 'Timor Wschodni')
INSERT INTO #geo6 VALUES ('TM', 'Turkmenistan', 'Turkmenistan')
INSERT INTO #geo6 VALUES ('TN', 'Tunisia', 'Tunezja')
INSERT INTO #geo6 VALUES ('TO', 'Tonga', 'Tonga')
INSERT INTO #geo6 VALUES ('TR', 'Turkey', 'Turcja')
INSERT INTO #geo6 VALUES ('TT', 'Trinidad and Tobago', 'Trynidad i Tobago')
INSERT INTO #geo6 VALUES ('TV', 'Tuvalu', 'Tuvalu')
INSERT INTO #geo6 VALUES ('TW', 'Taiwan (Province of China)', 'Tajwan')
INSERT INTO #geo6 VALUES ('TZ', 'Tanzania, the United Republic of', 'Tanzania')
INSERT INTO #geo6 VALUES ('UA', 'Ukraine', 'Ukraina')
INSERT INTO #geo6 VALUES ('UG', 'Uganda', 'Uganda')
INSERT INTO #geo6 VALUES ('UM', 'United States Minor Outlying Islands (the)', 'Terytoria Zamorskie Stanów Zjednoczonych')
INSERT INTO #geo6 VALUES ('US', 'United States of America (the)', 'Stany Zjednoczone Ameryki Pó³nocnej ³¹cznie z Portoryko i Navassa')
INSERT INTO #geo6 VALUES ('UY', 'Uruguay', 'Urugwaj')
INSERT INTO #geo6 VALUES ('UZ', 'Uzbekistan', 'Uzbekistan')
INSERT INTO #geo6 VALUES ('VA', 'Holy See (the)', 'Watykan')
INSERT INTO #geo6 VALUES ('VC', 'Saint Vincent and the Grenadines', 'Saint Vincent i Grenadyny')
INSERT INTO #geo6 VALUES ('VE', 'Venezuela (Bolivarian Republic of)', 'Wenezuela')
INSERT INTO #geo6 VALUES ('VG', 'Virgin Islands (British)', 'Brytyjskie Wyspy Dziewicze')
INSERT INTO #geo6 VALUES ('VI', 'Virgin Islands (U.S.)', 'Wyspy Dziewicze Stanów Zjednoczonych')
INSERT INTO #geo6 VALUES ('VN', 'Viet Nam', 'Wietnam')
INSERT INTO #geo6 VALUES ('VU', 'Vanuatu', 'Vanuatu')
INSERT INTO #geo6 VALUES ('W2', 'Domestic', 'Krajowe')
INSERT INTO #geo6 VALUES ('WF', 'Wallis and Futuna', 'Wallis i Futuna')
INSERT INTO #geo6 VALUES ('WS', 'Samoa', 'Samoa')
INSERT INTO #geo6 VALUES ('YE', 'Yemen', 'Jemen ³¹cznie z wyspami Perim, Kamaran, Socotra')
INSERT INTO #geo6 VALUES ('ZA', 'South Africa', 'Republika Po³udniowej Afryki')
INSERT INTO #geo6 VALUES ('ZM', 'Zambia', 'Zambia')
INSERT INTO #geo6 VALUES ('ZW', 'Zimbabwe', 'Zimbabwe')
INSERT INTO #geo6 VALUES ('D09', 'Extra UE not allocated', 'Pozosta³e kraje')
--select * from #geo6


SELECT t.CountryCode, g.name_PL, g.name
	,[podzia³ NBP] as podzial_NBP
	,SUM(ilosc) as ilosc_transakcji
	,SUM(ilosc_internet) as ilosc_internet
	,SUM([iloœæ transakcji CashBack]) as ilosc_transakcji_CashBack
	,SUM([wartoœæ transakcji]) as wartosc_transakcji
	,SUM(wartosc_internet) as wartosc_internet
	,SUM([Wartoœæ wyp³at CashBack]) as wartosc_wyplat_CashBack
FROM #transakcje t
LEFT JOIN #geo6 g on g.code = t.CountryCode 
GROUP BY t.CountryCode, g.name_PL, g.name, [podzia³ NBP]
ORDER BY [podzia³ NBP] desc, g.name





