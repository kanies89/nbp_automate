select count(sp_tvid) as ilosc_softPOS FROM #softposterm

---split---

SELECT  
count (distinct ms_m_mid) AS 'MID all cashback',
count (distinct ms_id) AS 'SID all cashback',
count (distinct t_vid) AS 'TVID all cashback'
FROM         
       terminal
       left join terminal_app ON t_vid = ta_t_vid
       left join device _d ON t_de_id = _d.de_id
       left join device_model _dm ON _d.de_dm_id = _dm.dm_id
       left join device _d1 on _d1.de_group_id = _d.de_group_id
       left join device_model _dm1 on _d1.de_dm_id=_dm1.dm_id
       left join merchant_shop ON t_ms_id = ms_id

       
WHERE     
       ta_status = 4
       AND ta_av_id IN ('12', '15')      --tylko eP + eP(billpayment)
       AND t_de_id IS NOT NULL                 --tylko z przypisanem urządzeniem
       AND ms_m_mid <> 'X0001'                 --wyklucz wew. PayTel
--     AND ((_dm1.dm_name like '%CTLS%' or _dm1.dm_name like '%Cless%' or _dm1.dm_name like '%IWL%') OR ( _dm.dm_name like '%CTLS%' or _dm.dm_name like '%Cless%' or _dm.dm_name like '%IWL%') )
       AND t_parent_vid is null --wyklucz powizane
       AND (_dm.dm_name not like 'VIRTUAL%' OR _dm1.dm_name not like 'VIRTUAL%')
	   AND t_cashback_enabled=1