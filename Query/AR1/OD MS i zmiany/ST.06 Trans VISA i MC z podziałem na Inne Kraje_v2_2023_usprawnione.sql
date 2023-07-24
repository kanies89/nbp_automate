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
	WHEN  VT.country in ('QZ', 'QZZ') THEN 'Extra UE not allocated'
	WHEN  VT.country in ('SZ') THEN 'Extra UE not allocated'
	WHEN cc_name = 'Puerto Rico' THEN 'United States of America'
	WHEN  cc_name = 'Germany' THEN 'Niemcy'
	WHEN cc_name = 'Spain' THEN 'Hiszpania'  
	ELSE cc_name end as CountryName
,CASE WHEN VT.country = 'PR' THEN 'US' 
		WHEN VT.country in ('QZ', 'QZZ') THEN 'D09'
		WHEN  VT.country in ('SZ')  THEN 'D09'
		ELSE VT.country end as CountryCode, 
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
	WHEN MC.country in ('QZ', 'QZZ') THEN 'Extra UE not allocated'
	WHEN cc_name = 'Puerto Rico' THEN 'United States of America'
	WHEN cc_name = 'Germany' THEN 'Niemcy' 
	WHEN cc_name = 'Spain' THEN 'Hiszpania' 
	ELSE cc_name end as CountryName
	,case
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
		WHEN MC.country ='SWZ' THEN 'D09'
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
		WHEN MC.country = 'QZZ' THEN 'D09'   --- KOSOWO 
		ELSE 'uwaga - coœ nowego'
		END as 'CountryCode'
 ,count(*) as 'iloœæ transakcji'
 ,sum(convert(money,abs(tr_amount)))/100 as 'wartoœæ transakcji',
   0 as 'ilosc_internet',
    0 as 'wartosc_internet',
 count(case when tr_cash_req > 0 then 1 END) as 'iloœæ transakcji CashBack',
 sum(convert(money,abs(tr_cash_req/100)))as 'Wartoœæ wyp³at CashBack',

 case 
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
INSERT INTO #geo6 VALUES ('D09','Extra UE not allocated') -- D09  (mo¿na ustawiæ jako zz dla sortowania)
select * from #geo6


select t.CountryCode, g.name, t.CountryName, [podzia³ NBP] as podzial_NBP, sum(ilosc) as ilosc, sum([wartoœæ transakcji]) as wartosc_transakcji, sum(ilosc_internet) as ilosc_internet, sum(wartosc_internet) as wartosc_internet, sum([iloœæ transakcji CashBack]) as ilosc_transakcji_CashBack, sum([Wartoœæ wyp³at CashBack]) as Wartosc_wyplat_CashBack
from #transakcje t
left join #geo6 g on g.code = t.CountryCode 
group by t.CountryCode, g.name, t.CountryName, [podzia³ NBP]



