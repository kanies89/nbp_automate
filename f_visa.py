from calendar import monthrange

import pandas as pd
from fiscalyear import FiscalDate
import sys
import win32net as wnet
import os
from connect import connect_single_query

matched_lines = []  # List to store the matched lines

PATH = "y:/Internal/clearing/Visa/"

CARD_TYPE = {
    'D': 'Debit',
    'P': 'Prepaid',
    'C': 'Credit',
    'R': 'Charge'
}

FT = {
    0: ['Lost', 'Zgubienie lub kradzież karty'],
    1: ['Stolen', 'Zgubienie lub kradzież karty'],
    2: ['Not Received', 'Nieodebrana karta'],
    3: ['Fraudulent Application', 'Pozostałe'],
    4: ['Counterfeit Card Fraud', 'Karta sfałszowana'],
    5: ['Miscellaneous', 'Pozostałe'],
    6: ['Fraudulent Use of Account Number', 'Pozostałe'],
    9: ['Acquirer Reported Counterfiet', 'Pozostałe'],

}

NBP_Countries = [
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
    'IT',
    'G1',
    'W2',
    'PL'
]

quarter_months = [
    ['01', '02', '03'],
    ['04', '05', '06'],
    ['07', '08', '09'],
    ['10', '11', '12']
]

months = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12]
]

f_arn = []
f_trx_date = []
f_posted_date = []
f_quarter = []
f_fraud_type = []
f_fraud_type_desc = []
f_card_type = []

EPD_SPLIT = {
    'ARN': [f_arn],
    'trx_date': [f_trx_date],
    'posted_date': [f_posted_date],
    'quarter': [f_quarter],
    'FT': [f_fraud_type],
    'FT description': [f_fraud_type_desc]
}


def open_remote(*argv):
    local_drive = "y:"
    username = input('Provide username (not admin / ladmin): ')
    passwprd = input('Password')  # @TODO - kk: Modified to hide sensitive data
    data = {
        "remote": r"\\prdfil\tf$",
        "local": local_drive,
        "password": passwprd,
    }

    try:
        res = wnet.NetUseAdd(None, 2, data)
        print(res)

    except:
        print("Error adding connection:", sys.exc_info())
        return -1

    print("Items in the shared folder:\n{:}".format(os.listdir(local_drive)))


def check_quarter():
    a = FiscalDate.today()
    print(a)
    q = a.fiscal_quarter

    q_prev = q - 2
    print(q_prev)
    q_year = a.fiscal_year

    if q_prev == 0:
        q_prev = 4
        q_year -= 1

    q_year_str = str(q_year)
    print(q_prev, q_year_str)
    folders = []
    for month in quarter_months[q_prev - 1]:
        folders.append(q_year_str + month)

    print(folders)
    months[q_prev]

    return folders, q_year, months


def grep(path):
    pattern = 'FRDDMC61'  # Replace with your desired pattern
    with open(f'{path}', 'r') as file:
        file = file.readlines()
        for lines in file:
            if pattern in lines:
                if '******' in lines:

                    # Add matching lines from EPD file - with fraud data
                    matched_lines.append(lines)

                    # Retrieve posted date from EPD file name
                    posted_date = path[-16:-10:]
                    posted_date = pd.to_datetime(f'20{posted_date[:2]}/{posted_date[2:4]}/{posted_date[4:]}',
                                                 format='%Y/%m/%d', errors='coerce')
                    f_posted_date.append(posted_date)

                    # Retrieve quarter data from EPD file name
                    print(FiscalDate(posted_date.year, posted_date.month, posted_date.day).fiscal_quarter - 1)
                    if FiscalDate(posted_date.year, posted_date.month, posted_date.day).fiscal_quarter - 1 == 0:
                        quarter = 4
                    else:
                        quarter = FiscalDate(posted_date.year, posted_date.month, posted_date.day).fiscal_quarter - 1

                    f_quarter.append(quarter)


def find():
    open_remote()
    result = check_quarter()

    i = 0

    for folder in result[0]:
        for day in range(monthrange(result[1], result[2][0][i])[1]):
            if day + 1 < 10:
                full_path = f'{PATH}{folder}/{folder}0{str(day + 1)}_INITF.epd'
                print(full_path)
                grep(full_path)
            else:
                full_path = f'{PATH}{folder}/{folder}{str(day + 1)}_INITF.epd'
                print(full_path)
                grep(full_path)

        i += 1

    for line in matched_lines:
        print(line)


def get_data_from_sql():
    arns = ''

    for i in range(len(matched_lines)):
        # Retrieve ARN number
        ml_arn = matched_lines[i][123:123 + 23]
        f_arn.append(ml_arn)

        # Retrieve transaction date
        ml_trx_date = matched_lines[i][92:92 + 6] + '20' + matched_lines[i][98:98 + 2]
        ml_trx_date = pd.to_datetime(ml_trx_date, format='%m/%d/%Y')
        f_trx_date.append(ml_trx_date)

        # Retrieve fraud type
        ml_fraud_type = matched_lines[i][66:66 + 1]
        f_fraud_type.append(ml_fraud_type)

        # Get fraud description
        f_fraud_type_desc.append(FT[ml_fraud_type][1])

        if i == 0:
            arns += "('" + ml_arn + "', "
        elif i == len(matched_lines) - 1:
            arns += "'" + ml_arn + "')"
        else:
            arns += "'" + ml_arn + "', "

    # Add all ARN numbers to sql query
    with open('./query/f_visa/fraud_data_based_on_arn.sql') as sql:
        sql = sql.read()
        sql += arns
    if i + 1 == len(matched_lines):
        print('All ARN numbers passed to SQL query.')
    else:
        print('Not all ARN passed to sql query')

    # Save query
    with open('./query/f_visa/recent_fraud.sql', 'w') as recent:
        recent.write(sql)

    return sql


def nbp_divide(row):
    if row['country'] in NBP_Countries:
        value = row['country']
    else:
        value = 'G1'
    return value


if __name__ == "__main__":
    find()
    df_query = pd.DataFrame(connect_single_query(get_data_from_sql())[0])
    df_query['podział NBP'] = df_query.apply(lambda row: nbp_divide(row), axis=1)
    print(df_query)

    # @TODO - kk: glue the dataframe from sql query with retrieved data from epd
