import datetime
from calendar import monthrange
import pandas as pd
from fiscalyear import FiscalDate
import win32wnet
from connect import connect_single_query

matched_lines = []  # List to store the matched lines

PATH = "//prdfil/tf$/Internal/clearing/Visa/"

calc_quarter = int

arns_visa = ''


def disconnect_all_connections():
    try:
        # Disable all existing connections
        win32wnet.WNetCancelConnection2(r"\\prdfil", 0, 1)
    except Exception as e:
        print("\nAn error occurred while disconnecting all connections:", str(e))


def read_remote_file(remote_file_path, username, password):
    try:
        # Disconnect all existing connections
        disconnect_all_connections()

        # Establish a connection to the shared drive with credentials
        netpath = r"\\prdfil"
        win32wnet.WNetAddConnection2(0, None, netpath, None, username, password)

        # Read the remote file
        with open(remote_file_path, 'r') as file:
            file_contents = file.read()

        # Disconnect from the shared drive
        win32wnet.WNetCancelConnection2(netpath, 0, 0)

    except FileNotFoundError:
        print("\nFile not found:", remote_file_path)
    except PermissionError:
        print("\nPermission denied to access the file:", remote_file_path)
    except Exception as e:
        print("\nAn error occurred while reading the remote file:", str(e))


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
    'ARN': f_arn,
    'trx_date': f_trx_date,
    'posted_date': f_posted_date,
    'quarter': f_quarter,
    'FT': f_fraud_type,
    'FT description': f_fraud_type_desc
}


def check_quarter():
    if datetime.date.today().month < 4:
        q = 1
    elif datetime.date.today().month < 7:
        q = 2
    elif datetime.date.today().month < 10:
        q = 3
    else:
        q = 4

    q_prev = q - 1
    q_year = datetime.date.today().year

    if q_prev == 0:
        q_prev = 4
        q_year -= 1

        q_year_str = str(q_year)

        folders = []

        for month in quarter_months[q_prev - 1]:
            folders.append(q_year_str + month)

        months[q_prev - 1]

        return folders, q_year, months, q_prev

    else:
        q_year_str = str(q_year)

        folders = []
        for month in quarter_months[q_prev]:
            folders.append(q_year_str + month)

        months[q_prev]

    return folders, q_year, months, q_prev


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
                    if FiscalDate(posted_date.year, posted_date.month, posted_date.day).fiscal_quarter - 1 == 0:
                        quarter = 4
                    else:
                        quarter = FiscalDate(posted_date.year, posted_date.month, posted_date.day).fiscal_quarter - 1

                    f_quarter.append(quarter)


def find(user, passw):
    # open_remote()
    result = check_quarter()

    i = 0
    username = user
    password = passw
    for folder in result[0]:
        for day in range(1, monthrange(result[1], result[2][0][i])[1]):
            if day < 10:
                full_path = f'{PATH}{folder}/{folder}0{str(day)}_INITF.epd'

                # Example usage
                remote_file_path = full_path  # Remote network path

                read_remote_file(remote_file_path, username, password)
                print('\nChecking files for VISA FRAUD in: '+full_path)
                grep(full_path)
            else:
                full_path = f'{PATH}{folder}/{folder}{str(day)}_INITF.epd'
                print('\nChecking files for VISA FRAUD in: '+full_path)
                grep(full_path)

        i += 1

    for line in matched_lines:
        print('\nFound VISA FRAUD data: '+line)


def get_data_for_sql():
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
        try:
            f_fraud_type_desc.append(FT[int(ml_fraud_type)][1])
        except ValueError:
            f_fraud_type_desc.append(f'Nieznane oznaczenie - {ml_fraud_type}')

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
        print('\nAll ARN numbers passed to SQL query for VISA FRAUD.')
    else:
        print('\nNot all ARN passed to sql query for VISA FRAUD')

    # Save query
    with open('./query/f_visa/recent_fraud.sql', 'w') as recent:
        recent.write(sql)
    print('\nVISA ARNs: ' + arns)
    return sql, arns


def nbp_divide(row):
    if row['country'] in NBP_Countries:
        value = row['country']
    else:
        value = 'G1'
    return value


def f_visa_make(user, passw):
    # Find data from Visa EPD files that matches the fraud records
    find(user, passw)

    # Save ARNs and SQL
    data = get_data_for_sql()
    arns_visa = data[1]
    # Get data from sql query and ARN number retrieved by find()
    df_query = pd.DataFrame(connect_single_query(data[0])[0])
    # Add column 'podział NBP'
    df_query['podział NBP'] = df_query.apply(lambda row: nbp_divide(row), axis=1)

    # Set new dataframe based on data retrieved from find()
    df_epd = pd.DataFrame.from_dict(EPD_SPLIT)

    df_query.to_csv('df_visa_sql.csv')
    df_epd.to_csv('df_visa_epd.csv')

    # Join two dataframes by ARN number
    df_visa_fraud_data = df_query.merge(df_epd, left_on='ARN', right_on='ARN')
    df_visa_fraud_data.to_csv('df_visa_fraud_data.csv')
    print('VISA finished')
    return df_visa_fraud_data, arns_visa


if __name__ == "__main__":
    f_visa_make()[0]
