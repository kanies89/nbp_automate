import pandas as pd
from connect import connect_single_query
from fiscalyear import FiscalDate
from f_visa import NBP_Countries
from f_visa import check_quarter

rows = []

f_arn = []
f_trx_date = []
f_posted_date = []
f_quarter = []
f_fraud_type = []
f_fraud_type_desc = []
f_card_type = []

DATA_SPLIT = {
    'ARN': f_arn,
    'trx_date': f_trx_date,
    'posted_date': f_posted_date,
    'quarter': f_quarter,
    'FT': f_fraud_type,
    'FT description': f_fraud_type_desc
}

FT = {
    0: ['Lost Fraud', 'Zgubienie lub kradzież karty'],
    1: ['Stolen Fraud', 'Zgubienie lub kradzież karty'],
    2: ['Never Received Issue', 'Nieodebrana karta'],
    3: ['Fraudulent Application', 'Pozostałe'],
    4: ['Counterfeit Card Fraud', 'Karta sfałszowana'],
    5: ['Account Takeover Fraud', 'Pozostałe'],
    6: ['Card Not Present Fraud', 'Pozostałe'],
    7: ['Multiple Imprint Fraud', 'Pozostałe'],

}


def read(file):
    try:
        read_file = pd.read_excel(f'{file}.xlsx', header=4)

    except FileNotFoundError:
        read_file = pd.read_excel(f'{file}.csv', header=4)

    return read_file


def add_arn_to_query(dataframe):
    i = 0
    arns = ''
    s = dataframe['Acquirer Reference Number'].size

    for row in dataframe.iterrows():
        if str(row[1][27]) != 'nan':
            if i == 0:
                arns += "('" + str(row[1][27]) + "', "
            elif i == s - 1:
                arns += "'" + str(row[1][27]) + "')"
            else:
                arns += "'" + str(row[1][27]) + "', "

            f_arn.append(str(row[1][27]))

            f_trx_date.append(pd.to_datetime(row[1][2], format='%m%d%Y'))
            posted_date = pd.to_datetime(row[1][11], format='%m%d%Y')
            f_posted_date.append(posted_date)

            # Retrieve quarter data from mastercard excel data
            if FiscalDate(posted_date.year, posted_date.month, posted_date.day).fiscal_quarter - 1 == 0:
                quarter = 4
            else:
                quarter = FiscalDate(posted_date.year, posted_date.month, posted_date.day).fiscal_quarter - 1

            f_quarter.append(quarter)
            fraud_type = row[1][7]
            if fraud_type[0] == '0':
                fraud_type = fraud_type[1]

            f_fraud_type.append(fraud_type)
            # Get fraud description
            try:
                f_fraud_type_desc.append(FT[int(fraud_type)][1])
            except ValueError:
                f_fraud_type_desc.append(fraud_type)

            i += 1
        else:
            s -= 1

    # Add all ARN numbers to sql query
    with open('./query/f_mastercard/fraud_data_based_on_arn.sql') as sql:
        sql = sql.read()
        sql += arns
    if i == s:
        print('\nAll ARN numbers passed to SQL query.')
    else:
        print('\nNot all ARN passed to sql query')

    print('\nMASTERCARD ARNs: ' + arns)

    # Save query
    with open('./query/f_mastercard/recent_fraud.sql', 'w') as recent:
        recent.write(sql)

    return sql, arns


def nbp_divide(row):
    if row['cc_A2'] in NBP_Countries:
        value = row['cc_A2']
    else:
        value = 'G1'
    return value


def f_mastercard_make():
    while True:
        try:
            df_mastercard_http = read(f'{check_quarter()[1]}_{check_quarter()[3]} Mastercard')
            break
        except FileNotFoundError:
            input(f'Insert data into NBP_Report.exe folder, from mastercard fraud service as excel file called: "{check_quarter()[1]}_{check_quarter(3)} Mastercard.xlsx" and then press enter.')

    data = add_arn_to_query(df_mastercard_http)
    arns_mastercard = data[1]
    df_query = pd.DataFrame(connect_single_query(data[0])[0])

    # Add column 'podział NBP'
    df_query['podział NBP'] = df_query.apply(lambda row: nbp_divide(row), axis=1)

    # Set new dataframe based on data retrieved from find()
    df_data = pd.DataFrame.from_dict(DATA_SPLIT)

    path_df = f'.\\temp\\{check_quarter()[1]}_{check_quarter()[3]}\\'
    df_query.to_csv(path_df + 'df_mastercard_sql.csv')
    df_data.to_csv(path_df + 'df_mastercard_epd.csv')

    # Join two dataframes by ARN number
    df_mastercard_fraud_data = df_query.merge(df_data, left_on='ARN', right_on='ARN')
    df_mastercard_fraud_data.rename(columns={'cc_A2': 'country'}, inplace=True)
    df_mastercard_fraud_data.to_csv(path_df + 'df_mastercard_fraud_data.csv')
    print('MASTERCARD finished')
    return df_mastercard_fraud_data, arns_mastercard


if __name__ == '__main__':
    f_mastercard_make()
