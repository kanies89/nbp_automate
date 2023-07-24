-- RAPORT NBP zakładka 5a.R.SF dotyczy strat poniesionych w wyniku chb przez paytel, merchantów i agentów

SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED


declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1, '19000101');
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-0 , '19000101');
select @dtb,@dte