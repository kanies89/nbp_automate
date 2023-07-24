select count(sp_tvid) as ilosc_softPOS FROM #softposterm

---split---

SELECT 
      count(distinct([tr_mid])) as 'MID all cashback'
      ,count(distinct([tr_sid])) as 'SID all cashback'
      ,count([tr_tvid]) as 'TVID all cashback'
      FROM [warehouse_data].[dbo].[active_application_tvid] 
	  WHERE tr_date = dateadd(d,-2,DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1 , '19000101')) and cashback = 1 --changed from -1 to -2 due to checking 2 quaters in the past, changed from 0 to -1 due to checking 2 quaters in the past