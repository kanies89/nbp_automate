import pandas as pd
from connect import connect
from openpyxl.utils import get_column_letter

import shutil
import openpyxl
from variables import EXCEL_READ, TO_FILL, AR2_4_row_1, AR2_4_row_2, AR2_6_row_1, AR2_6_row_2

path = 'Example\\'
df_nbp_2 = pd.read_excel(path + 'BSP_AR2_v.4.0_Q12023_20230421.xlsx', sheet_name=EXCEL_READ, header=None)


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
    return wb


def load_df():
    df = []
    for n in range(22):
        df.append(pd.read_csv(f"./df/df_{n}.csv"))
    return df


def prepare_data():
    # 4.a.R.L_PLiW2 and 4a.R.W_PLiW2 and 6.ab.LiW

    temp_table = f"Query\\AR2\\NBP_Temp_1.sql"
    query = f"Query\\AR2\\NBP_Query_1.sql"
    # dataframe_1 = connect(temp_table, query)
    dataframe_1 = load_df()  # for tests

    sheet = '4a.R.L_PLiW2'
    
    j = 0
    i = 0
    for n in range(0, 20):
        print(dataframe_1[n].columns)
        for country in dataframe_1[n]['name']:
            if country == 'Holandia':
                country = 'Niderlandy'
            print('I', i)
            print(country)
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
            print('W', i)
            print(country)
            if i <= 19:
                col = pd.Index(df_nbp_2[sheet].iloc[7]).get_loc(country)
                df_nbp_2[sheet][col].iloc[AR2_4_row_2[j]] = dataframe_1[n]['wartosc'].iloc[i]
            i += 1
        i = 0
        j += 1

    sheet = EXCEL_READ[6]
    for j in range(1):
        df_nbp_2[sheet][34].iloc[AR2_6_row_1[j]] = dataframe_1[20]['ilosc'].iloc[0]
        df_nbp_2[sheet][34].iloc[AR2_6_row_2[j]] = dataframe_1[21]['wartosc'].iloc[0]

    # 5a.R

    temp_table = f"Query\\AR2\\NBP_Temp_3.sql"
    query = f"Query\\AR2\\NBP_Query_3.sql"
    dataframe_3 = connect(temp_table, query)

    sheet = '5a.R.SF'
    df_nbp_2[sheet][3].iloc[8] = dataframe_3[2]['wartosc'].iloc[0]
    df_nbp_2[sheet][3].iloc[9] = dataframe_3[3]['wartosc'].iloc[0]
    df_nbp_2[sheet][3].iloc[10] = dataframe_3[4]['wartosc'].iloc[0]
    print("finished")

    # 9.R.L.MCC and 9.R.W.MCC

    temp_table = f"Query\\AR2\\NBP_Temp_4.sql"
    query = f"Query\\AR2\\NBP_Query_4.sql"
    # dataframe_4 = connect(temp_table, query)


if __name__ == '__main__':
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

    input_data = [
        d_21, d_22, d_23, d_24, d_31, d_32, d_33, d_34
    ]

    # RETURN ROW WITH "D2.1" IN COLUMN 0 - COLUMN 5 to be edited
    i = 0
    for inp in input_data:
        df_nbp_2[EXCEL_READ[0]].loc[df_nbp_2[EXCEL_READ[0]][0] == TO_FILL[i], 5] = inp
        i += 1

    # Fill sheets 4.a.R.L_PLiW2 and 4a.R.W_PLiW2 and 6.ab.LiW and 5a.R
    prepare_data()

    # Save everything to new excel file
    from_wb = path + 'BSP_AR2_v.4.0_Q12023_20230421.xlsx'
    to_wb = path + 'Filled\\' + 'BSP_AR2_v.4.0_Q12023_20230421.xlsx'
    wb = copy_wb(from_wb, to_wb, df_nbp_2)

    # Save the updated workbook
    wb.save(to_wb)
