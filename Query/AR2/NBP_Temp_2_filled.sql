-- RAPORT NBP zakładka 5a.R.LF_PLiW2 oraz 5a.R.WF_PLiW2, informacje dotyczące fraudów, dane tworzone zamiast statego pliku excel z fraudami

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

set transaction isolation level read uncommitted
IF OBJECT_ID('tempdb..#dane') IS NOT NULL DROP TABLE #dane
SELECT distinct
	aquirerReferenceNumber 'ARN',
	tr_sink_node,
	m_network,
	m_mid 'MID',
	m_name 'MID_name', 
	_tr_tid 'TID',
	abs(convert(money,(tr_amount/100))) 'tr_amout'
	,CASE
		WHEN substring(te_pos_entry_mode, 1, 2) in ('02','90') then 'MS'
		WHEN substring(te_pos_entry_mode, 1, 2) in ('04','05', '95') then 'CHIP'
		WHEN substring(te_pos_entry_mode, 1, 2) in ('07','91') then 'CTLS'
		ELSE te_pos_entry_mode
	END pos_entry_mode
	,CASE WHEN ipc_category1 = 'C' THEN 'Credit'
		WHEN ipc_category1 IN ('P','D') THEN 'Debit' 
		WHEN ipc_category1 = 'CH' THEN 'Charge'
		ELSE ipc_category1
		END AS 'Typ_karty'

	--,iif(CS.cc_A2 = 'PL', 'W2', CS.cc_A2) as country
	,CS.cc_A2
	,case when code is null then 'G1' when code = 'PL' THEN 'W2' else code end   as code
	,'' as 'accountFundingSource'
	,IIF(substring(te_pos_entry_mode, 1, 2) = '01', 'MOTO', 'inne') as czy_moto
	,IIF(paytel_olap.dbo.getKeyValue(te_structured_data_req, 'Log') LIKE '%SC1%', 'SC1', 'SC0') as 'czy_SCA'
		,te_pos_cardholder_auth_method
		,CASE WHEN abs(tr_amount)<=10000 and substring(te_pos_entry_mode, 1, 2) in ('07','91') THEN 1
				ELSE 0 end as czy_niskokwotowa_zblizeniowa
INTO #dane
FROM [paytel_olap].[dbo].[v_trans] -- w przypadku starszych niż 90 dni v_trans
JOIN v_trans_ext on (tr_tran_nr=te_tran_nr)    
JOIN if_transaction AS IT (NOLOCK) ON isnull(tr_prev_tran_nr, tr_tran_nr) = tranNr 
 and it.aquirerReferenceNumber in ('05185243074030360473185', '05185243090030631480563', '05185243115031043558906', '05185243115031043546109', '05185243117031078316178', '05185243062030157497409', '05185243115031032952565', '05185242330028682998303', '05185242330028682845504', '05185242328028646718304', '05185243048029942470951', '05185242330028683114876', '05185243129031273801293', '05185243112031000863540', '05185243112031000859662', '05185243117031072573436', '05185243117031072732941', '05185243148031663818540', '05185243148031664201852', '05185243163031957574445', '05185243163031957671639', '05185243165032001035571')

LEFT JOIN mc_transaction AS MCT (NOLOCK)ON IT.postTranId = MCT.postTranId
LEFT JOIN  country_codes CS (nolock) on country=cc_A3
left JOIN terminal on (_tr_tid=_t_tid)
left JOIN merchant on (tr_mid=m_mid)
LEFT JOIN paytel_olap.dbo.if_product_category (NOLOCK) ON gcmsProductId = ipc_product_id
left join #geo3 on code = CS.cc_A2

UNION
SELECT
	aquirerReferenceNumber 'ARN',
	tr_sink_node,
	m_network,
	m_mid 'MID',
	m_name 'MID_name', 
	_tr_tid 'TID',
	abs(convert(money,(tr_amount/100))) 'tr_amout',
	CASE
		WHEN substring(te_pos_entry_mode, 1, 2) in ('02','90') then 'MS'
		WHEN substring(te_pos_entry_mode, 1, 2) in ('04','05', '95') then 'CHIP'
		WHEN substring(te_pos_entry_mode, 1, 2) in ('07','91') then 'CTLS'
		ELSE te_pos_entry_mode
	END pos_entry_mode
	,CASE WHEN accountFundingSource IN ('C','R') THEN 'Credit'
		WHEN accountFundingSource IN ('P','D') THEN 'Debit' 
		WHEN accountFundingSource = 'H' THEN 'Charge'
		ELSE accountFundingSource
		END AS 'Typ_karty'
	,country
	,case when code is null then 'G1' when code = 'PL' THEN 'W2' else code end  as code
	--,iif(country = 'POL', 'W2', country) as country
	,accountFundingSource
		,IIF(substring(te_pos_entry_mode, 1, 2) = '01', 'MOTO', 'inne') as czy_moto
		,IIF(paytel_olap.dbo.getKeyValue(te_structured_data_req, 'Log') LIKE '%SC1%', 'SC1', 'SC0') as 'czy_SCA'
		,te_pos_cardholder_auth_method
				,CASE WHEN abs(tr_amount)<=10000 and substring(te_pos_entry_mode, 1, 2) in ('07','91') THEN 1
				ELSE 0 end as czy_niskokwotowa_zblizeniowa
FROM [paytel_olap].[dbo].[v_trans] -- w przypadku starszych niż 90 dni v_trans
join v_trans_ext on (tr_tran_nr=te_tran_nr)	
left join v_visa_transaction  on (tranNr=tr_tran_nr) 
left join terminal on (_tr_tid=_t_tid)
left join shop on (ms_id=t_sid)
left join merchant on (tr_mid=m_mid)
left join paytel_olap.dbo.visa_product_id on productId=vp_product_id
left join #geo3 on code = country

WHERE 
aquirerReferenceNumber in ('74410493084018307202371', '74410493084018307202280', '74410493090018348774422', '74410493090018343830799', '74410493078018268394850', '74410493089018343438349', '74410493096018387090072', '74410493100018407963104', '74410493115018506674613', '74410493115018509806014', '74410493115018506669399', '74410493125018572704060', '74410493119018539998258', '74410493132018629398370', '74410493133018636262717', '74410493056018128407831', '74410493155018800305899', '74410493155018800304504', '74410493162018849701638', '74410493167018883769124', '74410493167018883770932', '74410493161018842810452', '74410493161018842818323', '74410493168018893046512', '74410493162018847887330', '74410493162018847887215', '74410493171018914403184', '74410493171018919430398', '74410493171018918839193', '74410493171018914376935', '74410493160018832288066') 
order by aquirerReferenceNumber

