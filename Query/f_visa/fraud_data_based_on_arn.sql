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
aquirerReferenceNumber in 