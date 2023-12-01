import pandas as pd
from variables import geo3, geo3_wld

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
    'ST.07',
    'p-dane'
]


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


def check_rules_ar2(ar: int, df: pd.DataFrame, rule: str, cc: int) -> list:
    """
    Checking the compliance rules for NBP report.
    :param ar:      sheet (AR1 = 1, AR2 = 2).               Type int.
    :param df:      DataFrame
    :param rule:    Name of the rule.                       Type string.
    :param cc:      Column with first value in DataFrame.   Type int.
    :return:        [sheet number, boolean, row number, column in sheet]
    """
    if ar == 1:
        pass
    elif ar == 2:
        first_part = 0
        second_part = 0
        results = []

        rules = {
            "PCP_090": [[2, 3, 4, 5, 6, 7, 8, 9], ['8'], ['8.1.1', '8.1.2'], 0],
            "PCP_091": [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.1'], ['8.1.1.1', '8.1.1.2'], 1],
            "PCP_092": [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2'], ['8.1.2.1', '8.1.2.2'], 2],
            "PCP_093": [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.1'], ['8.1.2.1.1.{i}', [1, 4], [0, 1]], 3],
            "PCP_094": [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.1'], ['8.1.2.1.2.{i}', [1, 4], [0, 1]], 4],
            "PCP_096": [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.1.2.{i}', [1, 10], [1, 4]],
                        ['8.1.2.1.2.{i}.1.{j}', [1, 10], [1, 4]], 5],
            "PCP_099": [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.1.2.1'], ['8.1.2.1.2.{i}.2.{j}', [0, 1], [1, 3]], 6],
            "PCP_006": [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.1.2.{i}.2.2]', [1, 10], [0, 1]],
                        ['8.1.2.1.3.{j}', [0, 1], [2, 6]], 7],
            "PCP_095": [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.2'], ['8.1.2.2.2.{i}', [0, 10], [0, 1]], 8],
            "PCP_102": [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.2.2.1'], ['8.1.2.2.2.1.1.{j}', [0, 1], [1, 4]], 9],
            "PCP_105": [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.2.2.1'], ['8.1.2.1.2.1.2.{j}', [0, 1], [1, 4]], 10],
            "PCP_007": [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.2.2.{i}.2.2', [1, 10], [0, 1]],
                        ['8.1.2.2.3.{j}', [0, 1], [2, 8]], 11],
            "PCP_108": [[6, 7, 8, 9], ['8.1.2.1.2.{i}.2.1', [1, 10], [0, 1]],
                        ['8.1.2.1.2.{i}.2.1.{j}', [1, 10], [1, 4]], 12],
            "PCP_120": [[6, 7, 8, 9], ['8.1.2.1.2.1.2.1.1'], ['8.1.2.1.2.1.2.1.1.{j}', [0, 1], [1, 5]], 13],
            "PCP_109": [[6, 7, 8, 9], ['8.1.2.1.2.1.2.2'], ['8.1.2.1.2.1.2.2.{j}', [0, 1], [1, 4]], 14],
            "PCP_121": [[6, 7, 8, 9], ['8.1.2.1.2.1.2.2.1'], ['8.1.2.1.2.1.2.2.1.{j}', [0, 1], [1, 5]], 15],
            "PCP_110": [[6, 7, 8, 9], ['8.1.2.2.2.1.2.1'], ['8.1.2.2.2.1.2.1.{j}', [0, 1], [1, 4]], 16],
            "PCP_122": [[6, 7, 8, 9], ['8.1.2.2.2.1.2.1.1'], ['8.1.2.2.2.1.2.1.1.{j}', [0, 1], [1, 6]], 17],
            "PCP_111": [[6, 7, 8, 9], ['8.1.2.2.2.1.2.2'], ['8.1.2.2.2.1.2.2.{j}', [0, 1], [1, 4]], 18],
            "PCP_123": [[6, 7, 8, 9], ['8.1.2.2.2.1.2.2.1'], ['8.1.2.2.2.1.2.2.1.{j}', [0, 1], [1, 6]], 19],
            "PCP_245_R": [[12, 13], ['9.1'], ['9.1.1', '9.1.2'], 20],
            "DSDs_038_R": [[12, 13], ['9.1.1'], ['9.1.1.{j}', [0, 1], [743, 1077]], 21],
            "DSDs_040_R": [[12, 13], ['9.1.2'], ['9.1.2.{j}', [0, 1], [743, 1077]], 22],
        }

        special_rules = {
            "PCP_031_R": [[12, 13], [9], ['8', 'SHEET:4a.R.L_PLiW2/4a.R.W_PLiW2', 'GEO3'], 23],
            "PCP_031_R_G1": [[12, 13], [9], ['8', 'SHEET:4a.R.L_PLiW2/4a.R.W_PLiW2', 'GEO6_Z_G1'], 24],
            "W_008": [[12, 13], [9], ['9.1', 'COMPARE:=<'], 25],
            "PCP_035_R": [[12, 13], ['9.1.1'], ['8.1.2.1', 'SHEET:4a.R.L_PLiW2/4a.R.W_PLiW2', 'GEO3'], 26],
            "PCP_035_R_G1": [[12, 13], ['9.1.1'], ['8.1.2.1', 'SHEET:4a.R.L_PLiW2/4a.R.W_PLiW2', 'GEO6_Z_G1'], 27],
            "PCP_038_R": [[12, 13], ['9.1.2'], ['8.1.2.2', 'SHEET:4a.R.L_PLiW2/4a.R.W_PLiW2', 'GEO3'], 28],
            "PCP_038_R_G1": [[12, 13], ['9.1.2'], ['8.1.2.2', 'SHEET:4a.R.L_PLiW2/4a.R.W_PLiW2', 'GEO6_Z_G1'], 29]
        }

        sheet_rules = {
            "NCN": [],
            "NCV": [],
            "NEG": [],
            "INT": [],
            "DEC": [],
            "NNUL": []
        }
        case = rules[rule]
        sheets = case[0]

        for sheet in sheets:
            df_tc = df[AR2_TO_CHECK[sheet]]
            columns = [*range(cc, df_tc.shape[1])]
            for c in columns:

                # part 1
                rows = []
                if isinstance(case[1][0], str) and '{}' in case[1][0]:
                    i = case[1][1]
                    j = case[1][2]

                    for i_number in range(i[0], i[1]):  # Adjust the range as needed
                        for j_number in range(j[0], j[1]):  # Adjust the range as needed
                            # Use the values of i and j in your logic
                            updated_value = case[1][0].format(i=i_number, j=j_number)
                            rows.append(df_tc[df_tc == updated_value].index[0])
                else:
                    rows.append(df_tc[df_tc == case[1][0]].index[0])

                for row in rows:
                    if df_tc.iat[row, c] == '':
                        first_part += 0
                    else:
                        first_part += pd.to_numeric(df_tc.iat[row, c])

                # part 2
                rows = []
                if isinstance(rules[rule][2][0], str) and '{}' in rules[rule][2][0]:
                    i = case[2][1]
                    j = case[2][2]

                    for i_number in range(i[0], i[1]):  # Adjust the range as needed
                        for j_number in range(j[0], j[1]):  # Adjust the range as needed
                            if rule == "PCP_007" and j_number == 4:
                                continue
                            # Use the values of i and j in your logic
                            updated_value = case[2][0].format(i=i_number, j=j_number)
                            print(updated_value)
                            rows.append(df_tc[df_tc == updated_value].index[0])
                else:
                    rows.append(df_tc[df_tc == case[1][0]].index[0])

                for row in rows:
                    if df_tc.iat[row, c] == '':
                        second_part += 0
                    else:
                        second_part += pd.to_numeric(df_tc.iat[row, c])

                if first_part == second_part:
                    results.append([sheet, True, rules[rule][3]])
                else:
                    text = ' + '.join(rules[rule][2])
                    results.append([sheet, False, rules[rule][3], c])
                    print(f"{rules[rule][1]}: ", first_part, f'!= {text}', second_part)
        return results
    else:
        print(f'There are no more rules for ar{ar}')


def check_rules_ar1(ar: int, df: pd.DataFrame, rule: str, cc: int) -> list:
    rules = {
        "RW_ST.01_01": [1, ['1.1.1'], '<=', ['1.1'], 0, 8],
        "RW_ST.01_02": [1, ['1.1.2'], '<=', ['1.1'], 1, 8],
        "RW_ST.01_03": [1, ['1.2.1'], '<=', ['1.2'], 2, 8],
        "RW_ST.01_04": [1, ['2.1.1'], '<=', ['2.1'], 3, 8],
        "RW_ST.01_05": [1, ['2.1.2'], '<=', ['2.1'], 4, 8],
        "RW_ST.01_06": [1, ['3.1.1'], '<=', ['3.1'], 5, 8],
        "RW_ST.01_07": [1, ['3.1.2'], '<=', ['3.1'], 6, 8],
        "RW_ST.01_08": [1, ['3.1.3'], '<=', ['3.1'], 7, 8],
        "RW_ST.01_09": [1, ['3.1.4'], '<=', ['3.1'], 8, 8],
        "RW_ST.01_10": [1, ['3.1.5'], '<=', ['3.1'], 9, 8],
        "RW_ST.01_11": [1, ['3.1.6'], '<=', ['3.1'], 10, 8],
        "RW_ST.01_12": [1, ['3.1.7'], '<=', ['3.1'], 11, 8],
        "RW_ST.01_13": [1, ['3.1.8'], '<=', ['3.1'], 12, 8],
        "RW_ST.01_14": [[1, 3], ['NRP', ['M03_UKP_']], '<=', ['NRP', ['M06_UIP_']], 13, [0, 5]],
        "RW_ST.01_15": [[1, 4], ['PRP', ['M03_UKP_']], '<=', ['M03_UKP_PRP_', [geo3_wld]], 14, [0, 5]],
        "RW_ST.01_16": [[1, 3], ['NRP', ['M01_UKP_']], '<=', ['NRP', ['M04_UIP_']], 15, [0, 5]],
        "RW_ST.01_17": [[1, 3], ['PRP', ['M01_UKP_']], '<=', ['PRP', ['M04_UIP_']], 16, [0, 5]],
        "RW_ST.01_18": [[1, 3], ['NRP', ['M01_IT.OKP_']], '<=', ['NRP', ['M04_IT.OIP_']], 17, [0, 5]],
        "RW_ST.01_19": [[1, 3], ['PRP', ['M01_IT.OKP_']], '<=', ['PRP', ['M04_IT.OIP_']], 18, [0, 5]],
        "RW_ST.01_20": [[1, 3], ['NRP', ['M01_UKP.IT.OKP_']], '<=', ['NRP', ['M04_UIP.IT.OIP_']], 19, [0, 5]],
        "RW_ST.01_21": [[1, 3], ['PRP', ['M01_UKP.IT.OKP_']], '<=', ['PRP', ['M04_UIP.IT.OIP_']], 20, [0, 5]],
        "RW_ST.01_22": [[1, 3], ['NRP', ['M02_UKP_']], '<=', ['NRP', ['M05_UIP_']], 21, [0, 5]],
        "RW_ST.01_23": [[1, 3], ['PRP', ['M02_UKP_']], '<=', ['PRP', ['M05_UIP_']], 22, [0, 5]],
        "RW_ST.01_24": [[1, 3], ['NRP', ['M02_OMOB_']], '<=', ['NRP', ['M05_UIP.OMOB_']], 23, [0, 5]],
        "RW_ST.01_25": [[1, 3], ['PRP', ['M02_OMOB_']], '<=', ['PRP', ['M05_UIP.OMOB_']], 24, [0, 5]],
        "RW_ST.01_26": [[1, 3], ['NRP', ['M02_IT.OKP_']], '<=', ['NRP', ['M05_IT.UIP_']], 25, [0, 5]],
        "RW_ST.01_27": [[1, 3], ['PRP', ['M02_IT.OKP_']], '<=', ['PRP', ['M05_IT.UIP_']], 26, [0, 5]],
        "RW_ST.01_28": [[1, 3], ['NRP', ['M03.UKP_']], '<=', ['NRP', ['M06_UIP_']], 27, [0, 5]],
        "RW_ST.01_29": [[1, 3], ['PRP', ['M03.UKP_']], '<=', ['PRP', ['M06_UIP_']], 28, [0, 5]],
        "RW_ST.01_30": [[1, 3], ['NRP', ['M03.UKP_']], '<=', ['NRP', ['M06_UIP_']], 27, [0, 5]],

        "RW_ST.02_01": [2, ['M09_UKPE_'], '<=', ['M09_'], 0, 0],
        "RW_ST.02_02": [2, ['M09_UKPEZR_'], '<=', ['M09_UKKPE_'], 1, 0],
        "RW_ST.02_03": [2, ['M09_UAKPE_'], '<=', ['M09_UKKPE_'], 2, 0],
        "RW_ST.02_04": [[2, 4], ['PRP', ['M09_UKPE_']], '<=', ['M09_UKPE_PRP_', geo3_wld], 3, [0, 5]],
        "RW_ST.02_05": [[2, 4], ['PRP', ['M09_UKKPE_']], '<=', ['M09_UKKPE_PRP_', geo3_wld], 4, [0, 5]],
        "RW_ST.02_06": [[2, 4], ['PRP', ['M09_UKPEZR_']], '<=', ['M09_UKPEZR_PRP_', geo3_wld], 5, [0, 5]],
        "RW_ST.02_07": [[2, 4], ['PRP', ['M09_UAKPE_']], '<=', ['M09_UAKPE_PRP_', geo3_wld], 6, [0, 5]],

        "RW_ST.03_01": [3, ['M04_UIP_'], '<=', ['M04_UIP.OMOB_'], 0, 0],
        "RW_ST.03_02": [3, ['M04_IT.OIP_'], '<=', ['M04_UIP.IT.OIP_'], 1, 0],
        "RW_ST.03_06": [3, ['M04_IT.OIP_'], '<=', ['M04_IT.PBL_'], 2, 0],
        "RW_ST.03_03": [3, ['M05_UIP_'], '<=', ['M05_UIP.OMOB_'], 3, 0],
        "RW_ST.03_04": [3, ['M05_IT.OIP_'], '<=', ['M05_IT.PBL_'], 4, 0],
        "RW_ST.03_05": [3, ['M06_UIP_'], '<=', ['M06_UIP.OMOB_'], 5, 0],

        "RW_ST.04_01": [4, 'M03_UKP.OZBL_PRP_', '<=', 'M03_UKP_PRP_', 0, 5],
        "RW_ST.04_02": [4, 'M03_UKP.OZBL_PRP_', '<=', 'M03_UKP_PRP_', 0, 5],

        "RW_ST.05_01": [5, ['11.1.1.1'], '<=', ['11.1.1'], 0, 4],
        "RW_ST.05_02": [5, ['M10_NRP'], '>=', ['M201_NRP'], 1, [4, 5]],
        "RW_ST.05_03": [5, ['M10_PRP'], '>=', ['M201_PRP'], 2, [4, 5]],
        "RW_ST.05_04": [5, ['11.2.1.1'], '<=', ['11.2.1'], 3, 4],
        "RW_ST.05_05": [5, ['M11_NRP'], '>=', ['M202_NRP'], 4, [4, 5]],
        "RW_ST.05_06": [5, ['M11_PRP'], '>=', ['M202_PRP'], 5, [4, 5]],
        "RW_ST.05_07": [5, ['12.1.1'], '<=', ['12.1'], 6, 4],
        "RW_ST.05_08": [[5, 6], ['M201_PRP', ['_KI_OKP.UKP_', '_KB_OKP.UKP_']], '==', ['M10_OKP.UKP_PRP_', geo3], 7, [0, 5]],
        "RW_ST.05_09": [[5, 6], ['M201_PRP', ['_KI_OCB_', '_KB_OCB_']], '==', ['M10_OCB_PRP_', geo3], 8, [0, 5]],
        "RW_ST.05_10": [[5, 6], ['M201_PRP', ['_KI_OKP.IT_', '_KB_OKP.IT_']], '==', ['M10_OKP.IT_PRP_', geo3], 9, [0, 5]],
        "RW_ST.05_11": [[5, 6], ['M202_PRP', ['_KI_OKP.UKP_', '_KB_OKP.UKP_']], '==', ['M11_OKP.UKP_PRP_', geo3], 10, [0, 5]],
        "RW_ST.05_12": [[5, 6], ['M202_PRP', ['_KI_OCB_', '_KB_OCB_']], '==', ['M11_OCB_PRP_', geo3], 11, [0, 5]],
        "RW_ST.05_13": [[5, 6], ['M202_PRP', ['_KI_OKP.IT_', '_KB_OKP.IT_']], '==', ['M11_OKP.IT_PRP_', geo3], 12, [0, 5]]
    }

    results = []

    if rule in ["RW_ST.04_01"]:
        case = rules[rule]
        sheet = case[0]
        df_tc = df[AR1_TO_CHECK[sheet]]
        code_row = case[5]
        code_col = 0

        parts = [1, 3]
        match = [0, 0]

        rows = [*range(df_tc[df_tc[0].notna()].index[0], df_tc[df_tc[df_tc[0].notna()].index[0]:][df_tc[0].isna()].index[0])]

        for row in rows:
            for p, part in enumerate(parts):
                print(df_tc.iloc[code_row])
                col = pd.Index(df_tc.iloc[code_row]).get_loc(case[part])
                # Check if df_tc is not empty
                if not df_tc.empty:
                    # Check if the value exists in the specified column
                    if case[part] in df_tc[code_col].values:
                        # Get the index of the first occurrence
                        match[p] = df_tc.iat[row, col]
                    else:
                        print(f"The value {case[part][0]} does not exist in the specified column.")
                else:
                    print("The DataFrame is empty.")

            condition = f"{match[0]} {case[2]} {match[1]}"
            print(condition)

            if eval(condition):
                results.append([sheet, True, case[4]])
            else:
                results.append([sheet, False, case[4], col])

            return results

    if rule in [
        "RW_ST.05_01", "RW_ST.05_04", "RW_ST.05_07",

        "RW_ST.01_01", "RW_ST.01_02", "RW_ST.01_03", "RW_ST.01_04", "RW_ST.01_05", "RW_ST.01_06", "RW_ST.01_07",
        "RW_ST.01_08", "RW_ST.01_09", "RW_ST.01_10", "RW_ST.01_11", "RW_ST.01_12", "RW_ST.01_13",

        "RW_ST.02_01", "RW_ST.02_02", "RW_ST.02_03",

        "RW_ST.03_01", "RW_ST.03_02", "RW_ST.03_03", "RW_ST.03_04", "RW_ST.03_05", "RW_ST.03_06"
                ]:

        case = rules[rule]
        sheet = case[0]
        df_tc = df[AR1_TO_CHECK[sheet]]
        code_col = case[5]

        columns = [*range(cc, df_tc.shape[1])]
        parts = [1, 3]
        match = [0, 0]

        c: int
        for c in columns:
            for p, part in enumerate(parts):
                rows = []
                if isinstance(case[part], str) and '{}' in case[1][0]:
                    print("HERE")
                    if p == 0:
                        k = 1
                    else:
                        k = 3
                    i = case[k][1]
                    j = case[k][2]

                    for i_number in range(i[0], i[1]):  # Adjust the range as needed
                        for j_number in range(j[0], j[1]):  # Adjust the range as needed
                            # Use the values of i and j in your logic
                            updated_value = case[part][0].format(i=i_number, j=j_number)
                            rows.append(df_tc[df_tc[code_col] == updated_value].index[0])
                else:
                    # Check if df_tc is not empty
                    if not df_tc.empty:
                        # Check if the value exists in the specified column
                        if case[part] in df_tc[code_col].values:
                            # Get the index of the first occurrence
                            rows.append(df_tc[df_tc[code_col] == case[part][0]].index[0])
                            print("Index of the first occurrence:", df_tc[df_tc[code_col] == case[part][0]].index[0])
                        else:
                            print(f"The value {case[part][0]} does not exist in the specified column.")
                    else:
                        print("The DataFrame is empty.")

                for row in rows:
                    print(row, c, df_tc.iat[row, c])
                    match[p] += df_tc.iat[row, c]

            condition = f"{match[0]} {case[2]} {match[1]}"
            print(condition)

            if eval(condition):
                results.append([sheet, True, case[4]])
            else:
                results.append([sheet, False, case[4], c])

            return results

    if rule in ["RW_ST.05_02", "RW_ST.05_03", "RW_ST.05_05", "RW_ST.05_06"]:
        case = rules[rule]
        sheet = case[0]
        df_tc = df[AR1_TO_CHECK[sheet]]
        code_col = case[5][0]
        code_row = case[5][1]

        parts = [1, 3]
        match = [0, 0]
        rows = [*range(df_tc[df_tc[code_col].notna()].index[0], df_tc.shape[0])]

        c: int
        for row in rows:
            for p, part in enumerate(parts):
                # Check if df_tc is not empty
                if not df_tc.empty:
                    # Check if the value exists in the specified column
                    if case[part] in df_tc.loc[code_row].values:
                        # Get the index of the first occurrence
                        col = pd.Index(df_tc.iloc[code_row]).get_loc(case[part])
                        print("Index of the first occurrence:", df_tc[df_tc[code_col] == case[part][0]].index[0])

                        match[p] = df_tc.iat[row, col]
                    else:
                        print(f"The value {case[part][0]} does not exist in the specified column.")
                else:
                    print("The DataFrame is empty.")

            condition = f"{match[0]} {case[2]} {match[1]}"
            print(condition)

            if eval(condition):
                results.append([sheet, True, case[4]])
            else:
                results.append([sheet, False, case[4], row])

            return results

    if rule in [
        "RW_ST.05_08", "RW_ST.05_09", "RW_ST.05_10", "RW_ST.05_11", "RW_ST.05_12", "RW_ST.05_13",

        "RW_ST.01_14", "RW_ST.01_15", "RW_ST.01_16", "RW_ST.01_17", "RW_ST.01_18", "RW_ST.01_19",
        "RW_ST.01_20", "RW_ST.01_21", "RW_ST.01_22", "RW_ST.01_23", "RW_ST.01_24", "RW_ST.01_25",
        "RW_ST.01_26", "RW_ST.01_27", "RW_ST.01_28", "RW_ST.01_29", "RW_ST.01_30",

        "RW_ST.02_04", "RW_ST.02_05", "RW_ST.02_06", "RW_ST.02_07"
    ]:
        case = rules[rule]

        code_col = case[5][0]
        code_row = case[5][1]

        parts = [1, 3]
        match = [0, 0]

        c: int
        for p, part in enumerate(parts):
            for row_value in case[part][1]:
                col_value = case[part][0]

                # Check if df_tc is not empty
                if p == 0:
                    sheet = case[0][p]
                    df_tc = df[AR1_TO_CHECK[sheet]]

                    if not df_tc.empty:
                        # Check if the value exists in the specified column
                        if case[part] in df_tc.loc[code_row].values:
                            # Get the index of the first occurrence
                            col = pd.Index(df_tc.iloc[code_row]).get_loc(col_value)
                            row = df_tc[df_tc[code_col] == row_value].index[0]
                            print("Index of the first occurrence:", df_tc[df_tc[code_col] == case[part][0]].index[0])

                            match[p] += df_tc.iat[row, col]
                        else:
                            print(f"The value {case[part][0]} does not exist in the specified column.")
                    else:
                        print("The DataFrame is empty.")

                else:
                    sheet = case[0][p]
                    df_tc = df[AR1_TO_CHECK[sheet]]

                    if not df_tc.empty:
                        # Check if the value exists in the specified column
                        if case[part] in df_tc.loc[code_row].values:
                            # Get the index of the first occurrence
                            col = pd.Index(df_tc.iloc[code_row]).get_loc(case[part])
                            row = df_tc[df_tc[code_col] == case[part][0]].index[0]
                            print("Index of the first occurrence:", df_tc[df_tc[code_col] == case[part][0]].index[0])

                            match[p] += df_tc.iat[row, col]
                        else:
                            print(f"The value {case[part][0]} does not exist in the specified column.")
                    else:
                        print("The DataFrame is empty.")

            condition = f"{match[0]} {case[2]} {match[1]}"
            print(condition)

            if eval(condition):
                results.append([sheet, True, case[4]])
            else:
                results.append([sheet, False, case[4], col])

            return results





