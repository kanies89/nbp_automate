-- RAPORT NBP zakładka 5a.R.LF_PLiW2 oraz 5a.R.WF_PLiW2, informacje dotyczące fraudów, dane tworzone przy pomocy statego pliku excel z fraudami


set transaction isolation level read uncommitted
IF OBJECT_ID('tempdb..#dane') IS NOT NULL DROP TABLE #dane
SELECT distinct
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

	,CS.cc_A2
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
 and it.aquirerReferenceNumber in ('',
									'05185243010029351149884',
									'05185243010029351105662',
									'05185243010029351082242',
									'05185243010029351011258',
									'05185243010029351027288',
									'05185243010029350865498',
									'05185243010029350750518',
									'05185242364029212952124',
									'05185242364029212997210',
									'05185242358029145813789',
									'05185242358029146394821',
									'05185242358029148095855',
									'05185243010029345915846',
									'05185243010029346132177',
									'05185242276027737386171',
									'',
									'05185243060030110609530',
									'05185243065030200228121')

LEFT JOIN mc_transaction AS MCT (NOLOCK)ON IT.postTranId = MCT.postTranId
LEFT JOIN  country_codes CS (nolock) on country=cc_A3
JOIN terminal on (_tr_tid=_t_tid)
JOIN merchant on (tr_mid=m_mid)


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
	END pos_entry_mode,
	country ,
	accountFundingSource
		,IIF(substring(te_pos_entry_mode, 1, 2) = '01', 'MOTO', 'inne') as czy_moto
		,IIF(paytel_olap.dbo.getKeyValue(te_structured_data_req, 'Log') LIKE '%SC1%', 'SC1', 'SC0') as 'czy_SCA'
		,te_pos_cardholder_auth_method
				,CASE WHEN abs(tr_amount)<=10000 and substring(te_pos_entry_mode, 1, 2) in ('07','91') THEN 1
				ELSE 0 end as czy_niskokwotowa_zblizeniowa
FROM
[paytel_olap].[dbo].[v_trans] -- w przypadku starszych niż 90 dni v_trans
join v_trans_ext on (tr_tran_nr=te_tran_nr)	
left join v_visa_transaction  on (tranNr=tr_tran_nr) 
join terminal on (_tr_tid=_t_tid)
join shop on (ms_id=t_sid)
join merchant on (tr_mid=m_mid)
WHERE 
aquirerReferenceNumber in
('74410493005017828454962',
'74410493005017828451661',
'74410493005017828462023',
'74410493007017831981769',
'74410493007017831975381',
'74410493007017831917052',
'74410493007017831927267',
'74410493007017831921500',
'74410492334017608880877',
'74410492341017654864107',
'74410492351017724524365',
'74410493059018147855579',
'74410493063018170959771',
'74410493063018171016225',
'74410492344017673832314',
'74410492302017406869161',
'74410493070018219974402',
'74410493021017916143345',
'74410493019017902217818',
'74410493019017902215549',
'74410493021017916117588',
'74410493019017902223113',
'74410493021017916091973',
'74410493021017916107670',
'74410493019017902221422',
'74410493021017916126746',
'74410493021017916068500',
'74410493054018113424959',
'74410493069018212344275',
'74410493046018065931697',
'74410493054018113424959',
'74410493069018212344275',
'74410493046018065931697',
'74410493078018268722720',
'74410493078018268730467',
'74410493085018314182698')
order by aquirerReferenceNumber


