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
aquirerReferenceNumber in ('74410493084018307202371', '74410493084018307202280', '74410493090018348774422', '74410493090018343830799', '74410493078018268394850', '74410493089018343438349', '74410493096018387090072', '74410493100018407963104', '74410493115018506674613', '74410493115018509806014', '74410493115018506669399', '74410493125018572704060', '74410493119018539998258', '74410493132018629398370', '74410493133018636262717', '74410493056018128407831', '74410493155018800305899', '74410493155018800304504', '74410493162018849701638', '74410493167018883769124', '74410493167018883770932', '74410493161018842810452', '74410493161018842818323', '74410493168018893046512', '74410493162018847887330', '74410493162018847887215', '74410493171018914403184', '74410493171018919430398', '74410493171018918839193', '74410493171018914376935', '74410493160018832288066')