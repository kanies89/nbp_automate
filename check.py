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


# PCP_090
def rule_1(dataframe, sheet_number):
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
def rule_2(dataframe, sheet_number):
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
def rule_3(dataframe, sheet_number):
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
def rule_4(dataframe, sheet_number):
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
def rule_5(dataframe, sheet_number):
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
def rule_6(dataframe, sheet_number):
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
def rule_7(dataframe, sheet_number):
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
def rule_8(dataframe, sheet_number):
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
def rule_9(dataframe, sheet_number):
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
def rule_10(dataframe, sheet_number):
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
def rule_11(dataframe, sheet_number):
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
def rule_12(dataframe, sheet_number):
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
def rule_13(dataframe, sheet_number):
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
def rule_14(dataframe, sheet_number):
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
def rule_15(dataframe, sheet_number):
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
def rule_16(dataframe, sheet_number):
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
def rule_17(dataframe, sheet_number):
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
def rule_18(dataframe, sheet_number):
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
def rule_19(dataframe, sheet_number):
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
def rule_20(dataframe, sheet_number):
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
def rule_21(dataframe, sheet_number):
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
def rule_22(dataframe, sheet_number):
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
def rule_23(dataframe, sheet_number):
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
def rule_24(dataframe, sheet_number):
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
def rule_26(dataframe, sheet_number):
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
def rule_27(dataframe, sheet_number):
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
def rule_29(dataframe, sheet_number):
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
