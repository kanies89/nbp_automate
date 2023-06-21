from connect import connect

temp_table = f"Query\\AR2\\NBP_Temp_4.sql"
query = f"Query\\AR2\\NBP_Query_4.sql"
dataframe_4 = connect(temp_table, query)
for k in range(len(dataframe_4)):
    dataframe_4[k].to_csv(f'df_9_{k}.csv')


