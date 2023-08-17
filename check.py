from variables import EXCEL_READ_AR2
import pandas as pd


# PCP_090
def rule_1(dataframe, sheet_number, column_in_app):
    print("HERE")
    results = []
    sheet = EXCEL_READ_AR2[sheet_number]
    try:
        row_f = pd.Index(dataframe[sheet][0]).get_loc("8.")
    except KeyError:
        print("Row - 8. - not found")
    try:
        row_s_1 = pd.Index(dataframe[sheet][0]).get_loc("8.1.1")
    except KeyError:
        print("Row - 8.1.1 - not found")
    try:
        row_s_2 = pd.Index(dataframe[sheet][0]).get_loc("8.1.2")
    except KeyError:
        print("Row - 8.1.2 - not found")
    columns_number = dataframe[sheet].shape[1]

    for c in range(columns_number):
        print(c)
        first_part = dataframe[sheet].iat[row_f, c]
        second_part = dataframe[sheet].iat[row_s_1, c] + dataframe[sheet].iat[row_s_2, c]

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])

    return results
