import pandas as pd

AR2_TO_CHECK = [
    'AR2',
    '4a.LiW',
    '4a.R.L_PLiW2',
    '4a.R.L_krajGEO3',
    '4a.R.W_PLiW2',
    '4a.R.W_krajGEO3',
    '5a.R.LF_PLiW2',
    '5a.R.LF_krajGEO3',
    '5a.R.WF_PLiW2',
    '5a.R.WF_krajGEO3',
    '5a.R.SF',
    '6.ab.LiW',
    '9.R.L.MCC',
    '9.R.W.MCC'
]

AR1_TO_CHECK = [
    'ST.01',
    'ST.02',
    'ST.03',
    'ST.04',
    'ST.05',
    'ST.06',
    'ST.07'
]


# PCP_090
def rule_1_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]
    try:
        row_f = df[df.iloc[:, 0] == "8"].index[0]
    except KeyError:
        print("Row - 8 - not found")
    try:
        row_s_1 = df[df.iloc[:, 0] == "8.1.1"].index[0]
    except KeyError:
        print("Row - 8.1.1 - not found")
    try:
        row_s_2 = df[df.iloc[:, 0] == "8.1.2"].index[0]
    except KeyError:
        print("Row - 8.1.2 - not found")
    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum = 0

        first_part = round(to_float(dataframe[sheet].iat[row_f, c]), 2)

        value_1 = to_float(dataframe[sheet].iat[row_s_1, c])
        value_1 = round(value_1, 2)
        value_2 = to_float(dataframe[sheet].iat[row_s_2, c])
        value_2 = round(value_2, 2)
        value_sum += value_1 + value_2

        second_part = round(value_sum, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print("1: ", first_part, '!=', second_part)

    return results


# PCP_091
def rule_2_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        row_f = df[df.iloc[:, 0] == "8.1.1"].index[0]
    except KeyError:
        print("Row - 8. - not found")

    try:
        row_s_1 = df[df.iloc[:, 0] == "8.1.1.1"].index[0]
    except KeyError:
        print("Row - 8.1.1.1 - not found")

    try:
        row_s_2 = df[df.iloc[:, 0] == "8.1.1.2"].index[0]
    except KeyError:
        print("Row - 8.1.1.2 - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum = 0

        first_part = round(to_float(dataframe[sheet].iat[row_f, c]), 2)

        value_1 = to_float(dataframe[sheet].iat[row_s_1, c])
        value_1 = round(value_1, 2)
        value_2 = to_float(dataframe[sheet].iat[row_s_2, c])
        value_2 = round(value_2, 2)
        value_sum += value_1 + value_2

        second_part = round(value_sum, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print("2: ", first_part, '!=', second_part)

    return results


# PCP_092
def rule_3_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        row_f = df[df.iloc[:, 0] == "8.1.2"].index[0]
    except KeyError:
        print("Row - 8.1.2 - not found")

    try:
        row_s_1 = df[df.iloc[:, 0] == "8.1.2.1"].index[0]
    except KeyError:
        print("Row - 8.1.2.1 - not found")

    try:
        row_s_2 = df[df.iloc[:, 0] == "8.1.2.2"].index[0]
    except KeyError:
        print("Row - 8.1.2.2 - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum = 0

        first_part = round(to_float(dataframe[sheet].iat[row_f, c]), 2)

        value_1 = to_float(dataframe[sheet].iat[row_s_1, c])
        value_1 = round(value_1, 2)
        value_2 = to_float(dataframe[sheet].iat[row_s_2, c])
        value_2 = round(value_2, 2)
        value_sum += value_1 + value_2

        second_part = round(value_sum, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print("3: ", first_part, '!=', second_part)

    return results


# PCP_093
def rule_4_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        row_f = df[df.iloc[:, 0] == "8.1.2.1"].index[0]
    except KeyError:
        print("Row - 8.1.2.1 - not found")

    try:
        rows = []
        for i in range(1, 4):
            condition = df.iloc[:, 0] == f"8.1.2.1.1.{i}"
            index = condition[condition].index[0]
            rows.append(index)

    except KeyError:
        print(f"Row - 8.1.2.1.1.{i} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        first_part = round(to_float(dataframe[sheet].iat[row_f, c]), 2)

        value_sum = 0
        for i in range(len(rows)):
            value = to_float(dataframe[sheet].iat[rows[i], c])
            value = round(value, 2)
            value_sum += value
        second_part = round(value_sum, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print("4: ", first_part, '!=', second_part)

    return results


# PCP_094
def rule_5_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        row_f = df[df.iloc[:, 0] == "8.1.2.1"].index[0]
    except KeyError:
        print("Row - 8.1.2.1 - not found")

    try:
        rows = []
        for i in range(1, 10):
            condition = df.iloc[:, 0] == f"8.1.2.1.2.{i}"
            index = condition[condition].index[0]
            rows.append(index)

    except KeyError:
        print(f"Row - 8.1.2.1.2.{i} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        first_part = round(to_float(dataframe[sheet].iat[row_f, c]), 2)

        value_sum = 0
        for i in range(len(rows)):
            value = to_float(dataframe[sheet].iat[rows[i], c])
            value = round(value, 2)
            value_sum += value
        second_part = round(value_sum, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print("5: ", first_part, '!=', second_part)

    return results


# PCP_096
def rule_6_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []
        for i in range(1, 10):
            condition = df.iloc[:, 0] == f"8.1.2.1.2.{i}"
            index = condition[condition].index[0]
            rows_1.append(index)

    except KeyError:
        print(f"Row - 8.1.2.1.2.{i} - not found")

    try:
        rows_2 = []
        for i in range(1, 10):
            for j in range(1, 4):
                condition = df.iloc[:, 0] == f"8.1.2.1.2.{i}.1.{j}"
                index = condition[condition].index[0]
                rows_2.append(index)

    except KeyError:
        print(f"Row - 8.1.2.1.2.{i}.1.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_1 = to_float(dataframe[sheet].iat[rows_1[i], c])
            value_1 = round(value_1, 2)
            value_sum_1 += value_1

        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_2 = to_float(dataframe[sheet].iat[rows_2[i], c])
            value_2 = round(value_2, 2)
            value_sum_2 += value_2

        second_part = round(value_sum_2, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print("6: ", first_part, '!=', second_part)

    return results


# PCP_099
def rule_7_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        i = 1
        rows_1 = []
        condition = df.iloc[:, 0] == f"8.1.2.1.2.{i}"
        index = condition[condition].index[0]
        rows_1.append(index)

    except KeyError:
        print(f"Row - 8.1.2.1.2.{i} - not found")

    try:
        rows_2 = []
        i = 1
        for j in range(1, 3):
            condition = df.iloc[:, 0] == f"8.1.2.1.2.{i}.2.{j}"
            index = condition[condition].index[0]
            rows_2.append(index)

    except KeyError:
        print(f"Row - 8.1.2.1.2.{i}.2.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print("7: ", first_part, '!=', second_part)

    return results


# PCP_006
def rule_8_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []
        for i in range(1, 10):
            condition = df.iloc[:, 0] == f"8.1.2.1.2.{i}.2.2"
            index = condition[condition].index[0]
            rows_1.append(index)

    except KeyError:
        print(f"Row - 8.1.2.1.2.{i}.2.2 - not found")

    try:
        rows_2 = []
        for j in range(2, 6):
            condition = df.iloc[:, 0] == f"8.1.2.1.3.{j}"
            index = condition[condition].index[0]
            rows_2.append(index)

    except KeyError:
        print(f"Row - 8.1.2.1.3.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print("8: ", first_part, '!=', second_part)

    return results


# PCP_095
def rule_9_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []

        condition = df.iloc[:, 0] == f"8.1.2.2"
        index = condition[condition].index[0]
        rows_1.append(index)

    except KeyError:
        print(f"Row - 8.1.2.2 - not found")

    try:
        rows_2 = []
        for i in range(1, 10):
            condition = df.iloc[:, 0] == f"8.1.2.2.2.{i}"
            index = condition[condition].index[0]
            rows_2.append(index)

    except KeyError:
        print(f"Row - 8.1.2.2.2.{i} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print("9: ", first_part, '!=', second_part)

    return results


# PCP_102
def rule_10_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []
        i = 1
        condition = df.iloc[:, 0] == f"8.1.2.2.2.{i}"
        index = condition[condition].index[0]
        rows_1.append(index)

    except KeyError:
        print(f"Row - 8.1.2.2.2.{i} - not found")

    try:
        i = 1
        rows_2 = []
        for j in range(1, 4):
            condition = df.iloc[:, 0] == f"8.1.2.2.2.{i}.1.{j}"
            index = condition[condition].index[0]
            rows_2.append(index)

    except KeyError:
        print(f"Row - 8.1.2.2.2.{i}.1.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print("10: ", first_part, '!=', second_part)

    return results


# PCP_105
def rule_11_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []
        i = 1
        condition = df.iloc[:, 0] == f"8.1.2.2.2.{i}"
        index = condition[condition].index[0]
        rows_1.append(index)

    except KeyError:
        print(f"Row - 8.1.2.2.2.{i} - not found")

    try:
        i = 1
        rows_2 = []
        for j in range(1, 3):
            condition = df.iloc[:, 0] == f"8.1.2.2.2.{i}.2.{j}"
            index = condition[condition].index[0]
            rows_2.append(index)

    except KeyError:
        print(f"Row - 8.1.2.2.2.{i}.2.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print("11: ", first_part, '!=', second_part)

    return results


# PCP_007
def rule_12_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []
        for i in range(1, 10):
            condition = df.iloc[:, 0] == f"8.1.2.2.2.{i}.2.2"
            index = condition[condition].index[0]
            rows_1.append(index)

    except KeyError:
        print(f"Row - 8.1.2.2.2.{i}.2.2 - not found")

    try:
        rows_2 = []

        for j in [2, 3, 5, 6, 7]:
            condition = df.iloc[:, 0] == f"8.1.2.2.3.{j}"
            index = condition[condition].index[0]
            rows_2.append(index)

    except KeyError:
        print(f"Row - 8.1.2.2.3.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print("12: ", first_part, '!=', second_part)

    return results


# PCP_108
def rule_13_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []
        for i in range(1, 10):
            condition = df.iloc[:, 0] == f"8.1.2.1.2.{i}.2.1"
            index = condition[condition].index[0]
            rows_1.append(index)

    except KeyError:
        print(f"Row - 8.1.2.1.2.{i}.2.1 - not found")

    try:
        rows_2 = []
        for i in range(1, 10):
            for j in range(1, 4):
                condition = df.iloc[:, 0] == f"8.1.2.1.2.{i}.2.1.{j}"
                index = condition[condition].index[0]
                rows_2.append(index)

    except KeyError:
        print(f"Row - 8.1.2.1.2.{i}.2.1.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print("13: ", first_part, '!=', second_part)

    return results


# PCP_120
def rule_14_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []
        i = 1
        condition = df.iloc[:, 0] == f"8.1.2.1.2.{i}.2.1.1"
        index = condition[condition].index[0]
        rows_1.append(index)

    except KeyError:
        print(f"Row - 8.1.2.1.2.{i}.2.1 - not found")

    try:
        rows_2 = []
        i = 1
        for j in range(1, 5):
            condition = df.iloc[:, 0] == f"8.1.2.1.2.{i}.2.1.1.{j}"
            index = condition[condition].index[0]
            rows_2.append(index)

    except KeyError:
        print(f"Row - 8.1.2.1.2.{i}.2.1.1.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print("14: ", first_part, '!=', second_part)

    return results


# PCP_109
def rule_15_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []
        i = 1
        condition = df.iloc[:, 0] == f"8.1.2.1.2.{i}.2.2"
        index = condition[condition].index[0]
        rows_1.append(index)

    except KeyError:
        print(f"Row - 8.1.2.1.2.{i}.2.2 - not found")

    try:
        rows_2 = []
        i = 1
        for j in range(1, 4):
            condition = df.iloc[:, 0] == f"8.1.2.1.2.{i}.2.2.{j}"
            index = condition[condition].index[0]
            rows_2.append(index)

    except KeyError:
        print(f"Row - 8.1.2.1.2.{i}.2.1.1.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print(first_part, '!=', second_part)

    return results


# PCP_121
def rule_16_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []
        i = 1
        condition = df.iloc[:, 0] == f"8.1.2.1.2.{i}.2.2.1"
        index = condition[condition].index[0]
        rows_1.append(index)

    except KeyError:
        print(f"Row - 8.1.2.1.2.{i}.2.1 - not found")

    try:
        rows_2 = []
        i = 1
        for j in range(1, 5):
            condition = df.iloc[:, 0] == f"8.1.2.1.2.{i}.2.2.1.{j}"
            index = condition[condition].index[0]
            rows_2.append(index)

    except KeyError:
        print(f"Row - 8.1.2.1.2.{i}.2.1.1.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print(first_part, '!=', second_part)

    return results


# PCP_110
def rule_17_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []
        i = 1
        condition = df.iloc[:, 0] == f"8.1.2.2.2.{i}.2.1"
        index = condition[condition].index[0]
        rows_1.append(index)

    except KeyError:
        print(f"Row - 8.1.2.2.2.{i}.2.1 - not found")

    try:
        rows_2 = []
        i = 1
        for j in range(1, 4):
            condition = df.iloc[:, 0] == f"8.1.2.2.2.{i}.2.1.{j}"
            index = condition[condition].index[0]
            rows_2.append(index)

    except KeyError:
        print(f"Row - 8.1.2.2.2.{i}.2.1.1.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print(first_part, '!=', second_part)

    return results


# PCP_122
def rule_18_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []
        i = 1
        condition = df.iloc[:, 0] == f"8.1.2.2.2.{i}.2.1.1"
        index = condition[condition].index[0]
        rows_1.append(index)

    except KeyError:
        print(f"Row - 8.1.2.2.2.{i}.2.1.1 - not found")

    try:
        rows_2 = []
        i = 1
        for j in range(1, 6):
            condition = df.iloc[:, 0] == f"8.1.2.2.2.{i}.2.1.1.{j}"
            index = condition[condition].index[0]
            rows_2.append(index)

    except KeyError:
        print(f"Row - 8.1.2.2.2.{i}.2.1.1.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print(first_part, '!=', second_part)

    return results


# PCP_111
def rule_19_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []
        i = 1
        condition = df.iloc[:, 0] == f"8.1.2.2.2.{i}.2.2"
        index = condition[condition].index[0]
        rows_1.append(index)

    except KeyError:
        print(f"Row - 8.1.2.2.2.{i}.2.2 - not found")

    try:
        rows_2 = []
        i = 1
        for j in range(1, 4):
            condition = df.iloc[:, 0] == f"8.1.2.2.2.{i}.2.2.{j}"
            index = condition[condition].index[0]
            rows_2.append(index)

    except KeyError:
        print(f"Row - 8.1.2.2.2.{i}.2.2.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print(first_part, '!=', second_part)

    return results


# PCP_123
def rule_20_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []
        i = 1
        condition = df.iloc[:, 0] == f"8.1.2.2.2.{i}.2.2.1"
        index = condition[condition].index[0]
        rows_1.append(index)

    except KeyError:
        print(f"Row - 8.1.2.2.2.{i}.2.2.1 - not found")

    try:
        rows_2 = []
        i = 1
        for j in range(1, 6):
            condition = df.iloc[:, 0] == f"8.1.2.2.2.{i}.2.2.1.{j}"
            index = condition[condition].index[0]
            rows_2.append(index)

    except KeyError:
        print(f"Row - 8.1.2.2.2.{i}.2.2.1.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print(first_part, '!=', second_part)

    return results


# PCP_245_R
def rule_21_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []
        condition = df.iloc[:, 0] == "9.1"
        index = condition[condition].index[0]
        rows_1.append(index)

    except KeyError:
        print(f"Row - 9.1 - not found")

    try:
        rows_2 = []
        for j in range(1, 3):
            condition = df.iloc[:, 0] == f"9.1.{j}"
            index = condition[condition].index[0]
            rows_2.append(index)

    except KeyError:
        print(f"Row - 9.1.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part == second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print(first_part, '!=', second_part)

    return results


# DSDs_040_R
def rule_22_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []
        condition = df.iloc[:, 0] == "9.1.1"
        index = condition[condition].index[0]
        rows_1.append(index)

    except KeyError:
        print(f"Row - 9.1.1 - not found")

    try:
        rows_2 = []
        for j in range(742, 1077):
            condition = df.iloc[:, 0] == f"9.1.1.{j}"
            index = condition[condition].index[0]
            rows_2.append(index)

    except KeyError:
        print(f"Row - 9.1.1.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part >= second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print(first_part, '!=', second_part)

    return results


# DSDs_038_R
def rule_23_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]

    try:
        rows_1 = []
        condition = df.iloc[:, 0] == "9.1.2"
        index = condition[condition].index[0]
        rows_1.append(index)

    except KeyError:
        print(f"Row - 9.1.2 - not found")

    try:
        rows_2 = []
        for j in range(742, 1077):
            condition = df.iloc[:, 0] == f"9.1.2.{j}"
            index = condition[condition].index[0]
            rows_2.append(index)

    except KeyError:
        print(f"Row - 9.1.1.{j} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

        if first_part >= second_part:
            results.append([sheet, True])
        else:
            results.append([sheet, False, c])
            print(first_part, '!=', second_part)

    return results


GEO3 = [
    'AT',
    'BE',
    'BG',
    'HR',
    'CY',
    'CZ',
    'DK',
    'EE',
    'FI',
    'FR',
    'GR',
    'ES',
    'NL',
    'IE',
    'IS',
    'LT',
    'LI',
    'LU',
    'LV',
    'MT',
    'DE',
    'NO',
    'PT',
    'RO',
    'SK',
    'SI',
    'SE',
    'HU',
    'IT',
    'W2'
]


# PCP_031_R
def rule_24_ar2(dataframe, sheet_number):
    if sheet_number == 12:
        check_sheets = [2, 3]
    else:
        check_sheets = [4, 5]

    first_part = []
    second_part = []

    results = []
    value_sum_1 = []
    sheet = AR2_TO_CHECK[sheet_number]

    for country in GEO3:
        ind = dataframe[sheet].loc[6] == country
        col_index = ind[ind].index[0]
        print(country, col_index)

        get_value = dataframe[sheet].iat[9, col_index]
        value = to_float(get_value)
        value = round(value, 2)
        value_sum_1.append(to_float(value))

    for i, value in enumerate(value_sum_1):
        value_sum_1[i] = round(value, 2)
        first_part.append(value_sum_1[i])

    value_sum_2 = []
    sheet = AR2_TO_CHECK[check_sheets[0]]

    for country in GEO3:
        ind = dataframe[sheet].loc[6] == country
        print(country)
        col_index = ind[ind].index[0]
        print(col_index)

        get_value = dataframe[sheet].iat[9, col_index]
        value = to_float(get_value)
        value = round(value, 2)
        value_sum_2.append(to_float(value))

    sheet = AR2_TO_CHECK[check_sheets[1]]

    for n, country in enumerate(GEO3):
        if sheet == '4a.R.L_krajGEO3':
            ind = dataframe[sheet].loc[7] == country
        else:
            ind = dataframe[sheet].loc[6] == country
        print(sheet)
        print(country)
        col_index = ind[ind].index[0]
        print(col_index)

        get_value = dataframe[sheet].iat[9, col_index]
        value = to_float(get_value)
        value = round(value, 2)
        value_sum_2[n] += to_float(value)

    for i, value in enumerate(value_sum_2):
        value_sum_2[i] = round(value, 2)
        second_part.append(value_sum_2[i])

    for n, country in enumerate(GEO3):
        if first_part[n] == second_part[n]:
            results.append([sheet, True])
        else:
            results.append([sheet, False, country])
            print("24: ", first_part[n], '!=', second_part[n])

    return results


# W_008
def rule_26_ar2(dataframe, sheet_number):
    results = []
    sheet = AR2_TO_CHECK[sheet_number]

    df = dataframe[sheet]
    print(sheet)
    try:
        rows_1 = []
        condition = df.iloc[:, 0] == 9
        print(df.iat[9, 0])
        print(condition[9])
        index = condition[condition].index[0]
        rows_1.append(index)

    except KeyError:
        print(f"Row - 9 - not found")

    try:
        rows_2 = []
        condition = df.iloc[:, 0] == "9.1"
        index = condition[condition].index[0]
        rows_2.append(index)

    except KeyError:
        print(f"Row - 9.1 - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_float(dataframe[sheet].iat[rows_1[i], c])
        first_part = round(value_sum_1, 2)

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_float(dataframe[sheet].iat[rows_2[i], c])
        second_part = round(value_sum_2, 2)

    if first_part == second_part:
        results.append([sheet, True])
    else:
        results.append([sheet, False, c])
        print(first_part, '!=', second_part)

    return results


# PCP_035_R
def rule_27_ar2(dataframe, sheet_number):
    if sheet_number == 12:
        check_sheets = [2, 4]
    else:
        check_sheets = [3, 5]

    results = []

    value_sum_1 = 0
    sheet = AR2_TO_CHECK[sheet_number]
    df = dataframe[sheet]

    try:
        condition = df.iloc[:, 0] == "9.1.1"
        index = condition[condition].index[0]

    except KeyError:
        print(f"Row - 9.1.1 - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(3, columns_number):
        if dataframe[sheet].iat[6, c] in GEO3:
            value_sum_1 += to_float(dataframe[sheet].iat[index, c])

    first_part = round(value_sum_1, 2)

    value_sum_2 = 0
    sheet = AR2_TO_CHECK[check_sheets[0]]
    df = dataframe[sheet]

    try:
        condition = df.iloc[:, 0] == "8.1.2.1"
        index = condition[condition].index[0]

    except KeyError:
        print(f"Row - 8.1.2.1 - not found")

    columns_number = dataframe[sheet].shape[1]
    for c in range(3, columns_number):
        if dataframe[sheet].iat[6, c] in GEO3:
            value_sum_2 += to_float(dataframe[sheet].iat[index, c])

    sheet = AR2_TO_CHECK[check_sheets[1]]
    df = dataframe[sheet]

    try:
        condition = df.iloc[:, 0] == "8.1.2.1"
        index = condition[condition].index[0]

    except KeyError:
        print(f"Row - 8.1.2.1 - not found")

    columns_number = dataframe[sheet].shape[1]
    for c in range(3, columns_number):
        if dataframe[sheet].iat[6, c] in GEO3:
            value_sum_2 += to_float(dataframe[sheet].iat[index, c])

    second_part = round(value_sum_2, 2)

    if first_part == second_part:
        results.append([sheet, True])
    else:
        results.append([sheet, False, c])
        print(first_part, '!=', second_part)

    return results


# PCP_038_R
def rule_29_ar2(dataframe, sheet_number):
    if sheet_number == 12:
        check_sheets = [2, 3]
    else:
        check_sheets = [4, 5]

    first_part = []
    second_part = []

    results = []
    value_sum_1 = []
    sheet = AR2_TO_CHECK[sheet_number]
    df = dataframe[sheet]

    try:
        condition = df.iloc[:, 0] == "9.1.2"
        index = condition[condition].index[0]

    except KeyError:
        print(f"Row - 9.1.2 - not found")

    for country in GEO3:
        ind = dataframe[sheet].loc[6] == country
        col_index = ind[ind].index[0]
        print(country, col_index)

        get_value = dataframe[sheet].iat[index, col_index]
        value = to_float(get_value)
        value = round(value, 2)
        value_sum_1.append(to_float(value))

    for i, value in enumerate(value_sum_1):
        value_sum_1[i] = round(value, 2)
        first_part.append(value_sum_1[i])

    value_sum_2 = []
    sheet = AR2_TO_CHECK[check_sheets[0]]

    df = dataframe[sheet]

    try:
        condition = df.iloc[:, 0] == "8.1.2.2"
        index = condition[condition].index[0]

    except KeyError:
        print(f"Row - 8.1.2.2 - not found")

    for country in GEO3:
        ind = dataframe[sheet].loc[6] == country
        print(country)
        col_index = ind[ind].index[0]
        print(col_index)

        get_value = dataframe[sheet].iat[index, col_index]
        value = to_float(get_value)
        value = round(value, 2)
        value_sum_2.append(to_float(value))

    sheet = AR2_TO_CHECK[check_sheets[1]]

    df = dataframe[sheet]

    try:
        condition = df.iloc[:, 0] == "8.1.2.2"
        index = condition[condition].index[0]

    except KeyError:
        print(f"Row - 8.1.2.2 - not found")

    for n, country in enumerate(GEO3):
        if sheet == '4a.R.L_krajGEO3':
            ind = dataframe[sheet].loc[7] == country
        else:
            ind = dataframe[sheet].loc[6] == country
        print(sheet)
        print(country)
        col_index = ind[ind].index[0]
        print(col_index)

        get_value = dataframe[sheet].iat[index, col_index]
        value = to_float(get_value)
        value = round(value, 2)
        value_sum_2[n] += to_float(value)

    for i, value in enumerate(value_sum_2):
        value_sum_2[i] = round(value, 2)
        second_part.append(value_sum_2[i])

    for n, country in enumerate(GEO3):
        if first_part[n] == second_part[n]:
            results.append([sheet, True])
        else:
            results.append([sheet, False, country])
            print("24: ", first_part[n], '!=', second_part[n])

    return results


def to_float(value):
    # Convert the value to a float using pd.to_numeric()
    try:
        # Convert the value to a float using pd.to_numeric()
        value_float = pd.to_numeric(value, errors='coerce')  # Convert to float and replace non-numeric values with NaN

        # Replace NaN with 0
        if pd.isna(value_float):
            value_float = 0

        return value_float

    except ValueError:
        return None  # Handle the case where the conversion fails


def to_int(value):
    # Convert the value to a float using pd.to_numeric()
    try:
        # Convert the value to a float using pd.to_numeric()
        value_int = pd.to_numeric(value, errors='coerce')  # Convert to float and replace non-numeric values with NaN

        # Replace NaN with 0
        if pd.isna(value_int):
            value_int = 0

        return value_int

    except ValueError:
        return None  # Handle the case where the conversion fails


first_1 = ['1.1.1', '1.1.2', '1.2.1', '2.1.1', '2.1.2', '3.1.1', '3.1.2', '3.1.3', '3.1.4', '3.1.5', '3.1.6', '3.1.7',
         '3.1.8']
second_1 = ['1.1', '1.1', '1.2', '2.1', '2.1', '3.1', '3.1', '3.1', '3.1', '3.1', '3.1', '3.1', '3.1']


def rule_1_ar1(dataframe, sheet_number):
    rules = []
    for i in range(len(first_1)):
        rules.append(rule_1_13_ar1(dataframe, sheet_number, i, first_1, second_1))
    return rules


# RW_ST.01_01 till RW_ST.01_13
def rule_1_13_ar1(dataframe, sheet_number, k, first, second):
    results = []
    print(k)
    sheet = AR1_TO_CHECK[sheet_number]
    df = dataframe[sheet]
    try:
        rows_1 = []
        condition = df.iloc[:, 0] == first[k]
        index = condition[condition].index[0]
        rows_1.append(index)

    except IndexError:
        print(f"Row - {first[k]} - not found")

    try:
        rows_2 = []
        condition = df.iloc[:, 0] == second[k]
        index = condition[condition].index[0]
        rows_2.append(index)

    except IndexError:
        print(f"Row - {second[k]} - not found")

    columns_number = dataframe[sheet].shape[1]

    for c in range(5, columns_number):
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_int(dataframe[sheet].iat[rows_1[i], c])
        first_part = value_sum_1

        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_int(dataframe[sheet].iat[rows_2[i], c])
        second_part = value_sum_2

    if first_part <= second_part:
        results.append([sheet, True])
    else:
        results.append([sheet, False, c])
        print(first_part, '!=', second_part)

    return results


# RW_ST.01_14
def rule_14_ar1(dataframe, sheet_number):
    results = []
    sheet = AR1_TO_CHECK[sheet_number]

    df = dataframe[sheet]
    try:
        rows_1 = []
        condition = df.iloc[:, 0] == '3.1'
        index = condition[condition].index[0]
        rows_1.append(index)

    except IndexError:
        print(f"Row - 3.1 - not found")

    sheet = AR1_TO_CHECK[sheet_number + 2]
    df = dataframe[sheet]
    try:
        rows_2 = []
        condition = df.iloc[:, 0] == '9.1'
        index = condition[condition].index[0]
        rows_2.append(index)

    except IndexError:
        print(f"Row - not found")

    for c in [5]:
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_int(dataframe[sheet].iat[rows_1[i], c])
        first_part = value_sum_1

        sheet = AR1_TO_CHECK[sheet_number + 2]
        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_int(dataframe[sheet].iat[rows_2[i], c])
        second_part = value_sum_2

    if first_part <= second_part:
        results.append([sheet, True])
    else:
        results.append([sheet, False, c])
        print(first_part, '!=', second_part)

    return results


# RW_ST.01_15
def rule_15_ar1(dataframe, sheet_number):
    results = []
    sheet = AR1_TO_CHECK[sheet_number]

    df = dataframe[sheet]
    try:
        rows_1 = []
        condition = df.iloc[:, 0] == '3.1'
        index = condition[condition].index[0]
        rows_1.append(index)

    except IndexError:
        print(f"Row - 3.1 - not found")

    try:
        rows_2 = range(9, 40)

    except IndexError:
        print(f"Row - not found")

    for c in [6]:
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_int(dataframe[sheet].iat[rows_1[i], c])
        first_part = value_sum_1

    for c in [3]:
        sheet = AR1_TO_CHECK[sheet_number + 3]
        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_int(dataframe[sheet].iat[rows_2[i], c])
        second_part = value_sum_2

    if first_part == second_part:
        results.append([sheet, True])
    else:
        results.append([sheet, False, c])
        print(first_part, '!=', second_part)

    return results


first_2 = [('1.1', 5), ('1.1', 6), ('1.2', 5), ('1.2', 6), ('1.2.1', 5), ('1.2.1', 6), ('2.1', 5), ('2.1', 6), ('2.1.1', 5), ('2.1.1', 6), ('2.2', 5), ('2.2', 6), ('3.1', 6)]
second_2 = [('7.1', 5), ('7.1', 6), ('7.2', 5), ('7.2', 6), ('7.2.2', 5), ('7.2.2', 6), ('8.1', 5), ('8.1', 6), ('8.1.1', 5), ('8.1.1', 6), ('8.2', 5), ('8.2', 6), ('9.1', 6)]


def rule_2_ar1(dataframe, sheet_number):
    rules = []
    for i in range(len(first_2)):
        rules.append(rule_16_28_ar1(dataframe, sheet_number, i, first_2, second_2))
    return rules


# RW_ST.01_16 till RW_ST.01_28
def rule_16_28_ar1(dataframe, sheet_number, k, first, second):
    results = []

    sheet = AR1_TO_CHECK[sheet_number]
    df = dataframe[sheet]
    try:
        rows_1 = []
        condition = df.iloc[:, 0] == first[k][0]
        index = condition[condition].index[0]
        rows_1.append(index)

    except IndexError:
        print(f"Row - {first[k][0]} - not found")

    sheet = AR1_TO_CHECK[sheet_number + 2]
    df = dataframe[sheet]
    try:
        rows_2 = []
        condition = df.iloc[:, 0] == second[k][0]
        index = condition[condition].index[0]
        rows_2.append(index)

    except IndexError:
        print(f"Row - {second[k][0]} - not found")

    sheet = AR1_TO_CHECK[sheet_number]
    df = dataframe[sheet]
    for c in [first[k][1]]:
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_int(df.iat[rows_1[i], c])
        first_part = value_sum_1

    sheet = AR1_TO_CHECK[sheet_number + 2]
    df = dataframe[sheet]
    for c in [second[k][1]]:
        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_int(df.iat[rows_2[i], c])
        second_part = value_sum_2

    if first_part <= second_part:
        results.append([sheet, True])
    else:
        results.append([sheet, False, c])
        print(first_part, '!=', second_part)

    return results


# RW_ST.01_29
def rule_29_ar1(dataframe, sheet_number):
    results = []

    sheet = AR1_TO_CHECK[sheet_number]
    df = dataframe[sheet]
    try:
        rows_1 = []
        condition = df.iloc[:, 0] == '3.1'
        index = condition[condition].index[0]
        rows_1.append(index)

    except IndexError:
        print(f"Row - 3.1 - not found")

    try:
        rows_2 = range(9, 40)

    except IndexError:
        print(f"Row - not found")

    for c in [6]:
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_int(dataframe[sheet].iat[rows_1[i], c])
        first_part = value_sum_1

    for c in [4]:
        sheet = AR1_TO_CHECK[sheet_number + 3]
        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_int(dataframe[sheet].iat[rows_2[i], c])
        second_part = value_sum_2

    if first_part == second_part:
        results.append([sheet, True])
    else:
        results.append([sheet, False, c])
        print(first_part, '!=', second_part)

    return results


# RW_ST.01_30
def rule_30_ar1(dataframe, sheet_number):
    results = []

    sheet = AR1_TO_CHECK[sheet_number]
    df = dataframe[sheet]
    try:
        rows_1 = []
        condition = df.iloc[:, 0] == '3.1'
        index = condition[condition].index[0]
        rows_1.append(index)

    except IndexError:
        print(f"Row - 3.1 - not found")

    try:
        rows_2 = range(9, 40)

    except IndexError:
        print(f"Row - not found")

    for c in [6]:
        value_sum_1 = 0
        for i in range(len(rows_1)):
            value_sum_1 += to_int(dataframe[sheet].iat[rows_1[i], c])
        first_part = value_sum_1

    for c in [5]:
        sheet = AR1_TO_CHECK[sheet_number + 3]
        value_sum_2 = 0
        for i in range(len(rows_2)):
            value_sum_2 += to_int(dataframe[sheet].iat[rows_2[i], c])
        second_part = value_sum_2

    if first_part == second_part:
        results.append([sheet, True])
    else:
        results.append([sheet, False, c])
        print(first_part, '!=', second_part)

    return results