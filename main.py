import pyodbc
import pandas as pd
from sqlalchemy import create_engine
from openpyxl.utils import get_column_letter

import shutil
import openpyxl

# Setting the connection
DRIVER_NAME = '{ODBC Driver 18 for SQL Server}'
SERVER_NAME = 'PRDBI'
DATABASE_NAME = 'paytel_olap'

EXCEL_READ = [
    'AR2',
    '4a.R.L_PLiW2',
    '4a.R.W_PLiW2',
    '5a.R.LF_PLiW2',
    '5a.R.WF_PLiW2',
    '5a.R.SF',
    '6.ab.LiW',
    '9.R.L.MCC',
    '9.R.W.MCC'
]

path = 'C:\\Users\\Krzysztof kaniewski\\Desktop\\'
df_nbp_2 = pd.read_excel(path + 'BSP_AR2_v.4.0_Q12023_20230421.xlsx', sheet_name=EXCEL_READ, header=None)

# input the personal data
d_21 = input('First name: ')
d_22 = input('Last name: ')
d_23 = input('Telephone number: ')
d_24 = input('E-mail: ')
d_31 = d_21
d_32 = d_22
d_33 = d_23
d_34 = d_24

# Choose rows based on cell in column 0:
TO_FILL = [
    'D2.1',
    'D2.2',
    'D2.3',
    'D2.4',
    'D3.1',
    'D3.2',
    'D3.3',
    'D3.4'
]

input_data = [
    d_21, d_22, d_23, d_24, d_31, d_32, d_33, d_34
]

## RETURN ROW WITH "D2.1" IN COLUMN 0 - COLUMN 5 to be edited
i = 0
for input in input_data:
    df_nbp_2[EXCEL_READ[0]].loc[df_nbp_2[EXCEL_READ[0]][0] == TO_FILL[i], 5] = input
    i += 1


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


def copy_wb(from_workbook, to_workbook, dataframe):
    # Copy the from_workbook to create a new workbook
    shutil.copyfile(from_workbook, to_workbook)

    # Load the new workbook
    wb = openpyxl.load_workbook(to_workbook)

    for sheet_name in EXCEL_READ:
        sheet = wb[sheet_name]
        for row in dataframe[sheet_name].index:
            for col in dataframe[sheet_name].columns:
                coord = get_column_letter(col + 1) + str(row + 1)
                new_value = dataframe[sheet_name].iat[row, col]

                # Handle merged cells
                for merged_range in sheet.merged_cells.ranges:
                    if coord in merged_range:
                        # Find the first cell in the merged range
                        first_cell = merged_range.min_row, merged_range.min_col
                        first_coord = get_column_letter(first_cell[1]) + str(first_cell[0])
                        # wb[sheet_name][first_coord].value = new_value
                        # not working, don't know why it is not filling the merged cels
                        break  # Exit the loop after setting the value for the merged cell
                else:
                    # If the cell is not merged, set the value directly
                    wb[sheet_name][coord].value = new_value

    # Save the updated workbook
    wb.save(to_workbook)

    if __name__ == '__main__':
        temp_table = "C:\\Users\\Krzysztof kaniewski\\Desktop\\AR2\\NBP_Temp_1.sql"
        query = "C:\\Users\\Krzysztof kaniewski\\Desktop\\AR2\\NBP_Query_1.sql"
        df = connect(temp_table, query)
