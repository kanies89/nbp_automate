/*
Wynikiem zapytania jest lista transakcji BLIK.
Dotyczy:		Raport kwartalny NBP. 
Autor:			Damian Witkowski
Odbiorca:		Zespó³ Przetwarzania
Serwer:			PRDBI
Baza danych:	paytel_olap
*/
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED
USE paytel_olap

declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1, '19000101');
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-0 , '19000101');
select @dtb,@dte
SELECT
	count(*) AS 'Liczba transakcji BLIK',
	SUM(convert(money,ABS(tr_amount/100))) AS 'Kwota transakcji BLIK'
	
FROM
	trans WITH (NOLOCK)-- w przypadku starszych ni¿ 90 dni v_trans

WHERE
	tr_reversed = 0
  	and tr_rsp_code = '00'
	AND tr_message_type IN (200, 220)
	and tr_app_id = '25'
	and tr_datetime_local between @dtb and @dte