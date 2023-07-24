select count(sp_tvid) as ilosc_softPOS FROM #softposterm

---split---

SELECT 
      count(distinct([tr_mid])) as 'MID all cashback'
      ,count(distinct([tr_sid])) as 'SID all cashback'
      ,count([tr_tvid]) as 'TVID all cashback'
      FROM [warehouse_data].[dbo].[active_application_tvid] 
	  WHERE tr_date = dateadd(d,-1,DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-0 , '19000101')) and cashback = 1