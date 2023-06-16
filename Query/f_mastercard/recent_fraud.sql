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
	END pos_entry_mode,
	CS.cc_A2
	,CASE WHEN ipc_category1 = 'C' THEN 'Credit'
		WHEN ipc_category1 IN ('P','D') THEN 'Debit' 
		WHEN ipc_category1 = 'CH' THEN 'Charge'
		ELSE ipc_category1
		END AS 'Typ_karty'
	,CASE
		WHEN te_pos_cardholder_auth_method in ('A', 'B', 'C', 'D', '9') THEN 'SCA'    ----- dwuskładnikowe
		ELSE 'non_SCA'  ----- dwuskładnikowe
		END as czy_SCA
FROM [paytel_olap].[dbo].[v_trans] -- w przypadku starszych niż 90 dni v_trans
JOIN v_trans_ext on (tr_tran_nr=te_tran_nr)    
--left join v_mc_transaction MC  on (tranNr=tr_tran_nr) 
--left join mcipm_ip0072t1 on MC.memberId=mcipm_ip0072t1.member_id 
--left join country_codes CS on mcipm_ip0072t1.country_code=cc_A3
JOIN if_transaction AS IT (NOLOCK) ON isnull(tr_prev_tran_nr, tr_tran_nr) = tranNr 
LEFT JOIN mc_transaction AS MCT (NOLOCK)ON IT.postTranId = MCT.postTranId
LEFT JOIN  country_codes CS (nolock) on country=cc_A3
JOIN terminal on (_tr_tid=_t_tid)
--join shop on (ms_id=t_sid)
JOIN merchant on (tr_mid=m_mid)
	LEFT JOIN if_product_category (NOLOCK) ON gcmsProductId = ipc_product_id

WHERE 
it.aquirerReferenceNumber in ('05185243010029351149884', '05185243010029351105662', '05185243010029351082242', '05185243010029351011258', '05185243010029351027288', '05185243010029350865498', '05185243010029350750518', '05185242364029212952124', '05185242364029212997210', '05185242358029145813789', '05185242358029146394821', '05185242358029148095855', '05185243010029345915846', '05185243010029346132177', '05185242276027737386171', '05185243060030110609530', '05185243065030200228121')