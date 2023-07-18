from calendar import monthrange
from main import create_folder_structure
from f_visa import check_quarter
import os
import re
ALL = [
    'AD',
    'AE',
    'AF',
    'AG',
    'AI',
    'AL',
    'AM',
    'AO',
    'AR',
    'AT',
    'AU',
    'AW',
    'AZ',
    'BA',
    'BB',
    'BD',
    'BE',
    'BF',
    'BG',
    'BH',
    'BI',
    'BJ',
    'BM',
    'BN',
    'BO',
    'BR',
    'BS',
    'BW',
    'BY',
    'CA',
    'CD',
    'CG',
    'CH',
    'CI',
    'CL',
    'CM',
    'CN',
    'CO',
    'CR',
    'CV',
    'CW',
    'CY',
    'CZ',
    'DE',
    'DJ',
    'DK',
    'DO',
    'DZ',
    'EC',
    'EE',
    'EG',
    'ES',
    'ET',
    'FI',
    'FJ',
    'FR',
    'GA',
    'GB',
    'GD',
    'GE',
    'GH',
    'GI',
    'GM',
    'GN',
    'GQ',
    'GR',
    'GT',
    'GU',
    'GW',
    'HK',
    'HN',
    'HR',
    'HT',
    'HU',
    'ID',
    'IE',
    'IL',
    'IN',
    'IQ',
    'IS',
    'IT',
    'JM',
    'JO',
    'JP',
    'KE',
    'KG',
    'KH',
    'KR',
    'KW',
    'KY',
    'KZ',
    'LA',
    'LB',
    'LC',
    'LI',
    'LK',
    'LR',
    'LT',
    'LU',
    'LV',
    'LY',
    'MA',
    'MC',
    'MD',
    'ME',
    'MG',
    'MK',
    'ML',
    'MM',
    'MN',
    'MO',
    'MR',
    'MT',
    'MU',
    'MV',
    'MW',
    'MX',
    'MY',
    'MZ',
    'NA',
    'NE',
    'NG',
    'NI',
    'NL',
    'NO',
    'NP',
    'NZ',
    'OM',
    'PA',
    'PE',
    'PG',
    'PH',
    'PK',
    'PL',
    'PR',
    'PS',
    'PT',
    'PY',
    'QA',
    'QZ',
    'RO',
    'RS',
    'RU',
    'RW',
    'SA',
    'SC',
    'SD',
    'SE',
    'SG',
    'SI',
    'SK',
    'SL',
    'SM',
    'SN',
    'SS',
    'SV',
    'SX',
    'SZ',
    'TC',
    'TD',
    'TG',
    'TH',
    'TJ',
    'TM',
    'TN',
    'TR',
    'TT',
    'TW',
    'TZ',
    'UA',
    'UG',
    'US',
    'UY',
    'UZ',
    'VA',
    'VG',
    'VI',
    'VN',
    'YE',
    'ZA',
    'ZM',
    'ZW'
]


"""def read_txt_files(directory):
    file_list = os.listdir(directory)
    values = []

    for filename in file_list:
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                contents = file.read()
                found_values = find_values(contents)
                values.extend(found_values)

    return values


def find_values(text):
    values = re.findall(r"'(..)'", text)
    return values


# Example usage
directory_path = './codes/'
all_values = read_txt_files(directory_path)

for a in ALL:
    if a not in all_values:
        print(a)
"""
check = 'ST.07'
checked = check + '_0'
print(check+'_')
print(len(check+'_'))
print(checked[6:0])
