import pandas as pd
from sqlalchemy import create_engine

# Setting the connection
DRIVER_NAME = '{ODBC Driver 18 for SQL Server}'
SERVER_NAME = 'PRDBI'
DATABASE_NAME = 'paytel_olap'


def connect(temp_table_file, query_file):
    with open(temp_table_file, 'r', encoding='utf-8') as file:
        temp_table = file.read()  # Read the SQL query from the file

    with open(query_file, 'r', encoding='utf-8') as file:
        query = file.read()  # Read the SQL query from the file

    engine = create_engine(
        'mssql+pyodbc://@' + SERVER_NAME + '/' + DATABASE_NAME + '?trusted_connection=yes&driver=ODBC+Driver+18+for+SQL+Server&encrypt=no')

    with engine.connect() as connection:
        connection.echo = False

        connection.execute(temp_table)
        q_list = query.split('---split---')
        df = []

        for q in q_list:
            tableResult = pd.read_sql(q, connection)
            df.append(pd.DataFrame(tableResult))

    engine.dispose()

    return df


def connect_single_query(query):
    engine = create_engine(
        'mssql+pyodbc://@' + SERVER_NAME + '/' + DATABASE_NAME + '?trusted_connection=yes&driver=ODBC+Driver+18+for+SQL+Server&encrypt=no')

    with engine.connect() as connection:
        connection.echo = False

        q_list = query.split('---split---')

        df = []

        for q in q_list:
            tableResult = pd.read_sql(q, connection)
            df.append(pd.DataFrame(tableResult))

    engine.dispose()

    return df
