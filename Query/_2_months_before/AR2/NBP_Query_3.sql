-- RAPORT NBP zakładka 5a.R.SF dotyczy strat poniesionych w wyniku chb przez paytel, merchantów i agentów

SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED


declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-2, '19000101'); --changed from -1 to -2 due to checking 2 quaters in the past
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1 , '19000101'); --changed from 0 to -1 due to checking 2 quaters in the past
select @dtb,@dte

---split---

SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED


declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-2, '19000101'); --changed from -1 to -2 due to checking 2 quaters in the past
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1 , '19000101'); --changed from 0 to -1 due to checking 2 quaters in the past

SELECT [id_c]
      ,[Status]
      ,[cd_id]
      ,[status_kpi_days]
      ,[Finish_Time]
      ,[status_user_comments]
      ,[status_date]
      ,[user_id]
      ,[user]
      ,[ARN]
      ,[date_CHB]
      ,[type]
      ,[status_user_date]
      ,[case_id]
      ,[code]
      ,[network]
      ,[tid]
      ,[agent_id]
      ,[agent_name]
      ,[agent_street]
      ,[agent_code]
      ,[agent_city]
      ,[tran_number]
      ,[tran_datetime]
      ,[tran_amount]
      ,[card_number]
      ,[shop_id]
      ,[shop_name]
      ,[shop_street]
      ,[shop_code]
      ,[shop_city]
      ,[pos_entry_mode]
      ,[message_text]
      ,[deleted]
      ,[import_char]
      ,[reason_code]
      ,[country]
      ,[charge_merchant_date]
      ,[status_insert_datetime_order]
      ,[jira]
      ,[prearbitraz]
      ,[arbitraz]
  FROM [paytel_olap].[dbo].[v_rs_chargeback]
  where [date_CHB] >= @dtb AND date_CHB < @dte
  and upper(Status) like '%PRZEGRANA%'
  
  ---split---

SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED


declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-2, '19000101'); --changed from -1 to -2 due to checking 2 quaters in the past
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1 , '19000101'); --changed from 0 to -1 due to checking 2 quaters in the past

  select SUM(cast(abs(tran_amount) as money)) as wartosc
  FROM [paytel_olap].[dbo].[v_rs_chargeback]
  where [date_CHB] >= @dtb AND date_CHB < @dte
  and upper(Status) like '%STRATA OPERACYJNA PAYTEL%'   -- starty jako agenta rozliczeniowego. 
  
  ---split---
  
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED


declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-2, '19000101'); --changed from -1 to -2 due to checking 2 quaters in the past
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1 , '19000101'); --changed from 0 to -1 due to checking 2 quaters in the past

  select SUM(cast(abs(tran_amount) as money)) as wartosc
  FROM [paytel_olap].[dbo].[v_rs_chargeback]
  where [date_CHB] >= @dtb AND date_CHB < @dte
  and upper(Status) like '%PRZEGRANA%'   --  straty dla merchantów/agentów/użytkownik usług płatniczych
  
  ---split---

SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED


declare @dtb as smalldatetime
declare @dte as smalldatetime

set @dtb = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-2, '19000101'); --changed from -1 to -2 due to checking 2 quaters in the past
set @dte = DATEADD(qq,DATEDIFF(QQ, '19000101', getdate())-1 , '19000101'); --changed from 0 to -1 due to checking 2 quaters in the past

  select SUM(cast(abs(tran_amount) as money)) as wartosc
  FROM [paytel_olap].[dbo].[v_rs_chargeback]
  where [date_CHB] >= @dtb AND date_CHB < @dte
  and upper(Status) like '%WYGRANA%'   -- straty posiadacza karty - czy gdzieś umieścić?

