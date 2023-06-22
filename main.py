import datetime
import sys
import pandas as pd
from connect import connect, connect_single_query
from openpyxl.utils import get_column_letter

import shutil
import openpyxl
from variables import EXCEL_READ_AR2, TO_FILL, AR2_4_row_1, AR2_4_row_2, AR2_6_row_1, AR2_6_row_2, AR2_5_row_1, \
    AR2_5_row_2, \
    AR2_9_row_1, EXCEL_READ_AR1
from f_visa import f_visa_make, check_quarter
from f_mastercard import f_mastercard_make
import re

path = 'Example\\'
df_nbp_2 = pd.read_excel(path + 'BSP_AR2_v.4.0_Q12023_20230421.xlsx', sheet_name=EXCEL_READ_AR2, header=None)
df_nbp_1 = pd.read_excel(path + 'AR1 - Q1.2023.xlsx', sheet_name=EXCEL_READ_AR1, header=None)


def to_log():
    report_date = datetime.datetime.now().strftime("%Y-%m-%d")
    file_name = f'Log/{report_date}_LOG.txt'
    with open(file_name, 'a') as log:
        log.write(f"\nReport start -AR2- --{report_date}--\n")
    return file_name


def copy_wb(from_workbook, to_workbook, dataframe):
    # Copy the from_workbook to create a new workbook
    shutil.copyfile(from_workbook, to_workbook)

    # Load the new workbook
    wb = openpyxl.load_workbook(to_workbook)

    for sheet_name in EXCEL_READ_AR2:
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
                        # not working, don't know why it is not filling the merged cells
                        break  # Exit the loop after setting the value for the merged cell
                else:
                    # If the cell is not merged, set the value directly
                    wb[sheet_name][coord].value = new_value
    return wb


def load_df():
    df = []
    for n in range(22):
        df.append(pd.read_csv(f"./df/df_{n}.csv"))
    return df


def prepare_data_ar2(user, passw):
    # 4.a.R.L_PLiW2 and 4a.R.W_PLiW2 and 6.ab.LiW

    temp_table = f"Query\\AR2\\NBP_Temp_1.sql"
    query = f"Query\\AR2\\NBP_Query_1.sql"
    # dataframe_1 = connect(temp_table, query)
    dataframe_1 = load_df()  # for tests # @TODO kk - remove this after tests.

    sheet = '4a.R.L_PLiW2'

    j = 0
    i = 0
    for n in range(0, 20):
        for country in dataframe_1[n]['name']:
            if country == 'Holandia':
                country = 'Niderlandy'
            if i <= 19:
                col = pd.Index(df_nbp_2[sheet].iloc[7]).get_loc(country)
                df_nbp_2[sheet][col].iloc[AR2_4_row_1[j]] = dataframe_1[n]['ilosc'].iloc[i]
            i += 1
        i = 0
        j += 1

    sheet = '4a.R.W_PLiW2'

    j = 0
    i = 0
    for n in range(0, 20):

        for country in dataframe_1[n]['name']:
            if country == 'Holandia':
                country = 'Niderlandy'
            if i <= 19:
                col = pd.Index(df_nbp_2[sheet].iloc[7]).get_loc(country)
                df_nbp_2[sheet][col].iloc[AR2_4_row_2[j]] = dataframe_1[n]['wartosc'].iloc[i]
            i += 1
        i = 0
        j += 1

    sheet = EXCEL_READ_AR2[6]
    for j in range(1):
        df_nbp_2[sheet][34].iloc[AR2_6_row_1[j]] = dataframe_1[20]['ilosc'].iloc[0]
        df_nbp_2[sheet][34].iloc[AR2_6_row_2[j]] = dataframe_1[21]['wartosc'].iloc[0]

    # 5a.R.SF

    temp_table = f"Query\\AR2\\NBP_Temp_3.sql"
    query = f"Query\\AR2\\NBP_Query_3.sql"
    dataframe_3 = connect(temp_table, query)

    sheet = '5a.R.SF'
    df_nbp_2[sheet][3].iloc[8] = dataframe_3[2]['wartosc'].iloc[0]
    df_nbp_2[sheet][3].iloc[9] = dataframe_3[3]['wartosc'].iloc[0]
    df_nbp_2[sheet][3].iloc[10] = dataframe_3[4]['wartosc'].iloc[0]

    # 5a.R.LF_PLiW2 and 5a.R.WF_PLiW2

    # Get the Visa
    data_visa = f_visa_make(user, passw)
    df_visa = pd.DataFrame(data_visa[0])
    # Get the Mastercard
    data_mastercard = f_mastercard_make()
    df_mastercard = pd.DataFrame(data_mastercard[0])
    df_complete = [df_visa, df_mastercard]
    df_fraud = pd.concat(df_complete)
    # Use extracted ARNs for query
    with open("./Query/AR2/NBP_Temp_2.sql", 'r',
              encoding='utf-8') as sql:
        sql = sql.read()
        pattern = '--insert'
        insert_start = [match.start() for match in re.finditer(pattern, sql)]
        mastercard_insert = [insert_start[0], insert_start[0] + len(pattern)]
        visa_insert = [insert_start[1], insert_start[1] + len(pattern)]

        sql = sql[:visa_insert[0]] + data_visa[1] + sql[visa_insert[1]:]
        sql = sql[:mastercard_insert[0]] + data_mastercard[1] + sql[mastercard_insert[1]:]

    with open("./Query/AR2/NBP_Temp_2_filled.sql", 'w',
              encoding='utf-8') as sql_w:
        sql_w.write(sql)

    temp_table = f"Query\\AR2\\NBP_Temp_2_filled.sql"
    query = f"Query\\AR2\\NBP_Query_2.sql"
    dataframe_2 = connect(temp_table, query)

    sheet = '5a.R.LF_PLiW2'

    j = 0
    i = 0
    for n in range(0, len(dataframe_2)):
        for country in dataframe_2[n]['code']:
            col = pd.Index(df_nbp_2[sheet].iloc[6]).get_loc(country)
            df_nbp_2[sheet][col].iloc[AR2_5_row_1[j]] = dataframe_2[n]['ilosc'].iloc[i]
            i += 1
        i = 0
        j += 1

    sheet = '5a.R.WF_PLiW2'

    j = 0
    i = 0
    for n in range(0, len(dataframe_2)):
        for country in dataframe_2[n]['code']:
            col = pd.Index(df_nbp_2[sheet].iloc[6]).get_loc(country)
            df_nbp_2[sheet][col].iloc[AR2_5_row_2[j]] = dataframe_2[n]['wartosc'].iloc[i]
            i += 1
        i = 0
        j += 1

    # for k in range(len(dataframe_2)):
    #     dataframe_2[k].to_csv(f'df_5_{k}.csv')

    # Make pivot table
    df_fraud['country_aggr'] = df_fraud['country'].apply(lambda c: aggr_country(c))
    df_fraud.to_csv('df_fraud.csv')
    print('Checking the quarter: ' + str(check_quarter()[3]))
    df_f_data = pd.pivot_table(index='pos_entry_mode', columns='country_aggr',
                               data=df_fraud[df_fraud['quarter'] == check_quarter()[3]],
                               aggfunc={'tr_amout': 'sum', 'country_aggr': 'count'}, fill_value=0)

    # 9.R.L.MCC and 9.R.W.MCC

    temp_table = f"Query\\AR2\\NBP_Temp_4.sql"
    query = f"Query\\AR2\\NBP_Query_4.sql"
    dataframe_4 = connect(temp_table, query)

    sheet = '9.R.L.MCC'

    for n in range(0, len(dataframe_4)):
        print(n)
        for country in dataframe_4[n]['name']:
            # last dataframe retrieved from database is different so if n=3 then execute different algorithm
            if n < 3:
                col = pd.Index(df_nbp_2[sheet].iloc[7]).get_loc(country)
                df_nbp_2[sheet][col].iloc[AR2_9_row_1[n]] = dataframe_4[n]['ilosc'].iloc[i]
            if n == 3:
                # Convert df_nbp_2[1] column to string
                df_nbp_2[sheet][1] = df_nbp_2[sheet][1].astype(str)
                mcc = dataframe_4[n]['mcc'].iloc[i]
                col = pd.Index(df_nbp_2[sheet].iloc[7]).get_loc(country)
                ind = df_nbp_2[sheet][df_nbp_2[sheet][1] == mcc].index[0]
                df_nbp_2[sheet].iat[ind, col] = dataframe_4[n]['ilosc'].iloc[i]
            i += 1
        i = 0
        j += 1

    sheet = '9.R.W.MCC'

    for n in range(0, len(dataframe_4)):
        print(n)
        for country in dataframe_4[n]['name']:
            # last dataframe retrieved from database is different so if n=3 then execute different algorithm
            if n < 3:
                col = pd.Index(df_nbp_2[sheet].iloc[7]).get_loc(country)
                df_nbp_2[sheet][col].iloc[AR2_9_row_1[n]] = dataframe_4[n]['wartosc_transakcji'].iloc[i]
            if n == 3:
                # Convert df_nbp_2[1] column to string
                df_nbp_2[sheet][1] = df_nbp_2[sheet][1].astype(str)
                mcc = dataframe_4[n]['mcc'].iloc[i]
                col = pd.Index(df_nbp_2[sheet].iloc[7]).get_loc(country)
                ind = df_nbp_2[sheet][df_nbp_2[sheet][1] == mcc].index[0]
                df_nbp_2[sheet].iat[ind, col] = dataframe_4[n]['wartosc_transakcji'].iloc[i]
            i += 1
        i = 0
        j += 1


def aggr_country(c):
    if c == 'PL':
        return 'PL'
    else:
        return 'NPL'


class Logger(object):
    def __init__(self, log_file):
        self.terminal = sys.stdout
        self.log_file = log_file

    def write(self, message):
        self.terminal.write(message)
        self.log_file.write(message)

    def flush(self):
        self.terminal.flush()
        self.log_file.flush()


def prepare_data_ar1():
    # ST.01

    temp_table = f"Query\\AR1\\NBP_Temp_1.sql"
    query = f"Query\\AR1\\NBP_Query_1.sql"
    dataframe_1 = connect(temp_table, query)

    i = 0
    for df in dataframe_1:
        df.to_csv(f'ST.01.{i}.csv')
        i += 1

    # ST.05

    temp_table = f"Query\\AR1\\NBP_Temp_2.sql"
    query = f"Query\\AR1\\NBP_Query_2.sql"
    dataframe_2 = connect(temp_table, query)

    i = 0
    for df in dataframe_2:
        df.to_csv(f'ST.05.{i}.csv')
        i += 1

    # ST.06

    temp_table = f"Query\\AR1\\NBP_Temp_3.sql"
    query = f"Query\\AR1\\NBP_Query_3.sql"
    dataframe_3 = connect(temp_table, query)

    i = 0
    for df in dataframe_3:
        df.to_csv(f'ST.06.{i}.csv')
        i += 1

    # ST.02

    # ST.07

    temp_table = f"Query\\AR1\\NBP_Temp_4.sql"
    query = f"Query\\AR1\\NBP_Query_4.sql"
    dataframe_4 = connect(temp_table, query)

    i = 0
    for df in dataframe_4:
        df.to_csv(f'ST.07.{i}.csv')
        i += 1

if __name__ == '__main__':
    # Open the log file in append mode
    log_file = open(to_log(), "a")
    # Create the logger object
    logger = Logger(log_file)
    # Assign the logger as the new sys.stdout
    sys.stdout = logger

    # AR2 sheet for NBP
    # Fill the first sheet with "Author of the report" info.
    # input the personal data
    d_21 = input('First name: ')
    d_22 = input('Last name: ')
    d_23 = input('Telephone number: ')
    d_24 = input('E-mail: ')
    d_31 = d_21
    d_32 = d_22
    d_33 = d_23
    d_34 = d_24
    user = 'PAYTEL\\Krzysztof Kaniewski'  # 'PAYTEL\\' + input("your_username: ")   # @TODO: kk - change later
    passw = 'Xl2Km0oPYahPagh6'  # input("your_password: ")  # @TODO - kk: Modify to hide sensitive data

    input_data = [
        d_21, d_22, d_23, d_24, d_31, d_32, d_33, d_34
    ]

    # RETURN ROW WITH "D2.1" IN COLUMN 0 - COLUMN 5 to be edited
    i = 0
    for inp in input_data:
        df_nbp_2[EXCEL_READ_AR2[0]].loc[df_nbp_2[EXCEL_READ_AR2[0]][0] == TO_FILL[i], 5] = inp
        i += 1

    # Fill sheets in AR2
    prepare_data_ar2(user, passw)

    # Save everything to new excel file
    from_wb = path + 'BSP_AR2_v.4.0_Q12023_20230421.xlsx'
    to_wb = path + f'Filled\\' + f'BSP_AR2_v.4.0_Q{check_quarter()[3]}{datetime.date.today().strftime("%Y")}_{datetime.date.today().strftime("%Y%m%d")}.xlsx'

    wb = copy_wb(from_wb, to_wb, df_nbp_2)

    # Save the updated workbook
    wb.save(to_wb)

    # Fill sheets in AR1
    prepare_data_ar1()

    # Save everything to new excel file
    from_wb = path + 'AR1 - Q1.2023'
    to_wb = path + f'Filled\\' + f'AR1 - Q{check_quarter()[3]}.{datetime.date.today().strftime("%Y")}'

    wb = copy_wb(from_wb, to_wb, df_nbp_1)

    # Save the updated workbook
    wb.save(to_wb)

    # Close the log file
    log_file.close()
