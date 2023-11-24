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


def check_rules(ar: int, df: pd.DataFrame, rule: str, cc: int) -> object:
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
            "PCP_090":          [[2, 3, 4, 5, 6, 7, 8, 9], ['8'], ['8.1.1', '8.1.2'], 0],
            "PCP_091":          [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.1'], ['8.1.1.1', '8.1.1.2'], 1],
            "PCP_092":          [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2'], ['8.1.2.1', '8.1.2.2'], 2],
            "PCP_093":          [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.1'], ['8.1.2.1.1.{i}', [1, 4], [0, 1]], 3],
            "PCP_094":          [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.1'], ['8.1.2.1.2.{i}', [1, 4], [0, 1]], 4],
            "PCP_096":          [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.1.2.{i}', [1, 10], [1, 4]], ['8.1.2.1.2.{i}.1.{j}', [1, 10], [1, 4]], 5],
            "PCP_099":          [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.1.2.1'], ['8.1.2.1.2.{i}.2.{j}', [0, 1], [1, 3]], 6],
            "PCP_006":          [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.1.2.{i}.2.2]', [1, 10], [0, 1]], ['8.1.2.1.3.{j}', [0, 1], [2, 6]], 7],
            "PCP_095":          [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.2'], ['8.1.2.2.2.{i}', [0, 10], [0, 1]], 8],
            "PCP_102":          [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.2.2.1'], ['8.1.2.2.2.1.1.{j}', [0, 1], [1, 4]], 9],
            "PCP_105":          [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.2.2.1'], ['8.1.2.1.2.1.2.{j}', [0, 1], [1, 4]], 10],
            "PCP_007":          [[2, 3, 4, 5, 6, 7, 8, 9], ['8.1.2.2.2.{i}.2.2', [1, 10], [0, 1]], ['8.1.2.2.3.{j}', [0, 1], [2, 8]], 11],
            "PCP_108":          [[6, 7, 8, 9], ['8.1.2.1.2.{i}.2.1', [1, 10], [0, 1]], ['8.1.2.1.2.{i}.2.1.{j}', [1, 10], [1, 4]], 12],
            "PCP_120":          [[6, 7, 8, 9], ['8.1.2.1.2.1.2.1.1'], ['8.1.2.1.2.1.2.1.1.{j}', [0, 1], [1, 5]], 13],
            "PCP_109":          [[6, 7, 8, 9], ['8.1.2.1.2.1.2.2'], ['8.1.2.1.2.1.2.2.{j}', [0, 1], [1, 4]], 14],
            # "PCP_121":          [[6, 7, 8, 9], '', ['', ''], 14],
            # "PCP_110":          [[6, 7, 8, 9], '', ['', ''], 15],
            # "PCP_122":          [[6, 7, 8, 9], '', ['', ''], 16],
            # "PCP_111":          [[6, 7, 8, 9], '', ['', ''], 17],
            # "PCP_123":          [[6, 7, 8, 9], '', ['', ''], 18],
            # "PCP_245_R":        [[12, 13], '', ['', ''], 19],
            # "DSDs_038_R":       [[12, 13], '', ['', ''], 20],
            # "DSDs_040_R":       [[12, 13], '', ['', ''], 21],
            # "PCP_031_R":        [[12, 13], '', ['', ''], 22],
            # "PCP_031_R_G1":     [[12, 13], '', ['', ''], 23],
            # "W_008":            [[], '', ['', ''], 24],
            # "PCP_035_R":        [[], '', ['', ''], 25],
            # "PCP_035_R_G1":     [[], '', ['', ''], 26],
            # "PCP_038_R":        [[], '', ['', ''], 27],
            # "PCP_038_R_G1":     [[], '', ['', ''], 28],
            # "NCN":              [[], '', ['', ''], 29],
            # "NCV":              [[], '', ['', ''], 30],
            # "NEG":              [[], '', ['', ''], 31],
            # "INT":              [[], '', ['', ''], 32],
            # "DEC":              [[], '', ['', ''], 33],
            # "NNUL":             [[], '', ['', ''], 34]
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