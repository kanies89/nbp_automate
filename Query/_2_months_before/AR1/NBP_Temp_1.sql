USE MDM_PROD

if object_id (N'tempdb..#softposterm')  is not null drop table #softposterm
select left(s_ta_tid,6)as sp_tvid,s_ta_tid 
into #softposterm
from [MDM_PROD].[dbo].[softpos] sp (nolock)
join  [MDM_PROD].[dbo].[terminal_app] ap (nolock) on s_ta_tid = ta_tid
where ta_av_id = 12
and s_deleted <>1
and ta_mid <>'X0001'
and s_id >37