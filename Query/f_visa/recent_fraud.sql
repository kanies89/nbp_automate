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
aquirerReferenceNumber in ('74410493265019613830138', '74410493265019614462758', '74410493265019614129860', '74410493265019615992035', '74410493265019615719479', '74410493265019615717465', '74410493265019615707706', '74410493265019615703598', '74410493265019615705692', '74410493265019615710189', '74410493265019615712342', '74410493269019638417883', '74410493273019663976666', '74410493273019663983563', '74410493282019723364639', '74410493272019658736118', '74410493296019816832116', '74410493303019865193106', '74410493305019873640807', '74410493305019873640906', '74410493305019873640484', '74410493311019909611550', '74410493304019869002724', '74410493302019857407440', '74410493303019859989659', '74410493332020032039219', '74410493344020104113062', '74410493279019707409850', '74410493347020125677183', '74410493282019723486275', '74410493282019726012722', '74410493340020083030976', '74410493348020130474765', '74410493346020119551411', '74410493349020136185141')