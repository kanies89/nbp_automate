SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED
SELECT
aquirerReferenceNumber 'ARN',
tr_sink_node,
m_network,
m_mid 'MID',
m_name 'MID_name', 
_tr_tid 'TID'
	,CASE WHEN accountFundingSource IN ('C','R') THEN 'Credit'
		WHEN accountFundingSource IN ('P','D') THEN 'Debit' 
		WHEN accountFundingSource = 'H' THEN 'Charge'
		ELSE accountFundingSource
		END AS 'Typ_karty'
	,CASE
		WHEN te_pos_cardholder_auth_method in ('A', 'B', 'C', 'D', '9') THEN 'SCA'    --- dwuskładnikowe
		ELSE 'non_SCA'    ----- dwuskładnikowe
		END as czy_SCA,
abs(convert(money,(tr_amount/100))) 'tr_amout',
CASE
	WHEN substring(te_pos_entry_mode, 1, 2) in ('02','90') then 'MS'
	WHEN substring(te_pos_entry_mode, 1, 2) in ('04','05', '95') then 'CHIP'
	WHEN substring(te_pos_entry_mode, 1, 2) in ('07','91') then 'CTLS'
	ELSE te_pos_entry_mode
END pos_entry_mode,
country

FROM
[paytel_olap].[dbo].[v_trans] -- w przypadku starszych niż 90 dni v_trans
join v_trans_ext on (tr_tran_nr=te_tran_nr)	
left join v_visa_transaction  on (tranNr=tr_tran_nr) 
join terminal on (_tr_tid=_t_tid)
join shop on (ms_id=t_sid)
join merchant on (tr_mid=m_mid)

WHERE 
aquirerReferenceNumber in ('74410493005017828454962', '74410493005017828451661', '74410493005017828462023', '74410493007017831981769', '74410493007017831975381', '74410493007017831917052', '74410493007017831927267', '74410493007017831921500', '74410492334017608880877', '74410492341017654864107', '74410492351017724524365', '74410493059018147855579', '74410493063018170959771', '74410493063018171016225', '74410492344017673832314', '74410492302017406869161', '74410493070018219974402', '74410493021017916143345', '74410493019017902217818', '74410493019017902215549', '74410493021017916117588', '74410493019017902223113', '74410493021017916091973', '74410493021017916107670', '74410493019017902221422', '74410493021017916126746', '74410493021017916068500', '74410493054018113424959', '74410493069018212344275', '74410493046018065931697', '74410493054018113424959', '74410493069018212344275', '74410493046018065931697', '74410493078018268722720', '74410493078018268730467', '74410493085018314182698')