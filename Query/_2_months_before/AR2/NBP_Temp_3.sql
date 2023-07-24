-- RAPORT NBP zakładka 5a.R.SF dotyczy strat poniesionych w wyniku chb przez paytel, merchantów i agentów

SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED


declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-2, '19000101'); --changed from -1 to -2 due to checking 2 quaters in the past
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1 , '19000101'); --changed from 0 to -1 due to checking 2 quaters in the past
select @dtb,@dte