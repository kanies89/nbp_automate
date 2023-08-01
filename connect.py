import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pyodbc

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

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # split the code to get individual query for retrieving the data for dataframes
        t_list = temp_table.split('---split---')

        for t in t_list:
            session.execute(text(str(t)))

        # split the code to get individual query for retrieving the data for dataframes
        q_list = query.split('---split---')
        df_list = []

        for q in q_list:
            result = session.execute(text(str(q)))
            data = result.fetchall()
            df = pd.DataFrame(data, columns=result.keys())
            df_list.append(df)

        session.commit()
        return df_list
    except:
        session.rollback()
        raise
    finally:
        session.close()
        engine.dispose()


def connect_single_query(query):
    engine = create_engine(
        'mssql+pyodbc://@' + SERVER_NAME + '/' + DATABASE_NAME + '?trusted_connection=yes&driver=ODBC+Driver+18+for+SQL+Server&encrypt=no')

    with engine.connect() as connection:
        connection.echo = False

        q_list = query.split('---split---')

        df = []

        for q in q_list:
            tableResult = pd.read_sql(f'{q}', connection)
            df.append(pd.DataFrame(tableResult))

    engine.dispose()

    return df
